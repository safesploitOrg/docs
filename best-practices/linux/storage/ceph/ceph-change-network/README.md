# 🧠 Ceph Public Network Migration (Proxmox)

**172.16.0.0/16 → 10.50.0.0/24**  
_No service downtime, no data loss_

## 📌 Context

This procedure documents a live Ceph public network migration performed on a Proxmox-backed Ceph cluster.  
The goal was to eliminate management-network congestion while maintaining cluster availability and data integrity.

---

  - [🎯 Objective](#-objective)
  - [🧱 Key Concepts (Read Once)](#-key-concepts-read-once)
  - [🚨 Troubleshooting](#-troubleshooting-osds-not-reachable--wrong-subnet)
  - [⚠️ Risks Considered](#-risks-considered)
  - [✅ Final State](#-final-state)

---

## 🎯 Objective

Migrate **all Ceph traffic** (MON, MGR, MDS, OSD front + back) from a congested management network to a **dedicated Ceph fabric** (e.g. 2.5 GbE switch), while keeping the cluster healthy and online.

--- 

## 🧱 Key Concepts (Read Once)

### `public_network`
- Client ↔ OSD traffic  
- MON / MGR control plane  
- CephFS metadata traffic

### `cluster_network`
- OSD ↔ OSD replication & recovery (data plane)

### Important behaviours
- **MON & MGR enforce address validation**
- **OSDs bind addresses at restart**
- `/etc/pve/ceph.conf` is **not authoritative alone** — Ceph also uses its **internal config database**

---

## 1️⃣ Prepare the New Ceph Network

Create a **dedicated bridge** on each node (example: `vmbr-ceph`):

```bash
vim /etc/network/interfaces
```

```ini
auto vmbr-ceph
iface vmbr-ceph inet static
    address 10.50.0.20/24
    bridge-ports eno2
    bridge-stp off
    bridge-fd 0
# Ceph (Fabric)
```

Assign IPs on the new subnet:

- `pve2 → 10.50.0.20/24`
- `pve3 → 10.50.0.30/24`
- `pve4 → 10.50.0.40/24`

Ensure this network is **isolated** (no gateway required).

### Verify connectivity
```bash
ping 10.50.0.30
iperf3 -s / -c <peer>
```

---

## 2️⃣ Add the New Public Network (Dual-Network Phase)

> **NOTE:** Back up the file first
```bash
cp /etc/pve/ceph.conf /etc/pve/ceph.conf.bak
```

Edit `/etc/pve/ceph.conf`:

```ini
public_network = 10.50.0.0/24, 172.16.0.0/16
cluster_network = 10.50.0.0/24, 172.16.0.0/16
```

⚠️ **Do NOT remove the old network yet**

Confirm:
- Proxmox UI → **Ceph → Nodes**
- `ceph config dump`

---

## 3️⃣ Recreate MONs (One by One)

MONs enforce network validation.

For each node:

```bash
pveceph mon destroy <node>
pveceph mon create
ceph -s
```

✔ Ensure quorum after each step.

---

## 4️⃣ Recreate MGRs (One by One)

- Recreate **standby managers first**
- Leave the **active manager for last**

```bash
pveceph mgr destroy <node>
pveceph mgr create
```

Verify:
```bash
ceph mgr dump
```

### 🔧 Recovery Tip
If a manager fails to start:
```bash
systemctl reset-failed ceph-mgr@<node>
systemctl start ceph-mgr@<node>
```

---

## 5️⃣ Recreate CephFS Metadata Servers (MDS)

> MDS binds its address **at creation time**

```bash
pveceph mds destroy <node>
pveceph mds create
```

✔ Verify CephFS health before proceeding.

---

## 6️⃣ Remove the Old Public Network

Edit `/etc/pve/ceph.conf` and remove `172.16.0.0/16`:

```ini
public_network = 10.50.0.0/24
cluster_network = 10.50.0.0/24
```

---

## 7️⃣ Recreate MONs, MGRs, and MDS (Again)

This ensures **all control-plane daemons bind exclusively** to the new network.

Order:
1. MONs (one by one)
2. MGRs (standbys first, active last)
3. MDS (one by one)

---

## 8️⃣ Protect the Cluster Before Touching OSDs

```bash
ceph osd set noout
```

---

## 9️⃣ Restart OSDs (Data Plane Migration)

Restart **one OSD at a time**:

```bash
systemctl restart ceph-osd@<id>
ceph -s
```

Wait for:
```
PGs: active+clean
```

Repeat for all OSDs.

---

## 🔟 Remove Protection

```bash
ceph osd unset noout
```

---

## 🔎 Verification (Critical)

### 1️⃣ Verify Ceph daemon addresses

```bash
ceph osd metadata <id> | egrep 'front_addr|back_addr'
```

Expected:
- ✅ `front_addr → 10.50.0.x`
- ✅ `back_addr → 10.50.0.x`
- ❌ No `172.16.x.x`

---

### 2️⃣ Verify traffic is using the Ceph fabric

While Ceph is under load:

```bash
ip -s link show vmbr-ceph
```

RX/TX counters should increase, confirming traffic is **not** using the management network.

---

### 3️⃣ Verify raw network performance (iperf3)

> ⚠️ **Important:** `iperf3` must be installed on **all Ceph nodes** to test the fabric correctly.

```bash
apt install iperf3
```

**Correct testing method:**

- Server on one node:
```bash
iperf3 -s
```

- Client on a *different* node:
```bash
iperf3 -c <peer_ip> -P 4
```

Expected for 2.5 GbE Ceph fabric:
- **~2.1–2.4 Gbit/s**
- Minimal or zero retransmits
- Stable throughput across multiple streams

---

## 🚨 Troubleshooting: “OSDs Not Reachable / Wrong Subnet”

### Symptom
```text
osd.X's public address is not in '172.16.x.x/16' subnet
```

### Cause
Ceph config DB or MON/MGR cache still references the old network.

### Fix (Critical)

#### Restart ALL MONs (mandatory)
```bash
systemctl restart ceph-mon@pve2
systemctl restart ceph-mon@pve3
systemctl restart ceph-mon@pve4
```

#### Restart ALL MGRs (mandatory)
```bash
systemctl restart ceph-mgr@pve2
systemctl restart ceph-mgr@pve3
systemctl restart ceph-mgr@pve4
```

#### (Optional) Clean config DB
```bash
ceph config rm global public_network
ceph config rm global cluster_network
ceph config set global public_network 10.50.0.0/24
ceph config set global cluster_network 10.50.0.0/24
```

Restart OSDs again (one by one).

✔ This should resolve any “OSDs missing / wrong subnet” cases.

--- 

## ⚠️ Risks Considered

### Why this change is risky

Changing Ceph cluster networking affects quorum, OSD availability, replication traffic, and client IO. Incorrect sequencing can cause data unavailability or permanent loss.

### Failure modes considered
- MON quorum loss
- OSD flapping
- Client IO stalls
- Backfill storms
- Split-brain conditions

### Assumptions
- Single Ceph cluster
- Dedicated replication network (fabric)
- Change executed during low IO window

---

## ✅ Final State

- Dedicated Ceph fabric (2.5 GbE)
- No Ceph traffic on management NIC
- MON / MGR / MDS / OSD fully migrated
- No data loss
- Stable cluster

## 🙏 Acknowledgements

This migration approach was heavily informed by the following Proxmox forum discussion, which proved critical in resolving address-binding and daemon recreation issues during the Ceph public network transition:

- **Proxmox Forum – “Ceph: changing public network”**  
  https://forum.proxmox.com/threads/ceph-changing-public-network.119116/

In particular, the guidance around:
- Temporarily running **dual public networks**
- **Recreating MON, MGR, and MDS daemons** to force address rebinding
- Avoiding full cluster downtime during network migration

was instrumental in achieving a clean, no–data-loss migration.

Many thanks to the contributors in that thread for sharing real-world operational experience.

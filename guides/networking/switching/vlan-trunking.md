# VLAN Trunking (802.1Q)

**VLAN trunking** is a method that allows multiple VLANs to traverse a single physical link between switches or between a switch and another network device.  
It’s defined under the IEEE **802.1Q** standard and is foundational in modern LANs, hypervisors, and cloud networking.

---

## 🧭 Key Concepts

| Term | Description |
|:------|:-------------|
| **VLAN (Virtual LAN)** | A logical segmentation of a Layer 2 network. |
| **Access Port** | Belongs to a single VLAN; used for end devices. |
| **Trunk Port** | Carries traffic for multiple VLANs simultaneously. |
| **Native VLAN** | The VLAN used for untagged frames on a trunk (default = VLAN 1). |
| **802.1Q Tag** | A 4-byte header inserted into Ethernet frames to identify the VLAN ID. |
| **Allowed VLANs** | VLANs permitted on a trunk (others are filtered). |

---

## 🧩 Why Trunking?

Without trunking, each VLAN would need its own physical cable between switches.  
Trunking allows VLAN tagging, enabling **multiple VLANs to share one link**.

> **Example:** A single fibre uplink between two switches can carry VLANs 10, 20, and 30 using 802.1Q tagging.

---

## 💻 Cisco Configuration — Switch to Switch

### **Trunk Link Setup**

```bash
SwitchA(config)# interface GigabitEthernet0/1
SwitchA(config-if)# switchport mode trunk
SwitchA(config-if)# switchport trunk allowed vlan 10,20,30
SwitchA(config-if)# switchport trunk native vlan 99
SwitchA(config-if)# description Trunk_to_SwitchB
```

### **Verification**

```bash
SwitchA# show interfaces trunk
SwitchA# show interface GigabitEthernet0/1 switchport
SwitchA# show vlan brief
```

**Explanation:**
- `switchport mode trunk` enables 802.1Q tagging.
- `allowed vlan` defines which VLANs are permitted.
- `native vlan` defines which VLAN is untagged (commonly changed from VLAN 1 for security).

---

## 🖧 Cisco Access Port Example

```bash
SwitchA(config)# interface GigabitEthernet0/10
SwitchA(config-if)# switchport mode access
SwitchA(config-if)# switchport access vlan 20
SwitchA(config-if)# description HR_Workstation
```

| Port Type | VLAN Handling | Typical Device |
|:-----------|:---------------|:----------------|
| **Access** | Untagged traffic for one VLAN | PCs, printers |
| **Trunk**  | Tagged traffic for many VLANs | Switches, hypervisors, routers |

---

## 🔐 Native VLAN Security

| Risk | Mitigation |
|:------|:-------------|
| VLAN hopping attacks | Avoid VLAN 1 for native VLAN. |
| Untagged frames being misinterpreted | Use a dedicated, unused VLAN as native (e.g. VLAN 99). |
| Management traffic exposure | Isolate management VLANs from user VLANs. |

---

## 🧮 802.1Q Frame Structure

| Field | Size (bytes) | Description |
|:--------|:--------------|:-------------|
| **Destination MAC** | 6 | Target host address |
| **Source MAC** | 6 | Sender address |
| **TPID (Tag Protocol ID)** | 2 | `0x8100` identifies 802.1Q |
| **TCI (Tag Control Info)** | 2 | Contains VLAN ID (12 bits) + Priority bits |
| **EtherType** | 2 | Identifies payload type |
| **Payload** | 46–1500 | Frame contents |
| **FCS** | 4 | Frame Check Sequence |

---

## 🐧 Linux VLAN Trunking (802.1Q)

You can configure VLAN subinterfaces using the `ip` command or `nmcli`.

### **Example: Tagged VLAN on a NIC**

```bash
# Create VLAN interfaces
ip link add link eth0 name eth0.10 type vlan id 10
ip link add link eth0 name eth0.20 type vlan id 20

# Bring them up
ip link set eth0.10 up
ip link set eth0.20 up

# Assign IP addresses
ip addr add 192.168.10.1/24 dev eth0.10
ip addr add 192.168.20.1/24 dev eth0.20
```

**Verification:**
```bash
ip -d link show eth0.10
bridge vlan show
```

---

## 🧱 Proxmox / Virtualised Lab Example

In homelabs or hypervisors like **Proxmox VE**, VLAN trunking allows VMs to connect to multiple VLANs through tagged interfaces.

### **Proxmox Bridge Config Example (`/etc/network/interfaces`)**

```bash
auto vmbr0
iface vmbr0 inet static
    address 192.168.99.10/24
    gateway 192.168.99.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094
```

In VM settings:
- Assign `vmbr0` as the network bridge.
- Set VLAN tag under “Hardware → Network Device → VLAN Tag”.

---

## ☁️ VLANs in AWS VPCs (Analogy)

While AWS doesn’t expose VLANs directly, similar isolation concepts exist:
| Concept | Cisco Equivalent | Purpose |
|:----------|:------------------|:-----------|
| **VPC** | VLAN / VRF | Logical network isolation |
| **Subnet** | VLAN segment | IP range within a VPC |
| **Route Table** | L3 Routing | Determines inter-subnet connectivity |

---

## 🧪 Try It in Your Lab

1. Use two switches (physical or virtual).  
2. Create VLANs 10, 20, and 99.  
3. Configure GigabitEthernet0/1 as a trunk between them.  
4. Assign ports 0/10–0/12 as VLAN 10, 0/13–0/15 as VLAN 20.  
5. Use `show interfaces trunk` and `show vlan brief` to verify.  
6. Test inter-VLAN isolation (ping between VLANs should fail unless routed).

---

## 🧰 Troubleshooting Commands

| Command | Description |
|:----------|:-------------|
| `show vlan brief` | Displays VLAN membership. |
| `show interfaces trunk` | Lists trunked ports and allowed VLANs. |
| `show interfaces switchport` | Detailed port mode and VLAN config. |
| `show mac address-table` | Verifies MAC addresses learned per VLAN. |
| `ping` / `traceroute` | Tests VLAN reachability. |

---

## 📚 Further Reading

- [Cisco: VLAN Trunking Protocol (VTP) and 802.1Q Overview](https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10023-3.html)  
- [IEEE 802.1Q Standard](https://standards.ieee.org/standard/802_1Q-2018.html)  
- [Linux VLAN HowTo](https://wiki.linuxfoundation.org/networking/vlan)  
- [Proxmox VLAN Documentation](https://pve.proxmox.com/wiki/Network_Configuration#sysadmin_network_vlan)

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/switching/vlan-trunking.md`*

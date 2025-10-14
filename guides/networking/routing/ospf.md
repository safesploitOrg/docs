# OSPF (Open Shortest Path First)

**OSPF (Open Shortest Path First)** is a **link-state dynamic routing protocol** defined in **RFC 2328 (OSPFv2)**.  
It uses **Dijkstra’s Shortest Path First (SPF)** algorithm to determine the best path to each destination and supports fast convergence and hierarchical design using **areas**.

---

## 🧭 Key Characteristics

| Feature             | Description                                  |
|:--------------------|:---------------------------------------------|
| **Type**            | Link-state                                   |
| **Algorithm**       | Dijkstra SPF                                 |
| **Metric**          | Cost (based on interface bandwidth)          |
| **Transport**       | IP protocol 89                               |
| **Authentication**  | Plaintext or MD5                             |
| **Convergence Speed** | Fast                                       |
| **Scalability**     | High (multi-area support)                    |

---

## 🧱 OSPF Concepts

| Term                  | Description                                                                 |
|:----------------------|:----------------------------------------------------------------------------|
| **Router ID (RID)**   | Unique 32-bit identifier (often highest IP or manually set).                |
| **Area**              | Logical segmentation (e.g. Area 0 is the backbone).                         |
| **Neighbour**         | Adjacent routers exchanging Hello packets.                                 |
| **Adjacency**         | Fully synchronised routers that share LSDBs.                               |
| **LSA (Link-State Advertisement)** | Packet describing network topology details.                   |
| **LSDB (Link-State Database)**     | The collection of LSAs known to the router.                   |
| **SPF Calculation**   | Determines the shortest path to all destinations.                          |

---

## 🔧 OSPF States

| State         | Description                                            |
|:---------------|:-------------------------------------------------------|
| **Down**       | No Hello packets received.                             |
| **Init**       | Hello received, but no bidirectional comms.            |
| **2-Way**      | Bidirectional Hello exchange.                          |
| **ExStart / Exchange** | Database description (DBD) exchange starts.   |
| **Loading**    | LSRs and LSUs exchanged to synchronise databases.      |
| **Full**       | LSDBs fully synchronised — adjacency established.      |

---

## 💻 Cisco Example — Single Area OSPF

```bash
Router(config)# router ospf 1
Router(config-router)# router-id 1.1.1.1
Router(config-router)# network 10.0.0.0 0.0.0.255 area 0
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0
Router(config-router)# passive-interface default
Router(config-router)# no passive-interface GigabitEthernet0/0
Router(config-router)# end
Router# show ip ospf neighbor
Router# show ip route ospf
```

**Explanation:**
- `network` statements define which interfaces participate in OSPF.
- The **area 0** command places them in the backbone area.
- `passive-interface` prevents unnecessary Hello packets on user-facing interfaces.

---

## 💻 Cisco Example — Multi-Area OSPF

```bash
Router(config)# router ospf 10
Router(config-router)# network 10.0.1.0 0.0.0.255 area 0
Router(config-router)# network 10.1.1.0 0.0.0.255 area 1
Router(config-router)# area 1 stub
```

**Notes:**
- Area 0 is the **backbone**.
- Stub and NSSA areas reduce LSDB size.
- Only **ABRs** connect multiple areas.

---

## 🐧 OSPF on Linux (FRRouting)

```bash
vtysh
conf t
router ospf
 router-id 2.2.2.2
 network 10.0.0.0/24 area 0
 network 192.168.1.0/24 area 0
log file /var/log/frr/ospfd.log
end
write
```

**Verification:**

```bash
show ip ospf neighbor
show ip route ospf
show ip ospf database
```

---

## ☁️ OSPF in AWS and Hybrid Environments

While AWS VPCs don’t natively use OSPF, they support **BGP-based dynamic routing** via:
- **AWS Site-to-Site VPN**
- **Transit Gateway**
- **Direct Connect**

However, OSPF remains highly relevant for:
- **On-premises routing domains** connecting to AWS.
- **Hybrid networks** via edge routers or firewalls (e.g. pfSense/FRR).
- **Lab simulations** (before implementing BGP).

---

## 🧮 OSPF Cost Calculation

**Cost = Reference Bandwidth / Interface Bandwidth**

Default reference bandwidth = 100 Mbps

| Interface         | Bandwidth | Default Cost |
|:------------------|:-----------|:--------------|
| **FastEthernet**  | 100 Mbps  | 1             |
| **GigabitEthernet** | 1 Gbps  | 1 (adjust reference) |
| **10-Gigabit**    | 10 Gbps   | 1 (unless adjusted)  |

**Adjusting Reference Bandwidth:**

```bash
Router(config-router)# auto-cost reference-bandwidth 10000
```

> Ensures 10G+ interfaces have realistic costs.

---

## 🔒 OSPF Security

| Control               | Description                                          |
|:-----------------------|:-----------------------------------------------------|
| **Authentication**     | Plaintext or MD5 keychain (per-interface or area).  |
| **Passive Interfaces** | Stops Hello packets on end-user ports.              |
| **LSA Filtering**      | Prevents unnecessary flooding.                      |
| **Route Filtering**    | Limits external redistribution.                     |

**Example (MD5 Authentication):**

```bash
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip ospf authentication message-digest
Router(config-if)# ip ospf message-digest-key 1 md5 MySecureKey
```

---

## 🧪 Try It in Your Lab

1. Build a 3-router topology (e.g., using your Cisco 3750X stack or GNS3).  
2. Configure OSPF single area.  
3. Observe neighbour adjacencies (`show ip ospf neighbor`).  
4. Introduce multi-area design.  
5. Enable authentication between two routers.  
6. Observe route convergence when a link is brought down.

---

## 🧰 Troubleshooting Tips

| Command                  | Purpose                            |
|:--------------------------|:-----------------------------------|
| `show ip ospf neighbor`   | Verify adjacencies.                |
| `show ip ospf database`   | Inspect LSDB contents.             |
| `show ip protocols`       | Check OSPF configuration.          |
| `debug ip ospf adj`       | View adjacency formation logs.     |
| `ping` / `traceroute`     | Verify end-to-end reachability.    |

---

## 📚 Further Reading

- [RFC 2328 — OSPFv2 Specification](https://datatracker.ietf.org/doc/html/rfc2328)  
- [Cisco OSPF Configuration Guide](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/7039-1.html)  
- [FRRouting OSPF Documentation](https://docs.frrouting.org/en/latest/ospfd.html)

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/routing/`*

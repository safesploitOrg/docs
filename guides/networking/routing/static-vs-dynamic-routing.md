# Static vs Dynamic Routing

Routing defines how packets travel from one network to another.  
This guide compares **static** and **dynamic** routing — when to use each, configuration examples, and how they apply in both on-prem and cloud (AWS VPC) environments.

---

## 🧭 Overview

| Type | Description | Use Case |
|:------|:-------------|:-----------|
| **Static Routing** | Administrator manually defines routes. | Small networks, lab setups, or edge routing with predictable paths. |
| **Dynamic Routing** | Routers exchange routes automatically using protocols (e.g. OSPF, BGP). | Large, scalable, or frequently changing environments. |

---

## 🧱 Static Routing

Static routes are **manually configured** and **do not change** unless the admin modifies them.  
They’re predictable and simple but don’t adapt to network failures automatically.

### ✅ Advantages
- Full control — no route advertisement leaks.
- Minimal overhead (CPU/RAM, no protocol chatter).
- Easier auditing and debugging (you know every path).

### ❌ Disadvantages
- No automatic failover.
- High admin overhead at scale.
- Prone to human error (typos, forgotten updates).

### 💻 Example — Linux

```bash
# Add a static route (temporary)
ip route add 10.20.0.0/16 via 192.168.1.1

# Make persistent (RHEL/AlmaLinux)
echo "10.20.0.0/16 via 192.168.1.1 dev eth0" >> /etc/sysconfig/network-scripts/route-eth0
```

### 💻 Example — Cisco IOS

```bash
Router(config)# ip route 10.20.0.0 255.255.0.0 192.168.1.1
Router(config)# do show ip route static
```

---

## 🔄 Dynamic Routing

Dynamic routing protocols **learn and share routes** automatically.  
They detect network changes and reroute traffic when links fail — ideal for large, redundant topologies.

### Common Protocols

| Protocol | Type | Notes |
|:----------|:------|:------|
| **RIP** | Distance-vector | Obsolete; max 15 hops; good for labs. |
| **OSPF** | Link-state | Hierarchical; ideal for enterprise LANs. |
| **EIGRP** | Hybrid | Cisco-proprietary (now partially open). |
| **BGP** | Path-vector | Used for ISPs, multi-site, and AWS Transit Gateway. |

### ✅ Advantages
- Auto-learns topology.
- Supports failover and load balancing.
- Reduces admin workload.

### ❌ Disadvantages
- More complex to configure and troubleshoot.
- Consumes CPU/RAM for routing table updates.
- Protocol misconfigurations can propagate quickly.

---

## 🧰 Example — OSPF on Cisco

```bash
Router(config)# router ospf 1
Router(config-router)# network 10.0.0.0 0.0.0.255 area 0
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0
Router(config)# do show ip ospf neighbor
```

### Example — OSPF on Linux (FRRouting)

```bash
vtysh
router ospf
 network 10.0.0.0/24 area 0
 network 192.168.1.0/24 area 0
```

---

## ☁️ Example — AWS VPC Routing

| Type | Description | Example |
|:------|:-------------|:-----------|
| **Static Route** | Added manually to route table. | `10.0.2.0/24 → nat-0abc12345` |
| **Dynamic Route** | Propagated from VPN / Direct Connect / TGW. | Automatically updates with BGP peers. |

> AWS route propagation uses **BGP** under the hood when connected via VPN or Direct Connect gateways.

---

## 🧩 When to Use Which

| Scenario | Recommended |
|:-----------|:-------------|
| Small lab / testbed | Static |
| Branch offices with few routes | Static or OSPF stub |
| Multi-site enterprise | OSPF / EIGRP |
| Internet peering, cloud hybrid | BGP |
| AWS VPCs with VPN or TGW | Dynamic (BGP propagation) |

---

## 🔒 Security Considerations

- Disable unused routing protocols (`no router rip` if not in use).
- Authenticate OSPF or BGP neighbours (MD5 / keychain).
- Filter route advertisements (prefix-lists, route-maps).
- Avoid default route leaks in hybrid environments.

---

## 🧪 Try It in Your Lab

1. Build a 3-router topology (3750X or GNS3/Packet Tracer).  
2. Configure static routes between all subnets.  
3. Replace them with OSPF (single area).  
4. Simulate a link failure — note how OSPF self-heals, but static does not.  
5. For cloud comparison, replicate the same in AWS using two VPCs with BGP-enabled site-to-site VPNs.

---

## 📚 Further Reading

- [Cisco: Static vs Dynamic Routing](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13684-12.html)
- [AWS: Route Tables and Propagation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [RFC 2328 — OSPFv2](https://datatracker.ietf.org/doc/html/rfc2328)

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/routing/`*

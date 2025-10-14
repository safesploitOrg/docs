# BGP (Border Gateway Protocol)

**BGP (Border Gateway Protocol)** is a **path-vector routing protocol** used to exchange routing information between **autonomous systems (AS)** on the Internet (eBGP) or within a large organisation (iBGP).  
Defined in **RFC 4271**, it’s the backbone of the Internet and commonly used in hybrid cloud setups (e.g. AWS Direct Connect or VPN route propagation).

---

## 🧭 Key Characteristics

| Feature                | Description |
|:------------------------|:------------|
| **Type**                | Path-vector |
| **Algorithm**           | Based on AS-PATH, policy, and attributes |
| **Transport**           | TCP port 179 |
| **Metric**              | Multi-attribute (weight, local-pref, AS-path, etc.) |
| **Scalability**         | Very high (Internet-grade) |
| **Convergence**         | Slower than OSPF but stable |
| **Authentication**      | MD5 optional |
| **Use Case**            | ISP peering, hybrid cloud, WAN, and data centre edge |

---

## 🧱 BGP Concepts

| Term / Attribute | Description |
|:-----------------|:-------------|
| **AS (Autonomous System)** | A group of routers under a single administrative domain. |
| **iBGP / eBGP**            | iBGP (internal) within the same AS; eBGP (external) between ASes. |
| **Neighbor (Peer)**        | Router that exchanges BGP updates with another. |
| **AS-PATH**                | Sequence of AS numbers a route has traversed (used for loop prevention). |
| **NEXT_HOP**               | IP address of the next hop for reaching a destination. |
| **LOCAL_PREF**             | Preference for outbound routes within an AS (higher = preferred). |
| **MED (Multi-Exit Discriminator)** | Suggests preferred inbound route from neighbouring AS. |
| **Weight**                 | Cisco-specific, local to the router; higher = preferred. |
| **Prefix Filtering**       | Controls which prefixes are advertised or accepted. |

---

## 🔄 BGP Session Types

| Session Type | Description | Example |
|:--------------|:-------------|:----------|
| **eBGP** | Between routers in different ASes | AS 65001 ↔ AS 65002 |
| **iBGP** | Between routers in the same AS | AS 65001 ↔ AS 65001 |
| **Route Reflector** | iBGP router that redistributes routes to clients | Reduces iBGP full-mesh requirement |

---

## 💻 Cisco BGP Example — eBGP Peering

```bash
RouterA(config)# router bgp 65001
RouterA(config-router)# neighbor 192.168.100.2 remote-as 65002
RouterA(config-router)# network 10.0.0.0 mask 255.255.255.0
RouterA(config-router)# neighbor 192.168.100.2 description eBGP-to-RouterB
RouterA(config-router)# end

RouterA# show ip bgp summary
RouterA# show ip bgp
```

**Explanation:**
- The router advertises `10.0.0.0/24` to its eBGP neighbour in AS 65002.
- BGP sessions use **TCP port 179**.
- eBGP default TTL = 1 (directly connected peers only).

---

## 💻 Cisco BGP Example — iBGP Peering

```bash
RouterA(config)# router bgp 65001
RouterA(config-router)# neighbor 10.1.1.2 remote-as 65001
RouterA(config-router)# neighbor 10.1.1.2 update-source Loopback0
RouterA(config-router)# network 172.16.0.0 mask 255.255.255.0
```

**Notes:**
- iBGP requires a full mesh between all routers in an AS (unless using route reflectors or confederations).
- Loopback interfaces ensure session stability.

---

## 🐧 BGP on Linux (FRRouting)

```bash
vtysh
conf t
router bgp 65010
 bgp router-id 1.1.1.1
 neighbor 192.168.1.2 remote-as 65020
 neighbor 192.168.1.2 description EBGP-to-AS65020
 network 10.10.0.0/16
end
write
```

**Verification:**

```bash
show ip bgp summary
show ip bgp
show ip bgp neighbors
```

---

## ☁️ BGP in AWS and Cloud Context

AWS uses **BGP for route propagation** between:
- **Customer Gateway (CGW)** and **Virtual Private Gateway (VGW)** in VPN setups.
- **Transit Gateway (TGW)** and **Direct Connect Gateways (DXGW)**.
- **Hybrid environments** — enabling dynamic route exchange with on-prem routers.

**Example AWS BGP session:**
| Local Device | Peer | Type | AS Number | Notes |
|:--------------|:------|:------|:------------|:--------|
| pfSense       | AWS VGW | eBGP | 65001 ↔ 7224 | Routes advertised dynamically |
| Cisco ISR     | AWS DXGW | eBGP | 65010 ↔ 64512 | Uses MD5 authentication over TCP 179 |

---

## 🧮 BGP Path Selection (Simplified)

BGP selects the **best route** using these attributes (in order):

1. Highest **Weight** (Cisco only)  
2. Highest **Local Preference**  
3. Locally originated route (`network` or `aggregate-address`)  
4. Shortest **AS-PATH**  
5. Lowest **Origin type** (IGP < EGP < Incomplete)  
6. Lowest **MED**  
7. eBGP learned routes preferred over iBGP  
8. Lowest **IGP metric** to the next hop  
9. Lowest **Router ID**

---

## 🔒 Security and Filtering

| Mechanism | Description |
|:------------|:-------------|
| **Prefix-lists / Route-maps** | Limit which routes are advertised or received. |
| **MD5 Authentication** | Protects against session hijacking. |
| **TTL Security / GTSM** | Prevents spoofed packets from non-adjacent routers. |
| **Max-prefix Limit** | Prevents accidental large route advertisements. |
| **Route Dampening** | Avoids flapping route instability. |

**Example (Cisco):**

```bash
Router(config)# router bgp 65001
Router(config-router)# neighbor 192.168.100.2 password MySecureBGPkey
Router(config-router)# neighbor 192.168.100.2 ttl-security hops 1
Router(config-router)# neighbor 192.168.100.2 maximum-prefix 100
```

---

## 🧪 Try It in Your Lab

1. Use two routers or VMs (Cisco or FRR).  
2. Configure **AS 65001** on Router A and **AS 65002** on Router B.  
3. Advertise unique prefixes (`10.0.0.0/24`, `10.1.0.0/24`).  
4. Establish an eBGP session.  
5. Verify using `show ip bgp summary` and confirm route exchange.  
6. Break the link — observe hold timers and session re-establishment.  
7. Optionally, integrate pfSense or AWS VPN to test hybrid propagation.

---

## 🧰 Troubleshooting Commands

| Command | Description |
|:----------|:-------------|
| `show ip bgp summary` | Displays session status and ASNs. |
| `show ip bgp neighbors` | Shows BGP capabilities and state. |
| `show ip bgp` | Displays learned and advertised routes. |
| `debug ip bgp updates` | Shows real-time route advertisement. |
| `clear ip bgp *` | Resets BGP sessions. |

---

## 📚 Further Reading

- [RFC 4271 — BGP-4 Specification](https://datatracker.ietf.org/doc/html/rfc4271)  
- [Cisco BGP Configuration Guide](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/1966-25.html)  
- [FRRouting BGP Documentation](https://docs.frrouting.org/en/latest/bgp.html)  
- [AWS VPN and Direct Connect Routing](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNRouting.html)

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/routing/`*

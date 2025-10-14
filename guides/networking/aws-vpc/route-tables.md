# AWS VPC Route Tables

AWS **Route Tables** define how network traffic is directed within and outside a **Virtual Private Cloud (VPC)**.  
They determine where packets go based on their destination IP address — similar to routing tables in traditional networks or routers.

---

## 🧭 Key Concepts

| Term | Description |
|:------|:-------------|
| **VPC** | Virtual Private Cloud — logically isolated section of AWS network. |
| **Route Table** | A set of rules (routes) that determine where traffic for a subnet is directed. |
| **Subnet Association** | Each subnet must be explicitly or implicitly associated with a route table. |
| **Main Route Table** | The default route table automatically associated with all subnets unless overridden. |
| **Custom Route Table** | Manually created route table for specific subnets or routing domains. |
| **Target** | The next hop for a route (e.g. Internet Gateway, NAT Gateway, Transit Gateway, etc.). |

---

## 🧱 How Routing Works in AWS

When an instance sends a packet, AWS checks:
1. Which subnet the instance belongs to.
2. Which **route table** is associated with that subnet.
3. Which route in the table matches the **destination CIDR**.
4. Which **target** to use (e.g., IGW, NATGW, TGW, ENI).

---

## 🧩 Example: Default Route Table

| Destination | Target | Purpose |
|:--------------|:---------|:----------|
| `10.0.0.0/16` | `local` | Routes traffic within the VPC (always present). |

> Every VPC has an implicit **local route** that enables internal communication between subnets.

---

## ☁️ Example: Public Subnet Route Table

```plaintext
Destination        Target              Description
---------------------------------------------------------
10.0.0.0/16        local               Intra-VPC routing
0.0.0.0/0          igw-0abc12345       Internet access via IGW
```

**Explanation:**
- `local` allows private communication within the VPC.
- `0.0.0.0/0` sends all non-local traffic to the Internet Gateway.
- Subnets associated with this table become **public subnets**.

---

## 🔒 Example: Private Subnet Route Table

```plaintext
Destination        Target              Description
---------------------------------------------------------
10.0.0.0/16        local               Intra-VPC routing
0.0.0.0/0          nat-0def6789        Outbound Internet via NAT Gateway
```

- No direct Internet Gateway route.
- Instances can **initiate** outbound connections but cannot be reached from the Internet.
- Subnets associated with this table are **private**.

---

## 🏗️ Example: Hybrid / VPN Route Table

```plaintext
Destination        Target              Description
---------------------------------------------------------
10.0.0.0/16        local               VPC internal routes
172.16.0.0/12      vgw-0aa123bb        VPN connection to on-prem
0.0.0.0/0          nat-0def6789        Internet access (via NATGW)
```

**Notes:**
- The **VGW (Virtual Private Gateway)** enables BGP route propagation from on-prem.
- Routes from VPNs or Direct Connect links can appear automatically when **route propagation** is enabled.

---

## 🛰️ Peering & Transit Gateway Routes

| Scenario | Route Example | Target | Purpose |
|:-----------|:----------------|:-----------|:-----------|
| **VPC Peering** | `10.2.0.0/16` | `pcx-0abc9fgh` | Enables routing to peer VPC. |
| **Transit Gateway (TGW)** | `10.3.0.0/16` | `tgw-0xyz1234` | Central routing hub for multi-VPC or hybrid networks. |
| **Direct Connect** | `172.31.0.0/16` | `dxvif-0de12345` | Private connection to on-premises environment. |

> Always ensure both sides of the peering or TGW connection have **reciprocal routes** configured.

---

## 🔁 Route Propagation

AWS can automatically propagate routes from:
- **VPN connections**
- **Direct Connect gateways**
- **Transit Gateways**

### Enable Route Propagation (Example)
```bash
aws ec2 enable-vgw-route-propagation   --gateway-id vgw-0aa123bb   --route-table-id rtb-0ff56789
```

---

## 🧮 CIDR & Route Table Example

| Subnet | CIDR | Route Table | Internet Access | Description |
|:---------|:------|:--------------|:----------------|:--------------|
| `Public-A` | 10.0.1.0/24 | `rtb-public` | ✅ | Internet via IGW |
| `Private-A` | 10.0.2.0/24 | `rtb-private` | ❌ | NATGW via Public subnet |
| `VPN-Subnet` | 10.0.3.0/24 | `rtb-hybrid` | 🔄 | VPN via VGW |
| `TGW-Subnet` | 10.0.4.0/24 | `rtb-tgw` | 🔄 | Transit Gateway |

---

## 🔒 Security & Best Practices

| Category | Best Practice |
|:------------|:---------------|
| **Least Privilege Routing** | Only add routes that are needed. |
| **Separation of Environments** | Use separate route tables for prod/dev/test. |
| **Audit Regularly** | Periodically review with `aws ec2 describe-route-tables`. |
| **Avoid IGW on Private Subnets** | Prevents accidental Internet exposure. |
| **Tag Route Tables** | Use consistent tags (e.g., `Environment`, `SubnetType`). |

---

## 🧰 CLI Commands

| Command | Purpose |
|:----------|:-----------|
| `aws ec2 describe-route-tables` | List all route tables. |
| `aws ec2 create-route` | Add a route to a table. |
| `aws ec2 replace-route` | Modify an existing route. |
| `aws ec2 delete-route` | Remove a route. |
| `aws ec2 associate-route-table` | Link a route table to a subnet. |

---

## 🧪 Lab Exercise

1. Create a VPC with CIDR `10.0.0.0/16`.  
2. Create two subnets: `10.0.1.0/24` (public) and `10.0.2.0/24` (private).  
3. Deploy an Internet Gateway and a NAT Gateway.  
4. Create route tables for public and private subnets.  
5. Test connectivity:
   - Public subnet → Internet ✅  
   - Private subnet → Internet via NAT ✅  
   - Private subnet inbound ❌  

---

## 📚 Further Reading

- [AWS Route Tables Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)  
- [AWS Transit Gateway Routing](https://docs.aws.amazon.com/vpc/latest/tgw/working-with-routes.html)  
- [AWS VPN Routing Guide](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNRouting.html)  
- [RFC 1519 — CIDR Overview](https://datatracker.ietf.org/doc/html/rfc1519)

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/aws-vpc/`*


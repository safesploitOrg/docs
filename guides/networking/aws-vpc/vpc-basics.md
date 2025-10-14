# AWS VPC Basics

An **Amazon Virtual Private Cloud (VPC)** is a logically isolated section of the AWS cloud where you can launch AWS resources in a **custom IP network** that you define.  
It behaves like an on-premises data centre network, giving full control over **IP addressing**, **subnetting**, **routing**, **firewalls**, and **connectivity**.

---

## 🧭 Core VPC Components

| Component | Description |
|:------------|:-------------|
| **VPC** | The root container for all AWS networking resources. |
| **Subnet** | Logical segmentation within a VPC (public or private). |
| **Route Table** | Defines how traffic is directed within or outside the VPC. |
| **Internet Gateway (IGW)** | Enables Internet access for public subnets. |
| **NAT Gateway (NATGW)** | Enables private subnets to initiate outbound traffic securely. |
| **Network ACL (NACL)** | Stateless packet filter applied at subnet level. |
| **Security Group (SG)** | Stateful firewall applied to instances/ENIs. |
| **VPC Peering / Transit Gateway** | Connects multiple VPCs or hybrid networks. |

---

## 🧩 Default vs Custom VPCs

| Type | Description | Characteristics |
|:-------|:-------------|:----------------|
| **Default VPC** | Automatically created per region. | One public subnet per AZ, Internet access enabled, auto-created SG and route table. |
| **Custom VPC** | Manually defined for fine-grained control. | Choose CIDR, subnets, route tables, gateways, and security boundaries. |

> Best practice: Create and manage **Custom VPCs** for production — default VPCs are for testing or quick labs.

---

## 🧱 VPC CIDR and Subnetting

Each VPC is assigned an **IPv4 CIDR block** (and optionally IPv6).  
AWS allows between **/16 and /28** for the VPC’s CIDR range.

### Example:
```
VPC CIDR: 10.0.0.0/16
Subnet-A: 10.0.1.0/24 (Public)
Subnet-B: 10.0.2.0/24 (Private)
Subnet-C: 10.0.3.0/24 (Private)
```

| Subnet | CIDR | AZ | Type | Route Table | Internet Access |
|:---------|:------|:------|:------|:--------------|:----------------|
| Public-A | 10.0.1.0/24 | eu-west-2a | Public | Public RT | ✅ |
| Private-A | 10.0.2.0/24 | eu-west-2a | Private | Private RT | ❌ |
| Private-B | 10.0.3.0/24 | eu-west-2b | Private | Private RT | ❌ |

> Each subnet resides entirely within one Availability Zone.

---

## ☁️ VPC Architecture Overview

```
                 +-----------------------------+
                 |         AWS Cloud           |
                 |   VPC: 10.0.0.0/16          |
                 |                             |
     +-----------+-----------------------------+-----------+
     | Public Subnet (10.0.1.0/24)                         |
     |  EC2 (Web)  -->  IGW (Internet Gateway)             |
     +------------------------------------------------------+
     | Private Subnet (10.0.2.0/24)                        |
     |  EC2 (App/DB) --> NATGW (Outbound only)             |
     +------------------------------------------------------+
```

- **Public Subnet:** Contains resources needing Internet access (e.g. bastion hosts, web servers).  
- **Private Subnet:** Isolated, no direct inbound access (e.g. DB, backend apps).  
- **NAT Gateway:** Allows outbound Internet access from private subnets.  
- **IGW:** Allows inbound/outbound Internet for public subnets.

---

## 🔄 Route Table Behaviour

| Destination | Target | Description |
|:--------------|:----------|:-------------|
| `10.0.0.0/16` | local | Enables internal VPC communication. |
| `0.0.0.0/0` | igw-xxxxxx | Internet access for public subnets. |
| `0.0.0.0/0` | nat-xxxxxx | Outbound Internet via NATGW for private subnets. |

> Each subnet can be associated with only **one route table**, but a route table can be associated with **multiple subnets**.

---

## 🔐 Security Model: NACL vs Security Groups

| Feature | Network ACL (NACL) | Security Group (SG) |
|:-----------|:------------------|:----------------------|
| **Type** | Stateless | Stateful |
| **Scope** | Subnet-level | Instance/ENI-level |
| **Rules Evaluated** | Inbound + Outbound | Inbound + Outbound |
| **Default Behaviour** | Deny all (custom) / Allow all (default) | Deny all inbound, allow all outbound |
| **Use Case** | Granular subnet filtering | Instance-level firewalling |

---

## 🧰 Common AWS CLI Commands

| Command | Description |
|:-----------|:-------------|
| `aws ec2 describe-vpcs` | List all VPCs. |
| `aws ec2 create-vpc --cidr-block 10.0.0.0/16` | Create a new VPC. |
| `aws ec2 describe-subnets` | Show subnet details. |
| `aws ec2 create-subnet --vpc-id vpc-xxxx --cidr-block 10.0.1.0/24` | Create subnet. |
| `aws ec2 describe-route-tables` | List route tables. |
| `aws ec2 describe-security-groups` | List security groups. |

---

## 🧪 Lab Exercise

1. Create a custom VPC (`10.0.0.0/16`).  
2. Create two subnets (`10.0.1.0/24` public, `10.0.2.0/24` private).  
3. Attach an Internet Gateway.  
4. Create two route tables:
   - Public → IGW for Internet.
   - Private → NAT Gateway for outbound Internet.  
5. Launch EC2 instances in each subnet and verify:
   - Public EC2 → Internet ✅  
   - Private EC2 → Internet via NAT ✅  
   - Private EC2 → Direct inbound ❌  

---

## 🧩 Integration with On-Prem / Multi-VPC

AWS supports multiple interconnect options:

| Connection Type | Description | Routing Type |
|:------------------|:-------------|:---------------|
| **VPC Peering** | Point-to-point connection between VPCs. | Static routes |
| **Transit Gateway (TGW)** | Central hub for multi-VPC or hybrid connectivity. | Dynamic (BGP optional) |
| **VPN / Direct Connect** | Connect on-premises networks. | Static or BGP dynamic routing |

---

## 🔒 Security Best Practices

- Use **custom VPCs** — disable default VPCs in production.  
- Change **default security groups** — restrict inbound access.  
- Separate environments (Prod / Dev / Test) into different VPCs.  
- Enforce **least privilege routing** and network isolation.  
- Use **Flow Logs** for visibility and auditing.  
- Tag all network components consistently.

---

## 📚 Further Reading

- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)  
- [AWS Subnetting Guide](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)  
- [AWS NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)  
- [AWS Transit Gateway Overview](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)  

---

*Author: Zepher Ashe (@safesploit)*  
*Part of safesploitOrg/docs → `/guides/networking/aws-vpc/`*

# Networking — Overview

Welcome to the **Networking Guides** section of the safesploitOrg/docs repository.
This folder provides structured, vendor-neutral networking documentation — blending Cisco fundamentals, homelab practice, and public cloud design.

---

## 📂 Structure

```
guides/
└── networking/
    ├── README.md
    ├── subnetting/
    │   ├── cidr-table.md
    │   ├── vlsm.md
    │   └── examples.md
    ├── routing/
    │   ├── static-vs-dynamic.md
    │   ├── ospf.md
    │   └── bgp.md
    ├── switching/
    │   ├── vlan-trunking.md
    │   ├── spanning-tree.md
    │   └── etherchannel.md
    ├── aws-vpc/
    │   ├── vpc-basics.md
    │   ├── route-tables.md
    │   └── private-public-subnets.md
    └── firewalling/
        ├── pfsense-lab.md
        ├── nftables.md
        └── security-groups.md
```

Each directory focuses on a topic area and keeps Markdown guides short, practical, and example-driven.

---

## 🌐 Topics Covered

| Area                        | Description                                                | Example Guides             |
| :-------------------------- | :--------------------------------------------------------- | :------------------------- |
| **Subnetting & Addressing** | CIDR, VLSM, IPv4/IPv6, subnet planning.                    | `cidr-table.md`, `vlsm.md` |
| **Routing**                 | Static vs dynamic routing, OSPF, BGP, route summarisation. | `ospf.md`, `bgp.md`        |
| **Switching**               | VLANs, trunking, EtherChannel, STP, inter-VLAN routing.    | `vlan-trunking.md`         |
| **Firewalling**             | pfSense setup, nftables, ACLs, AWS Security Groups.        | `pfsense-lab.md`           |
| **Cloud Networking**        | AWS VPCs, route tables, subnets, NAT gateways, peering.    | `vpc-basics.md`            |
| **Network Automation**      | Ansible network modules, IaC patterns for networking.      | `ansible-networking.md`    |

---

## 🔗 External References

* VLSM calculator → [https://vlsm.git.safesploit.com/](https://vlsm.git.safesploit.com/)
* AWS VPC documentation → [https://docs.aws.amazon.com/vpc/](https://docs.aws.amazon.com/vpc/)
* Cisco Networking Basics → [https://www.cisco.com/c/en/us/training-events/training-certifications/exams/current-list/ccna.html](https://www.cisco.com/c/en/us/training-events/training-certifications/exams/current-list/ccna.html)

---

## 🧭 Contribution Guidelines

1. Use `kebab-case` filenames (e.g. `route-summarisation.md`).
2. Keep guides short (500–1200 words) and command-focused.
3. Include diagrams (ASCII or embedded PNG/SVG) where useful.
4. Add a **“Try it in your lab”** section for reproducibility.
5. Reference standards (RFCs, AWS docs, Cisco docs) when relevant.


# OpenWRT

- [Overview](#openwrt-overview)
- [🏗 Core Architecture](#openwrt-corearchitecture)
  - [Key components:](#openwrt-keycomponents)
- [🌐 Why People Use OpenWrt](#openwrt-whypeopleuseopenwrt)
  - [1️⃣ Advanced Networking](#openwrt-1advancednetworking)
  - [2️⃣ Firewall Control](#openwrt-2firewallcontrol)
  - [3️⃣ Package Ecosystem](#openwrt-3packageecosystem)
- [🖥 Hardware Support](#openwrt-hardwaresupport)
- [OpenWRT Best Practices](#openwrt-openwrtbestpractices)
- [Community and Resources](#openwrt-communityandresources)
- [🧠 How OpenWrt Differs from pfSense](#openwrt-howopenwrtdiffersfrompfsense)
- [Use Cases](#openwrt-usecases)
  - [🔬 Common Advanced Use Cases](#openwrt-commonadvancedusecases)

---

## Overview

OpenWRT is an open-source Linux-based operating system for embedded devices, primarily used as a router firmware. It is designed to be flexible, powerful, and secure, offering advanced networking features that are not available in many stock router firmwares. OpenWRT allows for extensive customizability, including support for third-party applications, VPNs, firewall configurations, and much more.

## 🏗 Core Architecture

OpenWrt is not just “firmware” — it’s a **modular embedded Linux system**.

### Key components:

- **BusyBox** – Lightweight Unix utilities
- **procd** – Init system (OpenWrt’s service manager)
- **netifd** – Network interface daemon
- **ubus** – IPC message bus
- **uci** – Unified Configuration Interface
- **opkg** – Package manager
- **LuCI** – Web UI (optional but common)

Unlike stock firmware:

- You get **full shell access**
- You can install/remove packages
- No hidden vendor services

---

## 🌐 Why People Use OpenWrt

### 1️⃣ Advanced Networking

- VLAN tagging (802.1Q)
- Policy routing
- Multiple SSIDs
- Guest networks with isolation
- Multi-WAN failover/load balancing
- Static routes
- WireGuard / OpenVPN
- QoS / SQM (bufferbloat control)

### 2️⃣ Firewall Control

Uses **nftables (modern versions)** or iptables (older).

You can:

- Create zone-based firewalls
- Do NAT, port forwarding
- Write custom rules
- Segment lab environments properly

Perfect for homelab VLAN segregation (which you’re already doing with pfSense).

---

### 3️⃣ Package Ecosystem

Installable packages include:

- `tcpdump`
- `htop`
- `nmap`
- `wireguard`
- `adblock`
- `sqm-scripts`
- `collectd`
- `docker` (on more powerful devices)

It’s basically a tiny Debian for routers.

---

## 🖥 Hardware Support

Supports:

- Consumer routers (TP-Link, Netgear, Linksys, GL.iNet, etc.)
- x86 devices
- Embedded ARM boards

Not all routers are supported — always check:

> <https://openwrt.org/toh/start>

Flash size matters:

- 8MB flash = painful
- 16MB = workable
- 32MB+ = comfortable
- 128MB+ = ideal

---

## OpenWRT Best Practices

[OpenWRT Best Practices](OpenWRT/OpenWRT%20Configuration/OpenWRT%20Best%20Practices.md)

- Performance Optimization
- Security Hardening Tips
- Long-Term Device Management
- Automation and Remote Management

---

## Community and Resources

- OpenWRT Official Documentation: <https://openwrt.org/start>
- Community Forums and Mailing Lists
- GitHub Repositories <https://github.com/openwrt>
- Tutorials and Blogs   
  <https://www.reddit.com/r/openwrt/comments/11kqdi8/openwrt_beginner_guidetutorial/>
- Training and Certifications

---

## 🧠 How OpenWrt Differs from pfSense

Since you use pfSense:

| Feature             | OpenWrt            | pfSense            |
|:--------------------|:-------------------|:-------------------|
| Base                | Embedded Linux     | FreeBSD            |
| Target              | Routers            | Firewall appliance |
| Hardware            | Low power ARM/MIPS | x86 mainly         |
| Flexibility         | Very high          | High               |
| Enterprise features | Limited            | More built-in      |

OpenWrt is ideal for:

- Edge devices
- Travel routers
- Lab segmentation
- Lightweight branch routing

pfSense is better for:

- Heavy firewalling
- IDS/IPS (Suricata/Snort)
- Enterprise edge

---

## Use Cases

- OpenWRT for Home Networks
- OpenWRT in Business/Enterprise Environments
- Use of OpenWRT in IoT (Internet of Things)
- OpenWRT as a VPN Router

### 🔬 Common Advanced Use Cases

- 📡 Wireless mesh (802.11s)
- 🌍 Captive portal (CoovaChilli)
- 🔐 WireGuard road-warrior setup
- 📊 SNMP monitoring
- 📈 Traffic shaping with SQM (excellent for bufferbloat)
- 🔄 VLAN trunk to managed switch
- 🔥 Lab segmentation gateway
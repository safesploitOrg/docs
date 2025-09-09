# 🔒 nftables Best Practices

Unlike iptables, nftables supports modern abstractions and cleaner syntax, making firewall rules more scalable, readable, and maintainable.  
This guide outlines recommended practices when building rulesets.

---

## 🗂 Organisation & Structure

- **Use tables and chains consistently**  
  - Keep separate tables for `inet` (IPv4+IPv6 combined), `ip`, and `ip6` only when necessary.  
  - Example:
    ```bash
    table inet filter {
        chain input {
            type filter hook input priority 0;
        }
    }
    ```

- **Combine IPv4 + IPv6 rules**  
  - Prefer `inet` family tables instead of duplicating rules for `ip` and `ip6`.


## 👥 Groups & Sets

- **Use sets for IP groups** (replaces iptables `ipset`)  
  - Easier to manage hosts/networks without duplicating rules.  
  - Example: block a group of hostile IPs
    ```bash
    set blacklist {
        type ipv4_addr;
        elements = { 
            192.168.10.5, 
            192.168.20.0/24 
        }
    }

    chain input {
        type filter hook input priority 0;
        ip saddr @blacklist drop
    }
    ```

- **Use sets for ports and services**  
  - Simplify multi-service allow/deny rules.  
  - Example: allow standard web ports
    ```bash
    set web_ports {
        type inet_service;
        elements = { 80, 443 }
    }

    chain input {
        tcp dport @web_ports accept
    }
    ```


## 🧩 Reusability & Abstraction

- **Name chains by purpose** (`input`, `forward`, `output`, `log_drop`).  
- **Split rules logically** (e.g., base policy, user-defined services, logging).  
- Example: logging chain  
  ```bash
  chain log_drop {
      log prefix "NFT DROP: " flags all
      drop
  }
  ```


## 🔐 Security-Oriented Defaults

- **Default deny**: always end chains with `drop`/`reject` unless explicitly allowed.
- **Log before dropping** sensitive traffic to detect probing.
- **Restrict administrative ports** (SSH, RDP, VPN) to trusted IP sets.
- Use **rate limits** on logging and SSH attempts:
    ```bash
    limit rate 5/minute accept
    ```


## ⚡ Performance & Maintainability

- Prefer **sets** over many individual rules (nftables uses maps/intervals internally, faster at scale).
- Keep ruleset in a single file (`/etc/sysconfig/nftables.conf`) under version control (e.g., Git).
 - Use **comments** generously in rules for future admins.

## 🧪 Testing & Validation

- Test changes with:
    ```bash
    nft -f new_rules.conf
    nft list ruleset
    ```
- Stage complex changes on non-production first.
- Keep a **console session open** when applying new rules in case of lockout.

---

## 👨‍💻 Example: IT Hosts with Multi-Line Sets

This example allows IT hosts to reach administrative and web services:  

```yaml
table inet filter {
    # IT hosts allowed to access sensitive services
    set it_hosts {
        type ipv4_addr;
        elements = {
            172.16.80.10,  # IT-010
            172.16.80.11,  # IT-011
            172.16.80.12   # IT-012
        }
    }

    # Common IT service ports
    set it_ports {
        type inet_service;
        elements = {
            22,      # SSH
            3389,    # RDP
            80,      # HTTP
            443      # HTTPS
        }
    }

    chain input {
        type filter hook input priority 0;

        # allow loopback
        iif lo accept

        # allow established/related connections
        ct state established,related accept

        # allow IT hosts on specific ports
        ip saddr @it_hosts tcp dport @it_ports accept

        # drop everything else with logging
        jump log_drop
    }

    chain log_drop {
        log prefix "NFT DROP: " flags all
        drop
    }
}
```
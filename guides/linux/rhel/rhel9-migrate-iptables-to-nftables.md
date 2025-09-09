## **Overview - RHEL9: Migrate from iptables to nftables**

- RHEL 9 uses `nftables` as the default backend for the firewall.
- `iptables` commands in RHEL 9 are actually wrappers around `nftables` (`iptables-nft`) or the legacy backend (`iptables-legacy`), depending on installation.
- Direct migration ensures existing firewall rules are preserved while moving to a modern, unified syntax.

----------

## **1. Check Current iptables Setup**

```
sudo iptables-save > ~/iptables.rules 
sudo ip6tables-save > ~/ip6tables.rules
```

- This exports all IPv4/IPv6 rules.
- **Inspect** them for custom chains or scripts you need to port manually.

> (Optional) Check which iptables version your system uses:

```bash
sudo alternatives --display iptables`
```

You should see something like:

`iptables - manual mode link currently points to /usr/sbin/iptables-nft`

- If it points to `iptables-legacy`, switching is recommended.

----------

## **2. Install nftables (if not already installed)**

```bash
sudo dnf install nftables -y 
sudo systemctl enable --now nftables
```

- This starts and enables the nftables service.
- Rules are stored in `/etc/nftables/` or `/etc/sysconfig/nftables.conf` depending on RHEL version.

----------

## **3. Convert iptables Rules to nftables**

RHEL 9 provides a script `iptables-translate` to convert rules:

```bash
sudo iptables-restore-translate -f ~/iptables.rules > ~/nftables.rules 
sudo ip6tables-restore-translate -f ~/ip6tables.rules >> ~/nftables.rules
```

- This produces a combined `nftables` syntax file.
- **Important:** Review the file carefully — some complex chains may need manual adjustments.

----------

## **4. (Optional) Test nftables Rules**

Before applying permanently:

```bash
sudo nft -f ~/nftables.rules
```

- Check current nftables state:

```bash
sudo nft list ruleset
```

- Test connectivity (SSH, web, VPN, etc.) to make sure nothing breaks.

----------

## **5. Persist nftables Rules**

```bash
sudo cp ~/nftables.rules /etc/sysconfig/nftables.conf 
sudo systemctl enable --now nftables
```

> Apply the Changes

```bash
sudo systemctl restart nftables
```

----------

## **6. Disable iptables Service**

To avoid conflicts:

```bash
sudo systemctl stop iptables ip6tables 
sudo systemctl disable iptables ip6tables
```

- Confirm nftables is handling firewall rules:

```bash
sudo nft list ruleset
```

----------

## **7. (Optional) Switch iptables to NFT backend**

- Even after migration, you can keep using `iptables` commands but backed by `nftables`:

```bash
sudo alternatives --set iptables /usr/sbin/iptables-nft 
sudo alternatives --set ip6tables /usr/sbin/ip6tables-nft
```

- This ensures compatibility with scripts that still call `iptables`.

----------

### ✅ **Key Tips**

- Always **backup original iptables rules** before migration.
- Test **rule-by-rule** on a staging host if possible.
- Use `nft list ruleset` frequently to verify rule loading.
- Avoid mixing `iptables-legacy` and `nftables` — choose one backend to prevent conflicts.
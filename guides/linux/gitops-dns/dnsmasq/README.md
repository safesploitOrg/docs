# GitOps for Homelab DNS (Dnsmasq)

- [Why GitOps?](#why-gitops)
- [🚀 Installation & Initial Configuration](#installation-initial-configuration)
- [🖋 Writing Hostnames](#writing-hostnames)
- [🔄 GitOps Workflow](#gitops-workflow)
- [🔄 Bash Sync Script & Cronjob](#bash-sync-script-cronjob)
- [🔄 (Optional) GitHub Actions CI Validation](#optional-github-actions-ci-validation)
- [Visual DNS Flow](#visual-dns-flow)
- [💡 Benefits & Considerations](#benefits-considerations)

---

## Why GitOps?

⚡ It started as a simple typo in `/etc/hosts`. One wrong hostname. One overlooked IP.

In an instant, my **homelab descended into chaos**:

- My **Proxmox cluster** stopped resolving nodes.
- The **Ceph distributed storage** went offline.
- Every **LXC container and VM** froze or failed to start.

It was a domino effect: a tiny DNS misconfiguration brought down my entire lab environment.

That’s when I realised: **manual DNS editing was a ticking time bomb**.

Enter **GitOps for DNS** - a workflow that stores every host entry in a repo under version control, automates deployment, and ensures a single source of truth.   
No more human error. No more cascading failures.

---

## Introduction

In this guide, we’ll implement **GitOps-style DNS** using **dnsmasq**, **GitHub**, **Bash**, and a **cronjob** - making your homelab DNS predictable, maintainable, and secure.

Deploy keys (SSH keys) are used to secure repository access, ensuring only your DNS server can pull updates.

---

### 🛠 Benefits of a GitOps DNS Workflow

- 🔄 **Automated sync** – Changes in Git automatically update the DNS server
- 🗂 **Version-controlled hosts** – Every edit is tracked with commit history
- 🛡 **Security-conscious** – Deploy keys and configuration validation reduce risk
- 🧩 **Modular & maintainable** – Split hosts into `.cfg` files for easier management
- ✅ Integrate **dnsmasq** with **GitHub Actions** for automated validation

---

## 🚀 Installation & Initial Configuration

### **1. Install dnsmasq and Git**

```bash
sudo yum install -y dnsmasq git       # RHEL/CentOS/AlmaLinux
sudo apt install -y dnsmasq git       # Debian/Ubuntu
```

---

### **2. Configure dnsmasq**

Create a config file in `/etc/dnsmasq.d/`:

> /etc/dnsmasq.d/000-base.conf

```bash
domain=safesploit.com
expand-hosts

log-queries
no-hosts
addn-hosts=/etc/hosts.d

listen-address=172.16.5.27
```

> 📝 **Tip:** Always bind dnsmasq to a specific NIC (`listen-address`)
>
> ⚠️ using `0.0.0.0` is **not supported**.   
> Otherwise, dnsmasq will only respond on `127.0.0.1`.( 

---

### 3. Prepare `/etc/hosts.d/` (Optional, Modular Setup)

```bash
sudo mkdir -p /etc/hosts.d
sudo touch /etc/hosts.d/000-network.cfg
# sudo touch /etc/hosts.d/XXX-*.cfg  # placeholder files
```

---

### **4. Enable & start service**

```bash
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq
```

Now dnsmasq is ready to resolve hostnames from `/etc/hosts.d/`.

### **5. (Optional) Test after starting dnsmasq**

Use `dig @<DNS Server IP> <DNS Entry>` to query:

```bash
dig @172.16.5.27 ldap.safesploit.com +short
```

This gives proof it works

---

## 🖋 Writing Hostnames

Add new `.cfg` files to `/etc/hosts.d/` following a consistent naming scheme like `XXX-<subnet_name>.cfg`:

- `005-critical-prod.cfg` → critical production hosts
- `081-mgmt.cfg` → management network
- `100-storage.cfg` → storage servers

---

### Example hostnames

Each `.cfg` file contains simple `IP hostname` mappings (just like `/etc/hosts`):

```bash
172.16.5.10       ldap
```

```bash
172.16.100.10      nas1
```

✅ This modular approach makes it **easy to version control, review, and expand**.

---

## 🔄 GitOps Workflow

> Assumed Knowledge: that you already know how to [create a GitHub repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).

### **1. Repository Structure**

```bash
.dns-configs/
└── dnsmasq/
    └── hosts.d/
        ├── 005-critical-prod.cfg
        ├── 081-mgmt.cfg
        ├── 100-storage.cfg
        └── XXX-*.cfg
```

### **2. Secure Access with Deploy Keys**

- Generate an SSH key for the DNS server:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_github_ed25519
```

- Add the public key to your GitHub repository’s **Deploy Keys** with **read-only access**.
- GitHub Docs: [Managing Deploy Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys#set-up-deploy-keys)

### **3. Workflow Steps**

- Detect changes on `main`
- Clone repo
- Sync `/etc/hosts.d/` via `rsync`
- Restart `dnsmasq`
- Record applied commit hash

> ⚠️ **Warning:** Validate configs before restart:
>
> ```bash
> dnsmasq --test
> systemctl restart dnsmasq
> ```

---

## 🔄 Bash Sync Script & Cronjob

DNS GitOps Script:

> ⚠️ Make sure you adjust these for your setup
>
> - REPO="dns-configs"
> - OWNER="github\_org/username"
> - GITHUB\_DEPLOY\_KEY="${HOME}/.ssh/id\_github\_ed25519"

### Bash Script

The script handles:

- SSH agent setup
- Change detection via commit hash
- Cloning and syncing `/etc/hosts.d/`
- Restarting dnsmasq
- Logging and optional quiet mode


[Git Clone Bash Script - git_clone_dns_configs_dnsmasq.sh](https://raw.githubusercontent.com/safesploitOrg/assets/main/repo/dev.to/gitops-dns-dnsmasq/git_clone_dns_configs_dnsmasq.sh)


---

### Cronjob (every 5 minutes):

```bash
*/5 * * * * /root/git_clone_dnsmasq.sh
```

> 🔧 Automatic updates reduce errors and maintain consistency.

---

## 🔄 (Optional) GitHub Actions CI Validation

At this point, the DNS server can pull host updates from Git.

However, blindly syncing DNS records from Git is risky. A bad hosts entry, duplicate hostname, or broken dnsmasq config could break DNS resolution.

To reduce that risk, I added a GitHub Actions workflow that validates the dnsmasq configuration before changes are accepted.

---

### CI Validation

| CI check | Reason |
|---|---|
| Runs inside AlmaLinux 10 | Matches the RHEL-style target environment |
| Installs real `dnsmasq` service | Validates against the actual service |
| Copies `dnsmasq.d` and `hosts.d` | Tests realistic file layout |
| Validates host format | Catches malformed records |
| Detects duplicate hostnames | Prevents ambiguous DNS |
| Creates CI-safe config | Avoids binding to homelab-only IPs in CI |
| Starts dnsmasq on `127.0.0.1:5353` | Tests real resolution safely |
| Uses `dig` tests | Proves records actually resolve |

---

### GitHub Actions workflow

[GitHub Actions CI Dnsmasq - dnsmasq-ci.yml](https://raw.githubusercontent.com/safesploitOrg/assets/main/repo/dev.to/gitops-dns-dnsmasq/dnsmasq-ci.yml)


---

## Visual DNS Flow

```text
   [Client Request] 
          |
          v
   [DNS (dnsmasq)]
          |
    ┌─────┴─────┐
    v           v
[Local hosts]  [Upstream DNS]
```

> 🖼 Shows decision flow for DNS resolution.

---

## 💡 Benefits & Considerations

### **Benefits:**

- ✅ Version-controlled DNS (rollback capable)
- ✅ Modular and maintainable
- ✅ Automatic sync reduces human error
- ✅ CI/CD guardrails for DNS

### **Security Notes:**

- 🔑 Protect deploy keys (`chmod 600 ~/.ssh/id_github_ed25519`)
- 🔍 Validate dnsmasq configs before restart
- ⚠️ Be careful with `rsync --delete` — deletions in Git remove files on server

---

## 🔜 Next Steps / Future Improvements

- ✅ Integrate **dnsmasq** with **GitHub Actions** for automated validation
- ✅ Add **linting / syntax checks** for host files
- Support **multiple domains** or overlay networks
- Consider **BIND migration** for more advanced DNS features

---

## Conclusion

GitOps makes your homelab DNS:

- **Predictable** – every change tracked
- **Secure** – deploy keys and validation
- **Maintainable** – modular files and automation

You now have a **fully automated, version-controlled DNS workflow** for your homelab.
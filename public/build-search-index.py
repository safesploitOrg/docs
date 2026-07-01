#!/usr/bin/env python3

"""
Generate a static JSON search index for the safesploitOrg/docs GitHub Pages site.

This script scans Markdown files in the repository and outputs:

    public/search-index.json

The generated index is consumed by:

    public/assets/js/search.js

Design goals:
- Works in GitHub Actions
- No external Python dependencies
- Skips hidden/system/vendor/build folders
- Avoids indexing ./public itself
- Produces browser-friendly JSON
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


# =============================================================================
# GLOBAL VARS
# =============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = REPO_ROOT / "public"
OUTPUT_FILE = PUBLIC_DIR / "search-index.json"

MARKDOWN_EXTENSIONS = {".md", ".markdown"}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    "node_modules",
    "vendor",
    "public",
    "dist",
    "build",
    ".venv",
    "venv",
}

EXCLUDED_FILES = {
    "LICENSE",
}

MAX_CONTENT_CHARS = 12000

# DEFAULT_TAGS_BY_PATH = {
#     "dns": ["DNS"],
#     "bind": ["BIND", "DNS"],
#     "dnsmasq": ["dnsmasq", "DNS"],
#     "redcap": ["REDCap"],
#     "linux": ["Linux"],
#     "rhel": ["RHEL", "Linux"],
#     "ansible": ["Ansible", "Automation"],
#     "terraform": ["Terraform", "IaC"],
#     "github": ["GitHub"],
#     "gitops": ["GitOps"],
#     "ci": ["CI/CD"],
#     "cicd": ["CI/CD"],
#     "security": ["Security"],
#     "hardening": ["Hardening", "Security"],
#     "netapp": ["NetApp", "ONTAP", "Storage"],
#     "ontap": ["ONTAP", "NetApp"],
#     "storage": ["Storage"],
#     "proxmox": ["Proxmox", "Virtualisation"],
#     "ceph": ["Ceph", "Storage"],
#     "network": ["Networking"],
#     "runbook": ["Runbook"],
#     "architecture": ["Architecture"],
#     "compliance": ["Compliance"],
# }

DEFAULT_TAGS_BY_PATH = {
    # =========================================================================
    # CONFLUENCE SPACES / TOP-LEVEL KNOWLEDGE AREAS
    # =========================================================================

    "devops": ["DevOps"],
    "devsecops": ["DevSecOps", "Security"],
    "itsys": ["Systems", "Infrastructure"],
    "itnet": ["Networking"],
    "itsec": ["Security"],
    "it management": ["IT Management", "Governance"],
    "it data centre": ["Data Centre", "Operations"],
    "dcops": ["Data Centre", "Operations"],
    "it service desk": ["Service Desk", "Support"],
    "itsd": ["Service Desk", "Support"],
    "it support": ["Support", "Endpoint"],

    # =========================================================================
    # HOMELAB / PORTFOLIO
    # =========================================================================

    "homelab": ["Homelab", "Infrastructure"],
    "portfolio": ["Portfolio"],
    "safesploit": ["Portfolio", "safesploit"],
    "sws": ["safesploit", "Homelab"],
    "project": ["Project"],
    "projects": ["Projects"],
    "architecture": ["Architecture"],
    "runbook": ["Runbook"],
    "runbooks": ["Runbook"],
    "template": ["Template"],
    "decision": ["Decision Record"],
    "adr": ["ADR", "Architecture"],

    # =========================================================================
    # DEVOPS / PLATFORM ENGINEERING
    # =========================================================================

    "ci_cd": ["CI/CD"],
    "ci-cd": ["CI/CD"],
    "cicd": ["CI/CD"],
    "continuous integration": ["CI"],
    "continuous delivery": ["CD"],
    "continuous deployment": ["CD"],
    "github actions": ["GitHub Actions", "CI/CD"],
    "github pages": ["GitHub Pages", "Static Site"],
    "github": ["GitHub"],
    "gitlab": ["GitLab"],
    "gitlabs": ["GitLab"],
    "git": ["Git"],
    "gitops": ["GitOps"],
    "argocd": ["Argo CD", "GitOps"],
    "argo cd": ["Argo CD", "GitOps"],
    "jenkins": ["Jenkins", "CI/CD"],
    "deployment": ["Deployment"],
    "deployment orchestration": ["Deployment", "Orchestration"],
    "blue-green": ["Deployment Strategy"],
    "canary": ["Deployment Strategy"],
    "sdlc": ["SDLC"],
    "secure sdlc": ["Secure SDLC", "Security"],
    "shift left": ["Shift Left", "Security"],
    "sbom": ["SBOM", "Supply Chain Security"],
    "dry code": ["DRY", "Software Engineering"],

    # =========================================================================
    # INFRASTRUCTURE AS CODE / AUTOMATION
    # =========================================================================

    "automation": ["Automation"],
    "configuration management": ["Configuration Management"],
    "configuration drift": ["Drift Detection", "Configuration Management"],
    "ansible": ["Ansible", "Automation"],
    "ansible vault": ["Ansible", "Secrets"],
    "jinja2": ["Jinja2", "Templating"],
    "terraform": ["Terraform", "IaC"],
    "pulumi": ["Pulumi", "IaC"],
    "packer": ["Packer", "Image Build"],
    "iac": ["IaC"],
    "compliance as code": ["Compliance as Code"],
    "policy as code": ["Policy as Code"],
    "cac": ["Compliance as Code"],
    "pac": ["Policy as Code"],

    # =========================================================================
    # CLOUD
    # =========================================================================

    "cloud": ["Cloud"],
    "aws": ["AWS", "Cloud"],
    "amazon web services": ["AWS", "Cloud"],
    "ec2": ["AWS", "Compute"],
    "lambda": ["AWS", "Serverless"],
    "rds": ["AWS", "Database"],
    "aurora": ["AWS", "Database"],
    "dynamodb": ["AWS", "Database"],
    "s3": ["AWS", "Storage"],
    "ebs": ["AWS", "Storage"],
    "efs": ["AWS", "Storage"],
    "fsx": ["AWS", "Storage"],
    "vpc": ["AWS", "Networking"],
    "iam": ["IAM", "Security"],
    "kms": ["KMS", "Encryption"],
    "guardduty": ["AWS", "Security"],
    "security hub": ["AWS", "Security"],
    "cloudtrail": ["AWS", "Audit"],
    "cloudwatch": ["AWS", "Monitoring"],
    "route 53": ["AWS", "DNS"],
    "waf": ["WAF", "Security"],
    "azure": ["Azure", "Cloud"],
    "entra": ["Azure", "Identity"],
    "azuread": ["Azure", "Identity"],
    "intune": ["Intune", "Endpoint Management"],
    "gcp": ["GCP", "Cloud"],

    # =========================================================================
    # CONTAINERS / ORCHESTRATION
    # =========================================================================

    "container": ["Containers"],
    "containerisation": ["Containers"],
    "docker": ["Docker", "Containers"],
    "docker compose": ["Docker Compose", "Containers"],
    "podman": ["Podman", "Containers"],
    "lxc": ["LXC", "Containers"],
    "kubernetes": ["Kubernetes", "Containers"],
    "k8s": ["Kubernetes", "Containers"],
    "k3s": ["K3s", "Kubernetes"],
    "eks": ["AWS", "Kubernetes"],
    "ecs": ["AWS", "Containers"],
    "fargate": ["AWS", "Containers"],
    "openshift": ["OpenShift", "Kubernetes"],
    "helm": ["Helm", "Kubernetes"],
    "rook-ceph": ["Ceph", "Kubernetes"],
    "csi": ["CSI", "Storage"],
    "rbac": ["RBAC", "Security"],

    # =========================================================================
    # SYSTEMS / LINUX / WINDOWS / ENDPOINT
    # =========================================================================

    "linux": ["Linux"],
    "rhel": ["RHEL", "Linux"],
    "red hat": ["RHEL", "Linux"],
    "almalinux": ["AlmaLinux", "Linux"],
    "ubuntu": ["Ubuntu", "Linux"],
    "debian": ["Debian", "Linux"],
    "systemd": ["systemd", "Linux"],
    "selinux": ["SELinux", "Hardening"],
    "apparmor": ["AppArmor", "Hardening"],
    "windows": ["Windows"],
    "windows 11": ["Windows 11", "Endpoint"],
    "rdp": ["RDP", "Remote Access"],
    "bitlocker": ["BitLocker", "Endpoint Security"],
    "macos": ["macOS", "Endpoint"],
    "brew": ["Homebrew", "macOS"],
    "ssh": ["SSH", "Remote Access"],
    "remote ssh": ["SSH", "Remote Access"],

    # =========================================================================
    # NETWORKING
    # =========================================================================

    "network": ["Networking"],
    "networking": ["Networking"],
    "vlan": ["VLAN", "Networking"],
    "vxlan": ["VXLAN", "Networking"],
    "dmz": ["DMZ", "Networking"],
    "subnet": ["Subnetting", "Networking"],
    "routing": ["Routing", "Networking"],
    "inter-vlan": ["Inter-VLAN Routing", "Networking"],
    "firewall": ["Firewall", "Security"],
    "vpn": ["VPN", "Remote Access"],
    "wireguard": ["WireGuard", "VPN"],
    "netbird": ["NetBird", "VPN"],
    "tailscale": ["Tailscale", "VPN"],
    "twingate": ["Twingate", "ZTNA"],
    "openwrt": ["OpenWRT", "Networking"],
    "pfsense": ["pfSense", "Firewall"],
    "gl.inet": ["GL.iNet", "Networking"],
    "axt1800": ["GL.iNet", "Router"],
    "dns": ["DNS", "Networking"],
    "bind": ["BIND", "DNS"],
    "dnsmasq": ["dnsmasq", "DNS"],
    "dhcp": ["DHCP", "Networking"],
    "arp": ["ARP", "Networking"],
    "stp": ["STP", "Switching"],
    "bgp": ["BGP", "Routing"],
    "ospf": ["OSPF", "Routing"],
    "vrrp": ["VRRP", "Networking"],
    "snmp": ["SNMP", "Monitoring"],
    "lldp": ["LLDP", "Networking"],
    "lacp": ["LACP", "Switching"],
    "lag": ["LAG", "Switching"],
    "wi-fi": ["Wi-Fi", "Networking"],
    "wifi": ["Wi-Fi", "Networking"],
    "802.1x": ["802.1X", "Network Security"],
    "radius": ["RADIUS", "Authentication"],
    "netgear": ["Netgear", "Switching"],
    "gs108tv3": ["Netgear GS108Tv3", "Switching"],
    "cisco": ["Cisco", "Networking"],
    "tp-link": ["TP-Link", "Networking"],

    # =========================================================================
    # VIRTUALISATION / STORAGE / DATA CENTRE
    # =========================================================================

    "virtualisation": ["Virtualisation"],
    "virtualization": ["Virtualisation"],
    "proxmox": ["Proxmox", "Virtualisation"],
    "pve": ["Proxmox", "Virtualisation"],
    "ceph": ["Ceph", "Storage"],
    "vmware": ["VMware", "Virtualisation"],
    "storage": ["Storage"],
    "nas": ["NAS", "Storage"],
    "san": ["SAN", "Storage"],
    "nfs": ["NFS", "Storage"],
    "smb": ["SMB", "Storage"],
    "cifs": ["SMB", "Storage"],
    "netapp": ["NetApp", "Storage"],
    "ontap": ["ONTAP", "NetApp"],
    "lun": ["LUN", "Storage"],
    "fibre channel": ["Fibre Channel", "SAN"],
    "fcoe": ["FCoE", "SAN"],
    "wwpn": ["WWPN", "SAN"],
    "multipath": ["Multipath", "Storage"],
    "mpio": ["MPIO", "Storage"],
    "xfs": ["XFS", "Linux Storage"],
    "lvm": ["LVM", "Linux Storage"],
    "data centre": ["Data Centre"],
    "dcim": ["DCIM", "Data Centre"],
    "ups": ["UPS", "Power"],
    "pdu": ["PDU", "Power"],
    "cooling": ["Cooling", "Data Centre"],
    "fire suppression": ["Fire Suppression", "Data Centre"],

    # =========================================================================
    # SECURITY / DEVSECOPS / CYBER
    # =========================================================================

    "security": ["Security"],
    "hardening": ["Hardening", "Security"],
    "zero trust": ["Zero Trust", "Security"],
    "least privilege": ["Least Privilege", "Security"],
    "cybersecurity": ["Cybersecurity"],
    "dfir": ["DFIR", "Incident Response"],
    "incident response": ["Incident Response"],
    "ioc": ["IoC", "Threat Intelligence"],
    "threat intelligence": ["Threat Intelligence"],
    "mitre": ["MITRE ATT&CK", "Security"],
    "attack": ["MITRE ATT&CK", "Security"],
    "vulnerability": ["Vulnerability Management"],
    "vulnerability scanner": ["Vulnerability Scanner"],
    "nessus": ["Nessus", "Vulnerability Management"],
    "qualys": ["Qualys", "Vulnerability Management"],
    "wazuh": ["Wazuh", "SIEM"],
    "ossec": ["OSSEC", "SIEM"],
    "siem": ["SIEM", "Security Monitoring"],
    "xdr": ["XDR", "Security"],
    "edr": ["EDR", "Endpoint Security"],
    "ndr": ["NDR", "Network Security"],
    "ids": ["IDS", "Detection"],
    "ips": ["IPS", "Prevention"],
    "falco": ["Falco", "Runtime Security"],
    "arkime": ["Arkime", "Packet Capture"],
    "darktrace": ["Darktrace", "NDR"],
    "microsoft defender": ["Microsoft Defender", "Endpoint Security"],
    "modsecurity": ["ModSecurity", "WAF"],

    # =========================================================================
    # IDENTITY / ACCESS / COMPLIANCE / GOVERNANCE
    # =========================================================================

    "identity": ["Identity"],
    "authentication": ["Authentication"],
    "authorisation": ["Authorisation"],
    "authorization": ["Authorisation"],
    "sso": ["SSO", "Identity"],
    "saml": ["SAML", "Identity"],
    "oidc": ["OIDC", "Identity"],
    "oauth": ["OAuth", "Identity"],
    "ldap": ["LDAP", "Identity"],
    "freeipa": ["FreeIPA", "Identity"],
    "active directory": ["Active Directory", "Identity"],
    "ad": ["Active Directory", "Identity"],
    "entra id": ["Entra ID", "Identity"],
    "iam": ["IAM", "Identity"],
    "pam": ["PAM", "Privileged Access"],
    "compliance": ["Compliance"],
    "governance": ["Governance"],
    "gdpr": ["GDPR", "Compliance"],
    "data protection": ["Data Protection", "Compliance"],
    "dpa2018": ["Data Protection Act 2018", "Compliance"],
    "iso 27001": ["ISO 27001", "Compliance"],
    "cyber essentials": ["Cyber Essentials", "Compliance"],
    "cyber essentials plus": ["Cyber Essentials Plus", "Compliance"],
    "ncsc": ["NCSC", "Security"],
    "prevent": ["PREVENT", "Compliance"],
    "aup": ["Acceptable Use Policy", "Governance"],
    "fup": ["Fair Use Policy", "Governance"],
    "document classification": ["Document Classification", "Governance"],

    # =========================================================================
    # OBSERVABILITY / MONITORING
    # =========================================================================

    "observability": ["Observability"],
    "monitoring": ["Monitoring"],
    "metrics": ["Metrics"],
    "logs": ["Logs"],
    "traces": ["Traces"],
    "grafana": ["Grafana", "Observability"],
    "prometheus": ["Prometheus", "Monitoring"],
    "promql": ["PromQL", "Prometheus"],
    "alertmanager": ["Alertmanager", "Prometheus"],
    "opentelemetry": ["OpenTelemetry", "Observability"],
    "datadog": ["Datadog", "Monitoring"],
    "new relic": ["New Relic", "Monitoring"],
    "elk": ["ELK", "Logging"],
    "checkmk": ["CheckMK", "Monitoring"],
    "nagios": ["Nagios", "Monitoring"],
    "nagstamon": ["Nagstamon", "Monitoring"],
    "diun": ["DIUN", "Container Monitoring"],

    # =========================================================================
    # ITSM / MANAGEMENT / SERVICE CONTINUITY
    # =========================================================================

    "itsm": ["ITSM"],
    "itil": ["ITIL"],
    "incident management": ["Incident Management"],
    "problem management": ["Problem Management"],
    "change management": ["Change Management"],
    "change advisory board": ["CAB", "Change Management"],
    "cab": ["CAB", "Change Management"],
    "change freeze": ["Change Freeze", "Change Management"],
    "postmortem": ["Postmortem", "Incident Management"],
    "rca": ["RCA", "Incident Management"],
    "sla": ["SLA", "Service Management"],
    "slas": ["SLA", "Service Management"],
    "bcm": ["Business Continuity", "ITSCM"],
    "bcp": ["BCP", "Business Continuity"],
    "drp": ["DRP", "Disaster Recovery"],
    "bia": ["BIA", "Business Continuity"],
    "service continuity": ["ITSCM", "Business Continuity"],
    "itom": ["ITOM", "Operations"],
    "bau": ["BAU", "Operations"],
    "technical debt": ["Technical Debt"],
    "target operating model": ["Target Operating Model"],
    "standard operating model": ["Operating Model"],
    "mou": ["MoU", "Governance"],
    "pmo": ["PMO", "Project Management"],
    "smart objective": ["SMART Objectives"],
    "star": ["STAR", "Career"],
    "swot": ["SWOT", "Career"],

    # =========================================================================
    # APPLICATIONS / SERVICES
    # =========================================================================

    "redcap": ["REDCap", "Application"],
    "bookstack": ["BookStack", "Documentation"],
    "guacamole": ["Guacamole", "Remote Access"],
    "apache": ["Apache", "Web Server"],
    "httpd": ["Apache", "Web Server"],
    "nginx": ["NGINX", "Web Server"],
    "php": ["PHP", "Application Stack"],
    "mariadb": ["MariaDB", "Database"],
    "mysql": ["MySQL", "Database"],
    "postgresql": ["PostgreSQL", "Database"],
    "prisma": ["Prisma", "ORM"],
    "tomcat": ["Tomcat", "Application Server"],

    # =========================================================================
    # SUPPORT / END USER / VENDOR KB
    # =========================================================================

    "microsoft teams": ["Microsoft Teams", "Support"],
    "teams": ["Microsoft Teams", "Support"],
    "chrome": ["Chrome", "Support"],
    "vs code": ["VS Code", "Support"],
    "vscode": ["VS Code", "Support"],
    "slack": ["Slack", "Support"],
    "linkedin": ["LinkedIn", "Support"],
    "1password": ["1Password", "Security"],
    "hpe": ["HPE", "Hardware"],
    "hp": ["HP", "Hardware"],
    "minisforum": ["Minisforum", "Hardware"],
    "mobaXterm": ["MobaXterm", "Support"],
    "hiren": ["Hiren BootCD", "Support"],
}


# =============================================================================
# TEXT HELPERS
# =============================================================================

def normalise_whitespace(value: str) -> str:
    """Collapse repeated whitespace into single spaces."""
    return re.sub(r"\s+", " ", value).strip()


def strip_markdown(value: str) -> str:
    """Make Markdown content more search/snippet friendly."""
    text = value

    # Remove fenced code block markers but keep code contents searchable.
    text = re.sub(r"```[a-zA-Z0-9_-]*", " ", text)
    text = text.replace("```", " ")

    # Remove inline code backticks but keep content.
    text = text.replace("`", "")

    # Remove Markdown links while preserving readable text and URL signal.
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 \2", text)

    # Remove image syntax while preserving alt text.
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)

    # Remove common Markdown formatting characters.
    text = re.sub(r"[*_~>#|]", " ", text)

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    return normalise_whitespace(text)


def extract_title(markdown_text: str, fallback: str) -> str:
    """Extract the first H1/H2-style heading, otherwise use filename stem."""
    for line in markdown_text.splitlines():
        clean_line = line.strip()

        if clean_line.startswith("#"):
            title = clean_line.lstrip("#").strip()
            if title:
                return title

    return fallback.replace("-", " ").replace("_", " ").title()


def extract_headings(markdown_text: str) -> List[str]:
    """Extract Markdown headings for extra searchable context."""
    headings: List[str] = []

    for line in markdown_text.splitlines():
        clean_line = line.strip()

        if clean_line.startswith("#"):
            heading = clean_line.lstrip("#").strip()
            if heading:
                headings.append(heading)

    return headings


def slugify(value: str) -> str:
    """Create a simple slug for fallback URLs."""
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "document"


# =============================================================================
# INDEX HELPERS
# =============================================================================

def should_exclude_path(path: Path) -> bool:
    """Return True if the file should not be indexed."""
    relative_parts = path.relative_to(REPO_ROOT).parts

    for part in relative_parts:
        if part in EXCLUDED_DIRS:
            return True

        if part.startswith(".") and part not in {".well-known"}:
            return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.suffix.lower() not in MARKDOWN_EXTENSIONS:
        return True

    return False


def infer_tags(relative_path: Path, title: str, content: str) -> List[str]:
    """Infer lightweight tags from path, title and content."""
    discovered_tags: List[str] = []

    searchable = " ".join(
        [
            str(relative_path).lower(),
            title.lower(),
            content[:3000].lower(),
        ]
    )

    for keyword, tags in DEFAULT_TAGS_BY_PATH.items():
        if keyword in searchable:
            for tag in tags:
                if tag not in discovered_tags:
                    discovered_tags.append(tag)

    return discovered_tags[:8]


def build_github_url(relative_path: Path) -> str:
    """
    Link result cards back to the source file in GitHub.

    This avoids needing to convert every Markdown file into an HTML page.
    """
    path_posix = relative_path.as_posix()
    return f"https://github.com/safesploitOrg/docs/blob/main/{path_posix}"


def build_index_item(path: Path) -> Dict[str, object]:
    """Build a single search-index item from a Markdown file."""
    relative_path = path.relative_to(REPO_ROOT)

    markdown_text = path.read_text(encoding="utf-8", errors="replace")
    title = extract_title(markdown_text, path.stem)

    headings = extract_headings(markdown_text)
    stripped_content = strip_markdown(markdown_text)

    if len(stripped_content) > MAX_CONTENT_CHARS:
        stripped_content = stripped_content[:MAX_CONTENT_CHARS].rstrip() + "..."

    tags = infer_tags(relative_path, title, stripped_content)

    content_parts = [
        title,
        " ".join(headings),
        stripped_content,
    ]

    return {
        "title": title,
        "path": relative_path.as_posix(),
        "url": build_github_url(relative_path),
        "tags": tags,
        "content": normalise_whitespace(" ".join(content_parts)),
    }


def discover_markdown_files() -> List[Path]:
    """Find all indexable Markdown files under the repository root."""
    markdown_files: List[Path] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if should_exclude_path(path):
            continue

        markdown_files.append(path)

    return sorted(markdown_files, key=lambda item: item.relative_to(REPO_ROOT).as_posix())


def write_search_index(index_items: List[Dict[str, object]]) -> None:
    """Write the search index JSON to ./public/search-index.json."""
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(index_items, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    markdown_files = discover_markdown_files()

    index_items = []

    for markdown_file in markdown_files:
        try:
            index_items.append(build_index_item(markdown_file))
        except Exception as error:
            relative_path = markdown_file.relative_to(REPO_ROOT)
            print(f"WARNING: Failed to index {relative_path}: {error}")

    write_search_index(index_items)

    print(f"Indexed {len(index_items)} Markdown files")
    print(f"Wrote {OUTPUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

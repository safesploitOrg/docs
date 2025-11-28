# Why Online Growth Is Safe for SAN (Fibre Channel), LVM2, and File System (XFS)

Modern enterprise Linux storage stacks are designed for **non-disruptive, online capacity expansion**, even while filesystems are mounted and under active I/O.  
This document explains why each layer—**SAN/FC, LVM2, and XFS**—fully supports this behaviour.

> ME4 LUN → dm-multipath → LVM2 (PV/VG/LV) → XFS/ext4

---

## 1. SAN / Fibre Channel (FC) – Non-Disruptive LUN Expansion

Modern enterprise SAN systems (such as **Dell EMC ME4**) support **live, nondisruptive LUN expansion**:

- Designed for **nondisruptive expansion**; brief I/O stalls may occur.
- No unmount or downtime  
- Host simply rescans the SCSI bus  
- Multipath handles updated path geometry automatically  

Dell’s ME4 Linux best-practices guide states:

> **“Resize tasks can be done online without disrupting the applications.”**  
**Source:**  
https://dl.dell.com/manuals/common/powervault-me4-and-linux-best-practices_en-us.pdf

After expanding the LUN, the host only needs a rescan:

```bash
rescan-scsi-bus.sh --resize
multipathd -k"resize map mpathX"
```

**Conclusion:**  
**SAN LUN expansion is explicitly engineered to occur online**, with no interruption to servers or I/O.

---

## 2. LVM2 – Online PV and LV Expansion (Safe While Mounted & Under I/O)

> ⚠️ Do not proceed unless all paths and the multipath device report the new size.

> Ensure the following report ALL paths are resized:
> ```bash
> multipath -ll mpathX
> blockdev --getsize64 /dev/sdX
> blockdev --getsize64 /dev/mapper/mpathX
> ```


### 2.1 PV Resize (`pvresize`) – Safe While Mounted

According to Red Hat’s LVM developers:

> **“`pvresize` simply updates the metadata to make LVM aware of the new size.”**  
> **“The data area does not change; only the PV extent map is updated.”**  
— Jonathan Brassow, Red Hat LVM developer  
**Source:**  
https://www.redhat.com/archives/linux-lvm/2009-May/msg00040.html

Because it modifies **only metadata**, `pvresize`:

- Does not touch data blocks  
- Does not affect the filesystem  
- Is safe under ongoing I/O
  - Provided the block device has been correctly resized on ALL paths 
- Is routinely run on **root filesystems**, which cannot be unmounted  

### Cloud vendor documentation confirming online PV resizing

All three major cloud providers document `pvresize` as part of their **“expand disk without downtime”** workflow:

- **AWS – Expand EBS volumes**  
  https://docs.aws.amazon.com/ebs/latest/userguide/recognize-expanded-volume-linux.html  
- **Google Cloud – Resize persistent disks**  
  https://cloud.google.com/compute/docs/disks/resize-persistent-disk  
- **Azure – Expand disks *without downtime***  
  https://learn.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks?tabs=ubuntu#expand-without-downtime  

These platforms are extremely conservative; documenting `pvresize` online means it is **fully safe and supported**.

**Conclusion:**  
`pvresize` is a **safe, online, non-disruptive** operation on modern LVM2.

---

### 2.2 LV Resize (`lvextend`) – Online and Atomic

`lvextend` updates:

- LVM metadata  
- device-mapper mappings  

These operations are:

- Atomic  
- Metadata is committed atomically via device-mapper table swap  
- Safe during active I/O  
- Non-disruptive to mounted filesystems  

Cloud vendors (AWS, GCP, Azure) all document `lvextend` as **online**, immediately after `pvresize`.

**Conclusion:**  
LVM2 PV and LV can be grown **online**, even during live writes, with no unmount required.

---

## 3. Online Filesystem Growth

After expanding the block device (SAN → PV → LV), the filesystem must grow to use the new space.  
Modern Linux filesystems support **online, mounted filesystem expansion**.

| Filesystem | Online Grow | Notes |
|-----------|--------------|-------|
| **XFS v4+** | ✔ | Designed for online growth; cannot shrink |
| **ext4** | ✔ | `resize2fs` supports online grow |

---

### 3.1 XFS – Designed for Online Filesystem Expansion

Red Hat’s official XFS documentation states:

> **“The filesystem must be mounted to be grown.”**  
**Source:**  
https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/storage_administration_guide/xfsgrow

This is one of the clearest vendor statements that XFS online growth is not just supported, but **required** while mounted.

Why XFS online growth is safe:

- Journaled metadata operations  
- Allocation groups expand in place  
- Grows only while mounted (required)  
- Designed for SAN arrays, RAID, HPC  
- Handles heavy concurrent I/O  

**Conclusion:**  
XFS is one of the safest and most robust filesystems for **online, mounted, high-throughput** growth.

---

## 🔴 Older Requirements (Why Some Admins Avoid Online Resize)

Before kernel **2.6.31** and early LVM2/LVM1:

- `pvresize` sometimes failed to detect new sizes  
- Multipath resizing was unreliable  
- PV resizing sometimes required `pvcreate --restorefile`  
- ext2/ext3 could corrupt if device size changed underneath 
- SAN rescan tools were buggy  
- UNIX systems generally required unmounting for geometry changes  
- LVM1 had no reliable online extension  

This produced the legacy rule:

> **“Never resize storage while mounted.”**

### Modern RHEL9 (2021+) systems:

- Online PV expansion = **safe**  
- Online LV expansion = **safe**  
- Online XFS growth = **officially supported**  
- SAN growth = **nondisruptive**  

The entire modern stack is designed for online operation.

---

## Summary Table

| Layer | Operation | Safe While Mounted / Under I/O? | Why |
|-------|-----------|----------------------------------|------|
| **SAN / FC** | Expand LUN | ✔ Yes | Engineered for nondisruptive growth |
| **LVM2 PV** | `pvresize` | ✔ Yes | Only metadata updated; no data block changes |
| **LVM2 LV** | `lvextend` | ✔ Yes | Atomic metadata update; safe under I/O |
| **Filesystems** | Online growth | ✔ Yes | XFS/ext4 support mounted expansion |

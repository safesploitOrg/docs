# 📦 Logical Volume Manager (LVM)

LVM provides a flexible, abstraction-based storage layer on Linux.  
Instead of partitioning disks directly, LVM lets you pool storage from multiple devices and allocate space dynamically.  
This improves scalability, snapshotting, resizing, and overall storage management.

---

## 🟦 Physical Volume (PV)

A Physical Volume is a disk or partition prepared for use by LVM.  
It represents the lowest LVM layer, created from real storage devices (e.g., `/dev/sda`, RAID LUNs).

**Key points:**
- Created with `pvcreate`
- Forms the building blocks of a VG
- Can be added or removed to adjust total capacity

---

## 🟧 Volume Group (VG)

A Volume Group aggregates one or more PVs into a single storage pool.  
This pool behaves like one large virtual disk.

**Key points:**
- Created with `vgcreate`
- Expands by adding more PVs
- Space is allocated to LVs from the VG

---

## 🟩 Logical Volume (LV)

A Logical Volume is carved out of a Volume Group and behaves like a virtual partition.  
Filesystems, swap, containers, or VMs are placed on LVs.

**Key points:**
- Created with `lvcreate`
- Can be resized dynamically
- Supports snapshots and thin provisioning



## Mermaid LVM2

- 🟨 **Physical Device (PD)**
- 🟦 **Physical Volume (PV)**
- 🟧 **Volume Group (VG)**
- 🟩 **Logical Volume (LV)**

---

```mermaid
flowchart TD

    %% --------------------
    %% PHYSICAL DEVICES
    %% --------------------
    A1("Physical Device 1<br>sda (60GB)")
    A2("Physical Device 2<br>sdb (50GB)")
    A3("Physical Device 3<br>sdc (40GB)")

    %% --------------------
    %% PHYSICAL VOLUMES
    %% --------------------
    B1("Physical Volume 1<br>(60GB)")
    B2("Physical Volume 2<br>(50GB)")
    B3("Physical Volume 3<br>(40GB)")

    A1 --> B1
    A2 --> B2
    A3 --> B3

    %% --------------------
    %% VOLUME GROUP
    %% --------------------
    C("Volume Group<br>(150GB)")

    B1 --> C
    B2 --> C
    B3 --> C

    %% --------------------
    %% LOGICAL VOLUMES
    %% --------------------
    D1("Logical Volume 1<br>(80GB)")
    D2("Logical Volume 2<br>(70GB)")

    C --> D1
    C --> D2

    %% --------------------
    %% COLOURS
    %% --------------------
    classDef dev fill:#f9e79f,stroke:#b7950b,color:#000,stroke-width:1px;
    classDef pv fill:#85c1e9,stroke:#2874a6,color:#000,stroke-width:1px;
    classDef vg fill:#f5b041,stroke:#ca6f1e,color:#000,stroke-width:1px;
    classDef lv fill:#82e0aa,stroke:#1d8348,color:#000,stroke-width:1px;

    class A1,A2,A3 dev;
    class B1,B2,B3 pv;
    class C vg;
    class D1,D2 lv;

```
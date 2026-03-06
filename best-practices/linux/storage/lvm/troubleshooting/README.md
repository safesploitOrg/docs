## Troubleshooting

### Visualises SAN → multipath → LVM → filesystem stack

```bash
lsblk -e7 -o NAME,HCTL,SIZE,TYPE,FSTYPE,MOUNTPOINT
```

This shows:

```text
FC path (sdX)
    ↓
multipath device (mpathX)
    ↓
LVM logical volume (LV)
    ↓
filesystem (ext4/xfs)
    ↓
mountpoint (/mnt/mpathX)
```

# rsync

- [Overview](#rsync-overview)
  - [Key Features of rsync:](#rsync-keyfeaturesofrsync)
  - [Basic Syntax:](#rsync-basicsyntax)
  - [Common Examples:](#rsync-commonexamples)
  - [Useful Options:](#rsync-usefuloptions)
- [rsync options](#rsync-rsyncoptions)
  - [🔁 Core Behaviour](#rsync-corebehaviour)
  - [💾 File Handling](#rsync-filehandling)
  - [🌐 Networking & Remote](#rsync-networkingremote)
  - [📦 Compression & Performance](#rsync-compressionperformance)
  - [🎯 Inclusion/Exclusion](#rsync-inclusionexclusion)
  - [🧪 Advanced](#rsync-advanced)
  - [✅ Common Short Form Combo](#rsync-commonshortformcombo)

---

## Overview

Sure! `rsync` is a powerful, efficient, and widely-used command-line utility for synchronising files and directories between two locations over a network or locally. It’s especially popular for backups and mirroring because of its ability to **only copy differences**, saving bandwidth and time.

---

### **Key Features of** `rsync`**:**

- **Delta Transfer Algorithm:** Only sends the differences between source and destination files, not the entire file.
- **Preserves Metadata:** Can preserve permissions, ownership, timestamps, symbolic links, and more.
- **Works Over SSH:** Securely transfers data using SSH (`rsync -e ssh` or with `-a` and a remote path).
- **Can Resume Transfers:** Useful if a large transfer is interrupted.
- **Deletion Sync:** Can delete files at the destination that no longer exist in the source (with `--delete`).
- **Compression:** Supports on-the-fly compression with `-z`.

---

### **Basic Syntax:**

```bash
rsync [options] source destination 
```

### **Common Examples:**

1. **Local directory sync:**

```bash
rsync -av /source/ /destination/ 
```

- `-a`: Archive mode (preserves most metadata).
- `-v`: Verbose output.
- The trailing slash `/` on source is important – it means “sync the contents”, not the folder itself.

---

2. **Remote sync over SSH:**

```bash
rsync -avz -e ssh /local/path/ user@remote:/remote/path/ 
```

---

3. **Sync from remote to local:**

```bash
rsync -avz user@remote:/remote/path/ /local/path/ 
```

---

4. **Dry-run (to see what will happen):**

```bash
rsync -av --dry-run /source/ /destination/ 
```

---

5. **Delete extraneous files at destination:**

```bash
rsync -av --delete /source/ /destination/ 
```

---

### **Useful Options:**

| Option                | Description                                               |
|:----------------------|:----------------------------------------------------------|
| `-a`                  | Archive mode (recursive, preserves symlinks, perms, etc.) |
| `-v`                  | Verbose output                                            |
| `-z`                  | Compress file data during the transfer                    |
| `-h`                  | Human-readable numbers (e.g. 1.1K, 234M)                  |
| `--delete`            | Delete files in destination not present in source         |
| `--exclude 'pattern'` | Exclude files/folders matching pattern                    |
| `--progress`          | Show progress during transfer                             |
| `--progress2`    | Show progress during transfer ()
| `--checksum`          | Skip based on checksum, not mod-                          |

---

## rsync options

### 🔁 **Core Behaviour**

| Option | Meaning |
| --- | --- |
| `-a` or `--archive` | Archive mode: preserves symbolic links, permissions, timestamps, group, owner, devices (same as `-rlptgoD`) |
| `-r` | Recursive: copy directories recursively |
| `-u` | Skip files that are newer on the destination |
| `-n` or `--dry-run` | Show what would be done, without actually doing it |
| `--delete` | Delete files on destination that don't exist on the source |
| `--remove-source-files` | Deletes source files after transfer (like a move) |
| `--update` | Skip files that are newer on the receiver |

---

### 💾 **File Handling**

| Option          | Meaning                                                                                 |
|:----------------|:----------------------------------------------------------------------------------------|
| `-l`            | Copy symlinks as symlinks                                                               |
| `-L`            | Transform symlinks into referent file/dir (dereference)                                 |
| `-H`            | Preserve hard links                                                                     |
| `-p`            | Preserve permissions                                                                    |
| `-o`            | Preserve owner (requires sudo if you're not root)                                       |
| `-g`            | Preserve group                                                                          |
| `-D`            | Preserve devices and special files                                                      |
| `--chmod=CHMOD` | Apply specific permissions on files/dirs (`--chmod=Du=rwx,Dg=rx,Do=rx,Fu=rw,Fg=r,Fo=r`) |

---

### 🌐 **Networking & Remote**

| Option                      | Meaning                                |
|:----------------------------|:---------------------------------------|
| `-e ssh`                    | Use SSH as the transport               |
| `--rsh=COMMAND`             | Specify remote shell to use            |
| `--rsync-path='sudo rsync'` | Run rsync with sudo on the remote host |

---

### 📦 **Compression & Performance**

| Option           | Meaning                                                             |
|:-----------------|:--------------------------------------------------------------------|
| `-z`             | Compress data during transfer                                       |
| `--progress`     | Show progress for each file                                         |
| `--stats`        | Show detailed statistics after the transfer                         |
| `--bwlimit=RATE` | Limit bandwidth (e.g. `--bwlimit=1000` for 1000 KB/s)               |
| `--inplace`      | Update destination files in-place (risky for interrupted transfers) |
| `--append`       | Continue transferring files where it left off                       |

---

### 🎯 **Inclusion/Exclusion**

| Option                | Meaning                                            |
|:----------------------|:---------------------------------------------------|
| `--exclude='PATTERN'` | Exclude files matching pattern                     |
| `--exclude-from=FILE` | Read exclude patterns from file                    |
| `--include='PATTERN'` | Include files matching pattern                     |
| `--filter='RULE'`     | Fine-grained filtering (e.g. `--filter='- *.tmp'`) |

---

### 🧪 **Advanced**

| Option                | Meaning                                                                            |
|:----------------------|:-----------------------------------------------------------------------------------|
| `--checksum`          | Compare files using checksum instead of mod-time/size (slower but more accurate)   |
| `--partial`           | Keep partially transferred files (useful for slow/large transfers)                 |
| `--backup`            | Backup destination files that are to be overwritten or deleted                     |
| `--backup-dir=/path/` | Directory to store backups of changed/deleted files                                |
| `--link-dest=/path/`  | Hardlink unchanged files from previous backup path (great for incremental backups) |

---

### ✅ **Common Short Form Combo**

```bash
rsync -avzP --delete /src/ user@host:/dest/ 
```

This means:

- `-a`: archive (recursive, preserve all)
- `-v`: verbose
- `-z`: compress
- `-P`: show progress and allow resuming
- `--delete`: clean up destination
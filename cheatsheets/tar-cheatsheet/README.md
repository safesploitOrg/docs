
[Linux](../../../../../Linux.md) > [Linux Administration](../../../../Linux%20Administration.md) > [Linux Core Administration](../../../Linux%20Core%20Administration.md) > [Linux Shell](../../Linux%20Shell.md) > [Linux Command Line](../Linux%20Command%20Line.md)

# tar

  - [🔹 Common file formats](#-common-file-formats)
  - [🔹 Core syntax](#-core-syntax)
  - [🔹 Most used options (memorise these)](#-most-used-options-memorise-these)
  - [🔹 Real-world examples](#-real-world-examples)
  - [🔹 Practical sysadmin use cases](#-practical-sysadmin-use-cases)
  - [🔹 Advanced flags (worth knowing)](#-advanced-flags-worth-knowing)
  - [🔹 Performance considerations](#-performance-considerations)
  - [⚠️ Gotchas (important)](#-gotchas-important)
  - [🔹 Mental model](#-mental-model)

---


## 🔹 What `tar` actually does

- Combines files → **one** `.tar` **file** (archiving)
- Preserves:

  - permissions
  - ownership
  - timestamps
  - directory structure
- By itself, **does NOT compress** (just packages)

Think of it like:

> 📦 `tar` = packaging  
> 🗜️ `gzip/bzip2/xz` = compression

---

## 🔹 Common file formats

|  Extension         |  Meaning         |
|:-------------------|:-----------------|
| `.tar`             | archive only     |
| `.tar.gz` / `.tgz` | gzip compressed  |
| `.tar.bz2`         | bzip2 compressed |
| `.tar.xz`          | xz compressed    |

---

## 🔹 Core syntax

```bash
tar [options] archive.tar files/
```

---

## 🔹 Most used options (memorise these)

|  **Option**    |  **Meaning**            |
|:---------------|:------------------------|
| `-c`           | create archive          |
| `-x`           | extract archive         |
| `-v`           | verbose (show progress) |
| `-f`           | file name (required)    |
| `-t`           | list contents           |
| `-z`           | gzip compression        |
| `-j`           | bzip2 compression       |
| `-J`           | xz compression          |

---

## 🔹 Real-world examples

### 📦 Create archive

```bash
tar -cvf backup.tar /data
```

### 🗜️ Create compressed archive (gzip)

```bash
tar -czvf backup.tar.gz /data
```

### 📂 Extract archive

```bash
tar -xvf backup.tar
```

### 📂 Extract `.tar.gz`

```bash
tar -xzvf backup.tar.gz
```

### 📋 List contents (no extraction)

```bash
tar -tvf backup.tar
```

### 📍 Extract to specific directory

```bash
tar -xvf backup.tar -C /restore/path
```

---

## 🔹 Practical sysadmin use cases

Given your infra background, `tar` shows up everywhere:

### 1. 🔁 Backups (quick + portable)

```bash
tar -czvf etc-backup.tar.gz /etc
```

### 2. 🚚 Data migration

- Bundle → transfer → extract (especially over SSH)

```bash
tar -czf - /data | ssh host "tar -xzf - -C /data"
```

➡️ Zero temp files, efficient for large datasets

---

### 3. 🔐 Permissions-safe packaging

- Unlike naive `cp`, preserves metadata (critical for:

  - NFS exports
  - system configs
  - app deployments)

---

### 4. 📦 Software distribution

- Most source packages come as:

  ```bash
  project.tar.gz
  ```

---

## 🔹 Advanced flags (worth knowing)

### Preserve permissions explicitly

```bash
tar -xvpf archive.tar
```

### Exclude files

```bash
tar -czvf backup.tar.gz /data --exclude="*.log"
```

### Incremental backups

```bash
tar -g snapshot.file -czvf backup.tar.gz /data
```

### Strip leading directories

```bash
tar -xvf archive.tar --strip-components=1
```

---

## 🔹 Performance considerations

- `gzip` → fast, decent compression (default)
- `bzip2` → slower, better compression
- `xz` → slowest, best compression (good for archives, not pipelines)

---

## ⚠️ Gotchas (important)

- Order matters:

  ```bash
  tar -czvf   ✅
  tar -cfzv   ❌ (can break depending on version)
  ```
- Always include `-f` before filename
- Extraction can overwrite files silently

---

## 🔹 Mental model

```bash
Files → tar → archive.tar → (optional compression) → archive.tar.gz
```
# ps Quick Reference (Linux)

A fast, practical cheat sheet for process inspection and troubleshooting. Designed for rapid recall.

---

## 🧠 Mental Model
`ps` shows running processes from the kernel's process table.

Two common styles:
- **BSD style** → `ps aux`
- **Unix style** → `ps -ef`

Both are useful in different contexts.

---

## 📌 Most Common Commands

### 🔹 Show all processes (human-friendly)
```bash
ps aux
```
- `a` = all users
- `u` = detailed/user-oriented output
- `x` = include processes without a TTY

### 🔹 Show all processes (Unix format)
```bash
ps -ef
```
- `-e` = everything
- `-f` = full format (UID, PPID, CMD, args)

---

## 🎯 Filtering Processes

### 🔹 Search for a process by name
```bash
ps aux | grep sshd
```

### 🔹 Using ps built-in pattern match (GNU)
```bash
ps -C sshd -f
```

### 🔹 Show processes for a user
```bash
ps -u root
```

### 🔹 Filter by PID
```bash
ps -p 1234 -f
```

---

## 📁 Useful Columns (What They Mean)
| Column | Meaning |
|--------|---------|
| PID | Process ID |
| PPID | Parent process ID |
| UID | User owning the process |
| %CPU | CPU usage |
| %MEM | Memory usage |
| VSZ | Virtual memory size |
| RSS | Resident memory |
| STAT | Process state |
| TIME | CPU time consumed |
| COMMAND | Command executed |

**State codes (STAT):**
- `R` → Running
- `S` → Sleeping
- `D` → Uninterruptible sleep (usually I/O)
- `T` → Stopped
- `Z` → Zombie
- `+` → Foreground process

---

## 🔧 Formatting Output

### 🔹 Custom columns
```bash
ps -eo pid,ppid,user,%cpu,%mem,cmd
```

### 🔹 Sorted by memory
```bash
ps -eo pid,user,%mem,cmd --sort=-%mem
```

### 🔹 Sorted by CPU
```bash
ps -eo pid,user,%cpu,cmd --sort=-%cpu
```

### 🔹 Tree view (relationships)
```bash
ps -ejH
```

Or:
```bash
ps -ef --forest
```

---

## 🔍 Practical Troubleshooting Examples

### 🔹 Highest CPU consumers
```bash
ps -eo pid,%cpu,cmd --sort=-%cpu | head
```

### 🔹 Highest memory consumers
```bash
ps -eo pid,%mem,cmd --sort=-%mem | head
```

### 🔹 Find processes holding open files (use with lsof)
```bash
ps -ef | grep deleted
```

### 🔹 Show environment variables for a PID
```bash
ps -p 1234 -eo pid,cmd
cat /proc/1234/environ | tr '\0' '\n'
```

---

## 🧩 Minimal Recall Table
| Concept | Shortcut |
|--------|----------|
| All processes | `ps aux` or `ps -ef` |
| Filter by name | `ps aux | grep name` |
| Custom columns | `ps -eo ...` |
| Sort | `--sort=-%cpu` or `--sort=-%mem` |
| Tree view | `--forest` |

---

## 🛠 When to Use ps vs. Other Tools
| Goal | Use |
|------|-----|
| Live, updating view | `top`, `htop` |
| Deep inspection | `/proc/<pid>/` |
| Check file handles | `lsof` |
| Check open sockets | `ss` |

---



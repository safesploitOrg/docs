# AWK Quick Reference (Linux)

A **fast, practical cheat sheet** for daily sysadmin, DevSecOps, log‑analysis, and automation work. Clean, minimal, and designed for *rapid recall*.

---

## 🧠 AWK Mental Model (Quick Recall)
```
awk 'pattern { action }' file
```
- **pattern** → when to run the action
- **action** → what to do (default: `print $0`)
- **$1, $2 … $NF** → fields
- **$0** → whole line
- **NR** → global line number
- **NF** → number of fields

---

## 📌 Common One‑Liners (Daily Use)

### 🔹 Print field(s)
```bash
awk '{ print $2 }' file
```

### 🔹 Prefix output
```bash
awk '{ print "ll  "$2 }' /etc/fstab
```

### 🔹 Print mountpoints only
```bash
df -h | awk 'NR>1 { print $NF }'
```

### 🔹 Skip comments + blank lines
```bash
awk '!/^#/ && NF { print $0 }'
```

### 🔹 Filter rows by value
```bash
awk '$3 == "ext4"' /etc/fstab
```

### 🔹 Lines matching regex
```bash
awk '/error/ { print }' /var/log/app.log
```

---

## 📁 Field Separators (FS)
### Input delimiter
```bash
awk -F":" '{ print $1 }' /etc/passwd
```

### CSV
```bash
awk -F"," '{ print $3 }' file.csv
```

### Regex delimiter
```bash
awk -F"[ ,:]" '{ print $1 }'
```

---

## 📤 Output Formatting (OFS)
```bash
awk 'BEGIN { OFS="," } { print $1, $2 }' file
```

### Pretty formatting
```bash
awk '{ printf "%-20s %s
", $1, $2 }'
```

---

## 🧮 Arithmetic & Aggregation
### Sum a column
```bash
awk '{ sum+=$2 } END { print sum }'
```

### Count lines
```bash
awk 'END { print NR }'
```

---

## 🚦 Conditionals
```bash
awk '{ if ($3 > 10) print $0 }'
```

### If/else
```bash
awk '{ if ($3>100) print "HIGH"; else print "LOW" }'
```

---

## 🔧 Key Built‑in Variables
| Var | Meaning |
|-----|---------|
| `$0` | entire line |
| `$1..$NF` | fields |
| `NF` | number of fields |
| `NR` | line number (global) |
| `FNR` | line number per file |
| `FS` | field separator |
| `OFS` | output field separator |
| `RS` | record separator |
| `ORS` | output record separator |

---

## 🪓 Useful Practical Snippets
### Remove duplicate lines
```bash
awk '!seen[$0]++' file
```

### Extract column and perform transformation
```bash
awk '{ print toupper($1) }'
```

### Replace text inline
```bash
awk '{ gsub("old","new"); print }'
```

### Print field indexes (debug)
```bash
awk '{ for (i=1;i<=NF;i++) print i, $i }'
```

---

## 📚 Real Sysadmin Examples
### Parse fstab quickly
```bash
awk '!/^#/ && NF { print $1, $2, $3 }' /etc/fstab
```

### Extract blocked IPs from logs
```bash
awk '/DENIED/ { print $NF }' firewall.log
```

### Show failed SSH attempts
```bash
awk '/Failed password/ { print $(NF-3) }' /var/log/auth.log
```

---

## 🧩 Minimal Recall Table
| Concept | Shortcut |
|--------|----------|
| Fields | `$1..$NF` |
| Whole line | `$0` |
| Line number | `NR` |
| Filter rows | `condition { print }` |
| Set delimiter | `-F","` |
| Format output | `printf` |
| Pre/Post blocks | `BEGIN` / `END` |

---


# Strong & Memorable Passwords — How to Create Them

**Goal:**  
Show how to *build* strong, **memorable passwords** from your surroundings — no generators, no jargon.

---

## 🧠 The Core Idea
Use real things around you to create a passphrase that your brain remembers easily — but others can’t guess.

**Example:**  
You’re at your desk and see:
1. A can (RedBull)  
2. A window
3. Wires (Ethernet cables)
4. Books  

You turn that into:

```txt
Redbull-window-ethernet-books!19
```

That’s already **far stronger** and **easier to remember** than `P@ssw0rd!`.

---

## 🪜 Step-by-step process

### 1️⃣ Look Around You  
Pick **3–6 random items** you can see or describe right now.
Avoid things that would be *obvious* to someone who knows you (e.g., your pet’s name).

**Examples:**
- mug, monitor, notebook, cable
- chair, window, phone, pen  
- jacket, fan, keyboard, plant
- bottle, fridge, paitning

---

### 2️⃣ Write Them as Words  
Write them down, separated by hyphens:

```txt
mug-window-cable-books
```


Already a solid base passphrase.

---

### 3️⃣ Add a Twist  
For a bit more strength, add a small personal touch (these are optional and aimed at users who want extra complexity):
- **Add a number or symbol** (like `!19` or `#77`).  
- **Use your own separator** (`_`, `.`, or nothing at all).  
- **Capitalise a word or two** — `Mug-Window-Cable-Books`  
- **(Optional) Substitute letters** (`a→@`, `e→3`, `o→0`) if you like.

These make it harder to guess but keep it easy to remember:

```txt
Mug_Window_Cable_Books#77
```

---

### 4️⃣ Check it Feels Natural  
If you can read it out loud and visualise the objects, it’s memorable. If it looks random or mechanical, you’ll forget it. Stick with your visual memory.

---

### 5️⃣ For High-Value Accounts *(optional hardening)*  
If this is for admin or financial accounts, add **one short random piece**:
- A 4-digit random number → `Redbull-window-ethernet-books!7419`  

---

## 🔑 Example Patterns (with realistic strength and entropy)

| Style              | Example                               | Est. Entropy | Strength | Notes                                      |
|:-------------------|:--------------------------------------|:-------------:|:---------:|:-------------------------------------------|
| Simple             | `plant-mug-window-pen`                | ~76 bits      | 🟢 Strong | 4 random words — already strong             |
| With symbol        | `Plant-mug-window-pen!`               | ~84 bits      | 🟢 Strong | Symbols/digits add a bit more complexity    |
| With small leet    | `Pl@nt-mug-window-p3n`                | ~79 bits      | 🟢 Strong | Slightly higher randomness, still readable  |
| With random digits | `Plant-mug-window-pen!7419`           | ~108 bits     | 🔵 Very strong | Excellent for admin or high-value logins |

---

### 🧠 What the colours mean

| Colour | Range     | Meaning                                |
|:------:|:-----------|:---------------------------------------|
| 🔴     | < 40 bits  | Weak — easy to brute-force              |
| 🟠     | 40–60 bits | Fair — acceptable if MFA is enabled     |
| 🟢     | 60–80 bits | Strong — resistant to brute-force       |
| 🔵     | 80+ bits   | Very strong — extremely hard to crack   |

---

## 🧩 Why This Works
- Each extra word adds *massive* strength — far more than random characters.  
- Humans remember **images**, not gibberish.  
- You can recreate it from memory if needed.

---

## ⚠️ Quick Safety Notes
- Don’t reuse the same password for multiple accounts.  
- Don’t use words connected to your personal life (pets, family, birthdays).  
- Don’t store your password in plain text. Use a password manager or vault.

---

## ✅ Summary (cheat-sheet)

| Step | What You Do                                         | Required |
|:----:|:----------------------------------------------------|:---------:|
| 1️⃣  | Pick 3–6 objects around you                         | ✅ |
| 2️⃣  | Join them together using `-`                        | ✅ |
| 3️⃣  | Add a symbol, number, or capital letter             | ✅ |
| 4️⃣  | Add 4 random digits for high-value or admin accounts | ✅ |
| 5️⃣  | Visualise it — if it’s memorable, you’ve done it right | ✅ |

---

**Quick tips:**
- The first two steps build the *core strength* (word count = entropy).  
- Adding symbols and digits adds *extra difficulty* for attackers.  
- Visualising your chosen items helps you *remember* it naturally.  
- For critical systems (admin, cloud, finance), always use **MFA** in addition to a strong passphrase.

## Quick links
- Password Generator: https://password.git.safesploit.com/  
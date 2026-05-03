# Linux Tmux

  - [Starting a New tmux Session](#starting-a-new-tmux-session)
  - [Managing Windows and Panes](#managing-windows-and-panes)
  - [Detaching and Reattaching](#detaching-and-reattaching)
  - [Killing a Session](#killing-a-session)

---


## Overview

`tmux` is a terminal multiplexer, which allows you to manage multiple terminal sessions within a single window. It’s especially useful for managing long-running processes and maintaining persistent sessions that can be reattached later. Here are some basic `tmux` commands and features:

### Starting a New tmux Session

- **Create a new tmux session:**

  ```bash
  tmux new -s session_name 
  ```
- **Detach from a session:**  
  While inside a `tmux` session, press:

  ```bash
  Ctrl + b, then d
  ```
- **Attach to an existing session:**

  ```bash
  tmux attach -t session_name 
  ```
- **List all sessions:**

  ```bash
  tmux ls 
  ```

---

### Managing Windows and Panes

- **Create a new window:** Press `Ctrl-b` then `c`.
- **Switch between windows:** Press `Ctrl-b` then the window number (e.g., `Ctrl-b 1`).
- **Split the window horizontally:** Press `Ctrl-b` then `%`.
- **Split the window vertically:** Press `Ctrl-b` then `"`.
- **Switch between panes:** Press `Ctrl-b` then the arrow keys.
- **Close the current pane:** Press `Ctrl-b` then `x` (you’ll be asked for confirmation).

---

### Detaching and Reattaching

- **Detach from a session:** Press `Ctrl-b` then `d`.
- **Reattach to a session:**

  ```bash
  tmux attach-session -t session_name 
  ```

---

### Killing a Session

- **Kill the current window:** Press `Ctrl-b` then `&` (confirm to close the window).
- **Kill a session:**

  ```bash
  tmux kill-session -t session_name
  ```

---

## Best Practices to Secure `tmux`:

- Use **SSH** and ensure that strong SSH key pairs are in use for authentication.
- Regularly check the permissions of `tmux` socket files and session files.
- Lock your `tmux` session when you're away (`tmux lock-session`).
- Ensure `tmux` sessions don’t run with elevated privileges unless absolutely necessary.
- Log out or kill sessions when you're done, especially if they contain sensitive data.
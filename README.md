# 🛡️ Iridium Password Generator Pro

**Iridium Pro** is a high-security, stateless password generator designed to run on **WSL (Windows Subsystem for Linux)**. It uses cryptographic hashing to generate consistent, ultra-secure passwords without ever storing them in a database.

---

## ✨ Key Features

* **Stateless Security**: No database, no cloud, no leaks. Your master password + a service seed + a private salt are the only things that create your keys.
* **WSL-Windows Bridge**: Seamlessly copies generated passwords directly to your Windows 11 clipboard using native `clip.exe` integration.
* **Privacy-First Interface**: 
    * Uses `getpass` for invisible master password entry.
    * Automatic 20-second clipboard clearing.
    * **Security Flash**: Uses ANSI escape codes (`\033[H\033[J`) to wipe the terminal screen completely after use, leaving zero visual trace.
* **Professional Cryptography**: Powered by the **SHA-256** hashing algorithm.

---

## 🚀 Installation & Setup

1.  **Clone or create the directory**:
    ```bash
    mkdir iridium && cd iridium
    ```

2.  **Set up the Python Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install pyperclip
    ```

3.  **Install Linux Dependencies** (Required for the `pyperclip` library):
    ```bash
    sudo apt update && sudo apt install xclip -y
    ```

---

## 🛠️ How to Use

1.  **Activate the environment**: `source .venv/bin/activate`
2.  **Run the script**: `python3 iridium.py`
3.  **Enter your Master Password**: Minimum 10 characters (it will be invisible as you type).
4.  **Enter a Seed**: The name of the service (e.g., 'gmail', 'amazon', 'work-vpn').
5.  **Set Length & Symbols**: Choose your preferred security level.
6.  **Paste**: The password is copied to your Windows clipboard. You have **20 seconds** to paste it (Ctrl+V).

---

## 🧠 Security Architecture

The core logic follows this cryptographic flow:



1.  **Concatenation**: Combines `Master Password + Seed + Private Salt`.
2.  **Hashing**: SHA-256 creates a unique, irreversible 256-bit fingerprint of that string.
3.  **Mapping**: The resulting hash is mathematically mapped to a specific character set (letters, numbers, symbols) using modulo operations.
4.  **Cleanup**: Executing the "Triple-Wipe Protocol" (Python memory, Windows clipboard, and Terminal buffer).

---

## ⚠️ Important Security Note
The `SECRET_SALT` inside the script is what makes your passwords unique to you. **Do not share your script with the salt included.** If you lose or change the salt, you will not be able to regenerate the same passwords for your services.

---
*Developed for LG Gram / WSL Environment - 2026*
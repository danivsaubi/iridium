# 🛡️ Iridium Universal Password Generator

**Iridium** is a high-security, stateless, and zero-dependency password generator. It uses cryptographic SHA-256 hashing to generate consistent, ultra-secure passwords without ever storing them.

Built to be **truly universal**, it runs natively on **Windows**, **Linux (WSL)**, and **Android (Termux)** without requiring any external Python libraries.

---

## ✨ Key Features

* **Stateless Security**: No database, no cloud, no leaks. Your master password + service seed + private salt = your unique key.
* **Zero Dependencies**: Uses only Python's standard library. No `pip install` required.
* **Universal Clipboard Support**:
    * **Windows / WSL**: Native integration with `clip.exe`.
    * **Android**: Native integration with `termux-clipboard-set`.
    * **Linux**: Support for `xclip` or `xsel`.
* **Safety First**: 
    * **Double-entry verification**: Prevents typos in your Master Password.
    * **Security Flash**: Wipes the terminal screen and clears the clipboard after 20 seconds.
* **Professional Cryptography**: Powered by **SHA-256** for deterministic key generation.

---

## 🚀 Quick Start

### 1. Prerequisite
You only need **Python 3.x** installed on your system.

### 2. Usage
Run it directly from your terminal:
```bash
python3 iridium.py
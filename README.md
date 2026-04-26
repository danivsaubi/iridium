# 🛡️ Iridium Crypto Suite

**Iridium** is an advanced security toolkit designed for the terminal, specifically optimized for **WSL (Windows Subsystem for Linux)** and Linux environments. It provides deterministic high-entropy password generation and file protection using military-grade encryption.

## ✨ Key Features

* **Password Generator:** Create unique keys from 10 to 256 characters using SHA-512.
* **File Vault:** Secure file encryption and decryption using **AES-256-GCM** (authenticated encryption).
* **Smart Path Navigation:** Robust TAB-completion that handles spaces, file extensions, and is case-insensitive.
* **Privacy & Security:**
    * Automatic Windows clipboard clearing (via 'clip.exe') after 20 seconds.
    * Automatic screen clearing post-generation to prevent shoulder-surfing.
    * Mandatory Master Password (minimum 10 characters) with double-entry confirmation.

---

## 🚀 Installation

### 1. Prerequisites
Ensure you have Python 3 installed along with the 'cryptography' library. Run these commands:
sudo apt update
sudo apt install python3-pip
pip install cryptography

### 2. Alias Configuration (Highly Recommended)
To launch the suite instantly by typing 'iridium' from any directory, add this line to your ~/.bashrc or ~/.zshrc file:
alias iridium='python3 ~/path/to/your/script/iridium.py'

*After adding it, run 'source ~/.bashrc' to apply the changes.*

---

## 🛠️ Usage Instructions

### 🔑 Password Generator
1. Master Password: Enter your master key (min. 10 characters).
2. Service Seed: The service name or context (e.g., google, github). This ensures every generated key is unique.
3. Length: Choose between 10 and 256. Pressing Enter defaults to 20 characters.
4. Symbols: Choose whether to include special characters for increased entropy.
5. Clipboard & Security: The password is automatically copied to the clipboard. A 20-second countdown will trigger, after which the clipboard is cleared and the screen is wiped.

### 🔐 Iridium Vault
* Encrypt: Select a file using TAB to browse your filesystem. The program will generate a secure .iridium container.
* Decrypt: Select an .iridium file. The toolkit will automatically restore the file with its original name and extension (e.g., .pdf, .jpg) using internal metadata headers.
* Secure Deletion: Once the process is finished, the program offers to delete the original unencrypted file (or the container).

---

## 🧠 Technical Details

* Key Derivation: SHA-512 with dynamic salting.
* Encryption: AES-256 in GCM (Galois/Counter Mode), providing both encryption and integrity verification.
* Zero Logs: No passwords, history, or metadata are stored on disk; everything is handled in volatile memory.

---

## 📋 RELEASE NOTES - v1.1.0

### 🚀 NEW FEATURES
- **Version Flag System:** Starting from this release, the project follows a semantic versioning flag. This allows for better tracking of updates and compatibility.
- **Ultimate TAB Completion:** Re-engineered path handling to support file extensions, dots, and spaces without breaking the terminal input.
- **Automatic Extension Recovery:** Implemented a 10-byte internal header to store the original file extension. Decrypting now restores the exact file type (e.g., .pdf, .zip) automatically.
- **Variable Password Length:** Users can now specify any length between 10-256 characters with a default fallback to 20.

### 🛠️ IMPROVEMENTS & FIXES
- **Privacy Wipe:** Integrated automatic 'clear_screen' command executed after the 20-second security timer.
- **UI Branding:** Updated all headers and menus to the new "IRIDIUM CRYPTO SUITE" visual identity.
- **WSL Stability:** Resolved the "phantom input" bug where the terminal would skip path prompts.
- **Code Reliability:** Fixed missing 'readline' imports and optimized delimiter handling for Linux shells.

---
*Note: Your security depends entirely on the strength of your Master Password. Never share it.*
#!/usr/bin/env python3
import hashlib
import getpass
import string
import time
import os
import subprocess
import sys

# --- SECURITY CONFIGURATION ---
# --- SECURITY CONFIGURATION ---
# It will try to load the salt from your system environment for safety.
# If not found, it uses a placeholder.
SECRET_SALT = os.environ.get("IRIDIUM_SALT", "REPLACE_THIS_WITH_YOUR_PRIVATE_SALT_IN_ENV")

def copy_to_clipboard(text):
    """Detects the operating system and copies text to the clipboard natively."""
    try:
        # 1. WINDOWS (or WSL pointing to Windows)
        win_clip = "/mnt/c/Windows/System32/clip.exe" if os.path.exists("/mnt/c/Windows") else "clip.exe"
        if sys.platform == "win32" or os.path.exists("/mnt/c/Windows"):
            process = subprocess.Popen([win_clip], stdin=subprocess.PIPE, shell=(sys.platform=="win32"))
            process.communicate(input=text.encode())
            return "Windows Clipboard"

        # 2. ANDROID (Termux)
        if subprocess.run(["which", "termux-clipboard-set"], capture_output=True).returncode == 0:
            subprocess.run(["termux-clipboard-set"], input=text.encode())
            return "Termux Clipboard"

        # 3. UNIX / LINUX (Generic)
        for tool in ["xclip -selection clipboard", "xsel -bi"]:
            cmd = tool.split()
            if subprocess.run(["which", cmd[0]], capture_output=True).returncode == 0:
                subprocess.run(cmd, input=text.encode())
                return f"Linux ({cmd[0]})"
    except:
        pass
    return None

def generate_password(master, seed, length, symbols):
    """Deterministic SHA-256 password generation."""
    full_string = master + seed + SECRET_SALT
    hash_hex = hashlib.sha256(full_string.encode()).hexdigest()
    
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += "!@#$%^&*()-_+=<>?"

    final_pass = ""
    hash_int = int(hash_hex, 16)
    for _ in range(length):
        final_pass += chars[hash_int % len(chars)]
        hash_int //= len(chars)
    return final_pass

def main():
    # Universal screen clear (ANSI)
    print("\033[H\033[J", end="")
    print("===== 🛡️ Iridium Universal Password Generator =====")
    print("=" * 30)

    # User Inputs with Confirmation
    master = getpass.getpass("🔑 Master Password: ")
    confirm_master = getpass.getpass("🔁 Confirm Master Password: ")

    if master != confirm_master:
        print("\n❌ Error: Passwords do not match. Integrity first!")
        return

    if len(master) < 10:
        print("\n❌ Error: Master password must be at least 10 characters.")
        return

    seed = input("🌱 Service (e.g., gmail, bank): ").strip().lower()
    
    try:
        ln_in = input("📏 Length [16]: ")
        length = int(ln_in) if ln_in else 16
    except: length = 16

    sym_in = input("✨ Use Symbols? (y/n) [y]: ").lower()
    use_symbols = False if sym_in == 'n' else True

    # Generation
    password = generate_password(master, seed, length, use_symbols)

    # Clipboard Operation
    method = copy_to_clipboard(password)
    
    print("\n" + "—" * 30)
    if method:
        print(f"✅ Copied to: {method}")
    else:
        print("⚠️ Automatic copy failed. Clipboard tool not found.")
    
    print(f"🔑 PASSWORD: {password}")
    print("—" * 30 + "\n")

    # Security Timer
    try:
        for i in range(20, 0, -1):
            print(f"🧹 Clearing memory in {i}s... ", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # Final Cleanup
    copy_to_clipboard("") # Clear clipboard
    print("\033[H\033[J🔒 Memory and screen cleared.")

if __name__ == "__main__":
    main()
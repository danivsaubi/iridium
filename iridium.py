#!/usr/bin/env python3
import hashlib
import getpass
import string
import time
import os
import subprocess
import pyperclip

# --- SECURITY CONFIGURATION ---
# Important: Changing this secret string will change all generated passwords!
SECRET_SALT = "birds-are-nothing-but-glorified-dinosaurs"

def generate_password(master_password, seed, length, use_symbols):
    # 1. Hashing logic
    full_string = master_password + seed + SECRET_SALT
    hash_hex = hashlib.sha256(full_string.encode()).hexdigest()
    
    # 2. Character set
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += "!@#$%^&*()-_+=<>?"

    # 3. Mapping hash to string
    final_password = ""
    hash_int = int(hash_hex, 16)
    
    for i in range(length):
        index = hash_int % len(characters)
        final_password += characters[index]
        hash_int //= len(characters)
        
    return final_password

def copy_to_windows_clipboard(text):
    """Bridge function to send text to Windows clipboard from WSL."""
    win_clip_path = "/mnt/c/Windows/System32/clip.exe"
    if os.path.exists(win_clip_path):
        try:
            process = subprocess.Popen([win_clip_path], stdin=subprocess.PIPE)
            process.communicate(input=text.encode())
            return True
        except:
            return False
    return False

def main():
    # Initial clear (Ctrl+L)
    print("\033[H\033[J", end="")
    
    print("IRIDIUM PASSWORD GENERATOR PRO")
    print("-" * 30 + "\n")
    
    # 1. Master Password
    while True:
        m_pass = getpass.getpass("🔑 Master Password (min 10): ")
        if len(m_pass) >= 10:
            confirm = getpass.getpass("🔄 Confirm Master Password: ")
            if m_pass == confirm:
                break
            print("❌ Error: Passwords do not match.")
        else:
            print("❌ Error: Minimum 10 characters required.")
            
    # 2. Seed
    seed = input("🌱 Seed / Service: ")
    
    # 3. Length
    while True:
        try:
            len_input = input("📏 Length (10-256): ")
            password_length = int(len_input)
            if 10 <= password_length <= 256: break
            print("❌ Error: Use a number between 10 and 256.")
        except ValueError:
            print("❌ Error: Please enter a valid number.")

    # 4. Symbols
    use_syms = input("✨ Include symbols? (y/n): ").lower() == 'y'
    
    # 5. Generation
    result = generate_password(m_pass, seed, password_length, use_syms)
    
    # 6. Output & Security Countdown
    print("\n" + "-" * 30)
    try:
        pyperclip.copy(result)
        win_success = copy_to_windows_clipboard(result)
        
        status = "Windows clipboard" if win_success else "Standard clipboard"
        print(f"✅ Copied to {status}!")
        print(f"\n🔑 PASSWORD: {result}\n")
        print("-" * 30)
        
        # Countdown
        for i in range(20, 0, -1):
            print(f"Security clear in {i}s... ", end="\r")
            time.sleep(1)
            
        # THE CLEANUP (The "Flash" effect)
        pyperclip.copy("")
        copy_to_windows_clipboard("")
        
        # Clear screen (Ctrl+L equivalent)
        print("\033[H\033[J", end="")
        
        # Minimalist security flash
        print("Done. Clipboard & screen cleared.")
        
    except Exception as e:
        print(f"\n❌ Clipboard error: {e}")
        print(f"Your password is: {result}")

if __name__ == "__main__":
    main()
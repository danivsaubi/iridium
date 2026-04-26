import hashlib
import getpass
import time
import os
import sys
import readline
import subprocess
import unicodedata
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- TAB COMPLETION CONFIG (CLEAN & CASE-INSENSITIVE) ---

def path_completer(text, state):
    # 'text' ara conté exactament tot el que l'usuari ha escrit a la línia
    expanded_path = os.path.expanduser(text)
    dirname = os.path.dirname(expanded_path)
    basename = os.path.basename(expanded_path)
    
    # Determinar el directori on buscar (si està buit, és el directori actual)
    search_dir = dirname if dirname else '.'
        
    try:
        items = os.listdir(search_dir)
    except OSError:
        return None
        
    matches = []
    for item in items:
        # Filtre case-insensitive
        if item.lower().startswith(basename.lower()):
            
            # Reconstruïm la ruta respectant com l'ha escrit l'usuari (~, relatiu, etc.)
            user_dirname = os.path.dirname(text)
            if not user_dirname:
                display = item
            elif user_dirname == '/':
                display = '/' + item
            else:
                display = user_dirname + "/" + item
                
            full_path = os.path.join(search_dir, item)
            
            # Afegim la barra '/' només si és un directori
            if os.path.isdir(full_path):
                matches.append(display + '/')
            else:
                matches.append(display)
                
    try:
        return matches[state]
    except IndexError:
        return None

# LA CLAU MÀGICA: Només el tabulador i el salt de línia separen paraules.
# Així, un fitxer com "El meu fitxer.txt" es llegeix i completa d'una sola peça.
readline.set_completer_delims('\t\n')
readline.set_completer(path_completer)
readline.parse_and_bind("tab: complete")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def copy_to_clipboard(text):
    try:
        subprocess.run(['clip.exe'], input=text.encode(), check=True, stderr=subprocess.DEVNULL)
        return True
    except: return False

# --- MODULE 1: PASSWORD GENERATOR ---

def password_generator(salt):
    clear_screen()
    print("🛡️  IRIDIUM PASSWORD GENERATOR")
    print("-" * 30)
    
    while True:
        mp = getpass.getpass("Master Password (min 10 chars): ")
        if len(mp) < 10:
            print("❌ Password too short! Must be at least 10 characters.")
            continue
        mp_confirm = getpass.getpass("Confirm Master Password: ")
        if mp != mp_confirm:
            print("❌ Passwords do not match! Try again.")
            continue
        break

    seed = input("Seed: ").lower().strip()
    
    while True:
        try:
            length_input = input("Password length (10-256) [default 20]: ").strip()
            length = int(length_input) if length_input else 20
            if 10 <= length <= 256: break
            else: print("❌ Please enter a number between 10 and 256.")
        except ValueError: print("❌ Invalid input. Please enter a number.")

    include_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
    
    key_material = mp + seed + salt
    full_hex = hashlib.sha512(key_material.encode()).hexdigest()
    while len(full_hex) < length * 2:
        full_hex += hashlib.sha512(full_hex.encode()).hexdigest()
    
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if include_symbols: charset += "!@#$%^&*()-_=+"
    
    password = "".join(charset[int(full_hex[i*2:i*2+2], 16) % len(charset)] for i in range(length))
    
    show_pwd = input("\nShow password on screen? (y/N): ").lower() == 'y'
    if show_pwd: print(f"🔑 Password: {password}")
    
    if copy_to_clipboard(password):
        print("\n✅ Password copied to clipboard!")
        for i in range(20, 0, -1):
            sys.stdout.write(f"\r🧹 Clearing clipboard and screen in {i}s... ")
            sys.stdout.flush()
            time.sleep(1)
        copy_to_clipboard("")
        # Neteja de seguretat abans de sortir
        clear_screen()
        print("🛡️  IRIDIUM SECURITY")
        print("-" * 30)
        print("✅ Clipboard and screen cleared for security.")
    else:
        if not show_pwd: print(f"\n🔑 Password: {password}")
    
    input("\nPress ENTER to return to menu...")

# --- MODULE 2: FILE VAULT ---

def process_file(action, input_path, salt):
    clear_screen()
    filename = os.path.basename(input_path)
    print(f"🔐 {'ENCRYPTING' if action == '1' else 'DECRYPTING'}: {filename}")
    print("-" * 40)
    
    # Validation loop for Master Password
    while True:
        mp = getpass.getpass("Master Password (min 10 chars): ")
        if len(mp) < 10:
            print("❌ Master Password too short! Must be at least 10 characters.")
            continue
            
        if action == '1': # Encryption requires confirmation
            mp_confirm = getpass.getpass("Confirm Master Password: ")
            if mp != mp_confirm:
                print("❌ Passwords do not match! Try again.")
                continue
        break
        
    seed = input("Vault Seed: ").lower().strip()
    key = hashlib.sha256((mp + seed + salt).encode()).digest()
    aesgcm = AESGCM(key)
    
    try:
        if action == '1':
            file_name_only, file_ext = os.path.splitext(input_path)
            output_path = file_name_only + ".iridium"
            with open(input_path, 'rb') as f: data = f.read()
            
            # Header for extension restoration
            ext_header = file_ext.ljust(10).encode('utf-8')
            payload = ext_header + data
            
            nonce = os.urandom(12)
            with open(output_path, 'wb') as f: 
                f.write(nonce + aesgcm.encrypt(nonce, payload, None))
            
            print(f"\n✅ Success: Created {os.path.basename(output_path)}")
            if input("\n🗑️ Delete original file? (y/N): ").lower() == 'y':
                os.remove(input_path)
        else:
            with open(input_path, 'rb') as f:
                nonce, ctx = f.read(12), f.read()
            
            decrypted_payload = aesgcm.decrypt(nonce, ctx, None)
            original_ext = decrypted_payload[:10].decode('utf-8').strip()
            original_data = decrypted_payload[10:]
            
            base_path = input_path.rsplit('.', 1)[0]
            output_path = base_path + original_ext
            
            with open(output_path, 'wb') as f: 
                f.write(original_data)
            
            print(f"\n✅ Success: Restored as {os.path.basename(output_path)}")
            if input("\n🗑️ Delete container? (y/N): ").lower() == 'y':
                os.remove(input_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
    input("\nPress ENTER to continue...")

def vault_menu(salt):
    clear_screen()
    print("📂 IRIDIUM CRYPTO VAULT")
    print("-" * 30)
    print("1) Encrypt file\n2) Decrypt file\nb) Back")
    
    choice = input("\nAction: ").lower().strip()
    if choice == 'b': return
    if choice not in ['1', '2']: return
    
    # Netegem el buffer de readline per evitar salts
    readline.set_startup_hook(lambda: readline.insert_text("")) 
    
    try:
        raw_path = input("\nEnter file path: ").strip()
        # Si per algun motiu l'input és buit (el "fantasma"), tornem a demanar
        if not raw_path:
            raw_path = input("Enter file path: ").strip()
    finally:
        readline.set_startup_hook() # Desactivem el hook

    path = os.path.expanduser(raw_path.replace("\\ ", " ").replace("'", "").replace('"', ""))
    
    # Resolució case-insensitive
    resolved = None
    if os.path.exists(path):
        resolved = path
    else:
        parent = os.path.dirname(path) or "."
        target = os.path.basename(path).lower()
        try:
            for entry in os.listdir(parent):
                if entry.lower() == target:
                    resolved = os.path.join(parent, entry)
                    break
        except: pass

    if resolved and os.path.isfile(resolved):
        process_file(choice, resolved, salt)
    else:
        print(f"\n❌ Error: File not found: {raw_path}")
        input("Press ENTER to return...")

# --- MAIN ENGINE ---

if __name__ == "__main__":
    salt = os.environ.get('IRIDIUM_SALT', 'default_salt_123')
    while True:
        clear_screen()
        print("🛡️  IRIDIUM CRYPTO SUITE")
        print("=" * 30)
        print("Choose an option below:")
        print("1) Password Generator\n2) File Vault\nq) Quit")
        sel = input("\nSelection: ").lower().strip()
        if sel == '1': password_generator(salt)
        elif sel == '2': vault_menu(salt)
        elif sel == 'q': break
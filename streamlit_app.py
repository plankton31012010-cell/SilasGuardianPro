import time
import hashlib

class SilasGuardian:
    def __init__(self):
        self.security_level = "A0"
        self.sectors = {
            0: {"name": "False Trail", "status": "Deceptive"},
            1: {"name": "Core System", "status": "Standby"},
            2: {"name": "Comms Bridge", "status": "Standby"},
            3: {"name": "Data Vault", "status": "Locked"} # Ehemals Archiv-Daten
        }

    def boot_sequence(self, auth_key, sector_pass):
        """Initialisiert den A1-Hochfahrmodus"""
        print(f"[*] Initialisiere SilasGuardian Production Mode...")
        
        # Authentifizierungs-Check
        if auth_key.lower() == "silas":
            print("[+] Identität bestätigt. Lade Kernmodule...")
            time.sleep(1)
            
            if sector_pass.lower() == "data":
                self.security_level = "A1"
                self.sectors[3]["status"] = "ACTIVE"
                print(f"[SUCCESS] Sektor 3 (Data Vault) autorisiert und online.")
                self.activate_full_system()
            else:
                print("[!] Falsches Sektor-Passwort. Zugriff verweigert.")
        else:
            print("[CRITICAL] Unbefugter Zugriff detektiert. Notfall-A0 wird gehalten.")

    def activate_full_system(self):
        print("--- SYSTEM-STATUS: ONLINE ---")
        for s_id, info in self.sectors.items():
            print(f"Sector {s_id} [{info['name']}]: RUNNING")
        print("------------------------------")
        print("Willkommen zurück, Silas. Alle Protokolle sind aktiv.")

# --- STARTUP ---
if __name__ == "__main__":
    guardian = SilasGuardian()
    # Beispiel für den realen Aufruf:
    guardian.boot_sequence(auth_key="silas", sector_pass="data")

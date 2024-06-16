import platform
import subprocess
import sys
import os
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

def cek_dan_instal(paket):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paket])
        print(Fore.BLUE + f"{paket} berhasil diinstal.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Kesalahan saat menginstal {paket}: {e}")

def main():
    os_type = platform.system()
    print(f"Sistem operasi: {os_type}")

    if os_type == "Windows":
        try:
            print("Memeriksa apakah virtual environment sudah terinstal...")
            subprocess.check_call([sys.executable, "-m", "venv", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(Fore.YELLOW + "Virtual environment sudah terinstal.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "Virtual environment belum terinstal. Melakukan instalasi virtual environment...")
            cek_dan_instal("virtualenv")

        try:
            print("Memeriksa apakah PyInstaller sudah terinstal...")
            subprocess.check_call(["pyinstaller", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(Fore.YELLOW + "PyInstaller sudah terinstal.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "PyInstaller belum terinstal. Melakukan instalasi PyInstaller...")
            cek_dan_instal("pyinstaller")

        # Membuat virtual environment di Windows
        print("Membuat virtual environment di Windows...")
        subprocess.run([sys.executable, "-m", "venv", "myenv"], shell=True)
        activate_script = os.path.join(os.getcwd(), "myenv", "Scripts", "activate")

        # Pindah ke dalam folder myenv
        if os.path.exists(activate_script):
            print("Pindah ke dalam folder myenv...")
            os.chdir(os.path.dirname(os.path.dirname(activate_script)))  # Naik satu level
            print(f"Sekarang berada di: {os.getcwd()}")  # Tambahkan pernyataan debug

        # Aktivasi lingkungan virtual
        if os.path.exists(activate_script):
            print("Mengaktifkan virtual environment...")
            activate_cmd = f"cmd /k {activate_script}"
            subprocess.Popen(activate_cmd, shell=True)
        else:
            print(Fore.RED + "Gagal mengaktifkan virtual environment.")
            return

        # Instalasi dependensi (jika diperlukan)
        print("Memulai instalasi dependensi...")
        pip_cmd = os.path.join(os.path.dirname(activate_script), "pip")
        result = subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
        if result.returncode == 0:
            print(Fore.BLUE + "Instalasi dependensi selesai.")  # Tambahkan pernyataan debug
        else:
            print(Fore.RED + "Gagal menginstal dependensi.")

        # Membuat file eksekusi tunggal menggunakan PyInstaller
        print("Membuat file eksekusi tunggal menggunakan PyInstaller...")
        result = subprocess.run([
         "pyinstaller",
#         "--add-binary", "stage1.bin:.",
#         "--add-binary", "stage2.bin:.",
         "--onefile",
         "--paths", r"C:\Users\class\OneDrive\Desktop\py\myenv\Lib\site-packages",
         "main.py"])
        if result.returncode == 0:
            print(Fore.BLUE + "Pembuatan file eksekusi tunggal selesai.")  # Tambahkan pernyataan debug
        else:
            print(Fore.RED + "Gagal membuat file eksekusi tunggal.")

        # Mencetak pesan dengan warna
        print(Fore.GREEN + Style.BRIGHT + "Pembuatan virtual environment dan PyInstaller selesai. File eksekusi tunggal telah dibuat.")
    else:
        print(Fore.RED + "Sistem operasi tidak didukung.")

if __name__ == "__main__":
    main()
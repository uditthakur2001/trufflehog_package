import os
import shutil
import subprocess
import platform
import urllib.request
import zipfile
import tarfile

def download_trufflehog():
    system = platform.system().lower()
    if system == 'windows':
        url = "https://github.com/trufflesecurity/trufflehog/releases/download/v3.81.10/trufflehog_3.81.10_windows_amd64.tar.gz"
        download_path = "trufflehog-windows-amd64.zip"
    elif system == 'linux':
        url = "https://github.com/trufflesecurity/trufflehog/releases/download/v3.81.10/trufflehog_3.81.10_linux_amd64.tar.gz"
        download_path = "trufflehog-linux-amd64.tar.gz"
    else:
        raise OSError("Unsupported operating system")

    print(f"Downloading TruffleHog from {url}...")
    urllib.request.urlretrieve(url, download_path)
    return download_path

def install_trufflehog(download_path):
    system = platform.system().lower()
    if system == 'windows':
        # with zipfile.ZipFile(download_path, 'r') as zip_ref:
        #     zip_ref.extractall('trufflehog')
        with tarfile.open(download_path, 'r:gz') as tar_ref:
            tar_ref.extractall('trufflehog')
        binary_path = os.path.join('trufflehog', 'trufflehog')
        install_path = os.path.join(os.environ['ProgramFiles'], 'TruffleHog')
    elif system == 'linux':
        with tarfile.open(download_path, 'r:gz') as tar_ref:
            tar_ref.extractall('trufflehog')
        binary_path = os.path.join('trufflehog', 'trufflehog')
        install_path = '/usr/local/bin'
    else:
        raise OSError("Unsupported operating system")

    if not os.path.exists(install_path):
        os.makedirs(install_path, exist_ok=True)

    shutil.move(binary_path, install_path)
    print(f"TruffleHog installed to {install_path}")

    return install_path

def add_to_path(install_path):
    system = platform.system().lower()

    if system == 'windows':
        current_path = os.environ.get('PATH', '')
        if install_path not in current_path:
            new_path = f"{current_path};{install_path}"
            try:
                subprocess.run(f'setx PATH "{new_path}"', shell=True, check=True)
                print("TruffleHog path has been added to your system PATH.")
                print("Please restart your Command Prompt or PowerShell for the changes to take effect.")
            except subprocess.CalledProcessError as e:
                print(f"Error updating PATH: {e}")
        else:
            print("TruffleHog path is already in your system PATH.")

    elif system == 'linux':
        bashrc_path = os.path.expanduser("~/.bashrc")
        with open(bashrc_path, "a") as bashrc:
            bashrc.write(f"\nexport PATH=$PATH:{install_path}\n")
        subprocess.run(["source", bashrc_path], shell=True)
        print("TruffleHog path has been added to your ~/.bashrc file.")

    else:
        raise OSError("Unsupported operating system")

def main():
    download_path = download_trufflehog()
    # install_path = install_trufflehog(download_path)
    # add_to_path(install_path)
    print("TruffleHog download complete.")

if __name__ == "__main__":
    main()

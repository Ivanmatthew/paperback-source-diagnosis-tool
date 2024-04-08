import subprocess
import webbrowser
import platform

def is_windows():
    return platform.system() == 'Windows'

def detect_mitmproxy():
    try:
        subprocess.run(['mitmproxy', '--version'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def is_compatible_win_version():
    if not is_windows():
        return None
    
    version = platform.uname()
    if version.release in ['7', '8', '8.1', '10', '11']:
        return True, version.release
    else:
        return False, version.release
    

def main():
    print("Detecting mitmproxy...")
    if not detect_mitmproxy():
        print("mitmproxy not found.")
        print("Please install mitmproxy. For your convenience, a popup window of microsoft store will be opened.")
        # The microsoft store link for mitmproxy
        webbrowser.open('ms-windows-store://pdp/?ProductId=9NWNDLQMNZD7')
        print("After installation, please run this script again.")
        return
    print("mitmproxy found.")

    print("Checking Windows version...")
    is_compatible, version = is_compatible_win_version()
    if not is_compatible:
        print("Windows version not supported.")
        print("Please use Windows 7, 8, 8.1, 10 or 11.")
        return
    print("Detected OS (Windows) version: " + version)

    print("All prerequisites are satisfied.")

        


if __name__ == "__main__":
    main()
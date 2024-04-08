import subprocess

def main():
    subprocess.run('poetry run python -m PyInstaller --clean -y main.spec', stdout=subprocess.PIPE, check=True)
    print('Build complete')

if __name__ == '__main__':
    main()
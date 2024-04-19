import subprocess

def build():
    subprocess.run('poetry run python -m PyInstaller --clean -y main.spec', stdout=subprocess.PIPE, check=True)
    print('Build complete')

def pack():
    subprocess.run(["makensis", ".nsi"], stdout=subprocess.PIPE, check=True)
    print('Pack complete')

def main():
    build()
    pack()

if __name__ == '__main__':
    main()
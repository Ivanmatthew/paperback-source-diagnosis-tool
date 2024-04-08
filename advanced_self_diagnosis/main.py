import signal
import subprocess
from os import path
import platform
import ctypes
import regex as re
import requests as req
import sys
import socket
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QComboBox, QMessageBox
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColorConstants, QIcon
from PySide6.QtCore import Qt, QProcess
import PySide6.QtAsyncio as QtAsyncio

base_dir = path.dirname(__file__)


def detect_mitm():
    try:
        subprocess.run(['mitmproxy', '--version'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_target_json(target_urls):
    with open('latest.json', 'w') as file:
        json_to_write = {
            "target_urls": target_urls
        }
        json.dump(json_to_write, file, indent=4)

def scrape_urls(code):
    urls = []
    for line in code.split("\n"):
        match = re.search(r"[\*\/].*|(https?://[^\}\'\"\r\n\t\f\v ]*)", line)
        if match and match.group(1):
            urls.append(match.group(1))
    
    return urls

def get_internal_ip():
    address_info = socket.getaddrinfo(socket.gethostname(), '8080')
    address_info = [x for x in address_info if x[4][0].startswith('192.168.')]
    if len(address_info) == 0:
        return None
    
    return address_info[0][4][0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_sources = {}
        self.repo_base_url = None
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Paperback Self-Diagnosis Tool")
        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.create_widgets()
        self.highlight_format = QTextCharFormat()

    def create_widgets(self):
        # Create layouts
        self.main_content_layout = QHBoxLayout()
        self.frame_1_layout = QVBoxLayout()
        self.frame_2_layout = QVBoxLayout()

        # Parent layouts
        self.main_content_layout.addLayout(self.frame_1_layout, 1)

        # Create widgets
        self.input_label = QLabel("Enter Paperback Repository URL:")

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Can be either base url or versioning.json url")

        self.search_repo_button = QPushButton("Start")


        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.ensureCursorVisible()
        self.output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


        self.dropdown_label = QLabel("Select a source (must be installed on your Paperback app):")

        self.source_select_dropdown = QComboBox()

        self.start_on_source_button = QPushButton("Start diagnosing source")

        # Parent to layouts
        self.frame_1_layout.addWidget(self.input_label)
        self.frame_1_layout.addWidget(self.input_text)
        self.frame_1_layout.addWidget(self.search_repo_button)
        self.frame_2_layout.addWidget(self.dropdown_label)
        self.frame_2_layout.addWidget(self.source_select_dropdown)
        self.frame_2_layout.addWidget(self.start_on_source_button)
        self.layout.addLayout(self.main_content_layout)
        self.layout.addWidget(self.output)

        # Event listeners
        self.search_repo_button.clicked.connect(self.search_repo_button_clicked)
        self.start_on_source_button.clicked.connect(self.start_on_source_button_clicked)

    def highlight_last_output_line(self, color=QColorConstants.Red):
        self.highlight_format.setBackground(color)

        block = self.output.document().findBlockByLineNumber(self.output.document().lineCount() - 1)
        blockPos = block.position()

        cursor = QTextCursor(self.output.document())
        cursor.setPosition(blockPos)
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.setCharFormat(self.highlight_format)

    def _on_readyReadStandardOutput(self):
        data = self.process.readAllStandardOutput().data().decode(errors='ignore')
        print(data)
        self.output.append(data)
    def _on_readyReadStandardError(self):
        data = self.process.readAllStandardError().data().decode(errors='ignore')
        self.output.append(data)

    def _on_finished(self):
        self.process.kill()
        self.output.append("Diagnosis has finished. You can now close this window and send the most recently created json file for further analysis.")
        self.highlight_last_output_line(QColorConstants.Green)
        QApplication.instance().beep()

    def hookprocess_output(self):
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self._on_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self._on_readyReadStandardError)
        self.process.finished.connect(self._on_finished)

    def start_diagnosis(self):
        self.hookprocess_output()
        self.process.setArguments(['-s', path.join(base_dir, 'mitm_log_target.py')])
        self.process.setProgram('mitmdump')
        self.process.start()

        if not self.process.waitForStarted():
            self.output.append("Failed to start the diagnosis process.")
            return
        
        # There is a bug in PySide6 where part of the first stdout line is not captured. That is only done after more data is written to stdout.
        # Therefore we can only assume port 8080 is used for mitmproxy.
        # get the IP address of the machine

        self.output.append(f"mitmdump has started. Please make sure to set your device is connected to the same network as this computer, and the device's proxy is set to {get_internal_ip()}:8080")

    def start_on_source_button_clicked(self):
        self.start_on_source_button.setDisabled(True)
        self.source_select_dropdown.setDisabled(True)
        source_name = self.source_select_dropdown.currentText()
        source = self.repo_sources[source_name]
        self.output.append("")
        self.output.append(f"Selected source: {source['name']}")
        self.output.append(f"Source URL: {source['websiteBaseURL']}")
        self.output.append("Fetching source code...")

        response = req.get(self.repo_base_url + "/" + source['name'] + "/index.js")
        if response.status_code == 200:
            self.output.append("Successfully fetched source code.")
            urls = scrape_urls(response.text)
            self.output.append(f"Found {len(urls)} URLs in the source code.")
            self.output.append("URLs:")
            for url in urls:
                self.output.append("  > " + url)
            
            create_target_json(urls)

            self.start_diagnosis()
        else:
            self.output.append("Failed to fetch source code.")

    def search_repo_button_clicked(self):
        target_url = self.input_text.text()
        if not target_url or target_url.isspace():
            self.output.append("Please enter a valid URL.")
            self.highlight_last_output_line()
            QApplication.instance().beep()
            return
        else:
            self.search_repo_button.setDisabled(True)
            self.input_text.setDisabled(True)
            # make a request to the target_url
            if not "versioning.json" in target_url:
                # check for trailing slash
                if target_url[-1] != "/":
                    target_url += "/"
                target_url += "versioning.json"
            
            self.repo_base_url = re.sub(r"\/versioning\.json.*", "", target_url)
            self.output.append(f"Target URL: {self.repo_base_url}")
            self.output.append("Fetching versioning.json...")

            response = req.get(target_url)
            if response.status_code == 200:
                try:
                    data = response.json()

                    # find either types or commons
                    if "builtWith" in data:
                        if "types" in data['builtWith']:
                            versionKey = "types"
                        elif "commons" in data['builtWith']:
                            versionKey = "commons"
                        else:
                            versionKey = None
                    else:
                        versionKey = None

                    if versionKey is not None and not "0.8" in data['builtWith'][versionKey]:
                        self.output.append(f"Diagnosed the issue to be an outdated version of Paperback. Latest version is 0.8 (2024) while repository version is {data['builtWith'][versionKey]}")
                        
                        self.highlight_last_output_line()
                        
                        QApplication.instance().beep()
                        return
                    
                    for source in data['sources']:
                        self.repo_sources[source['name']] = source
                        self.source_select_dropdown.addItem(source['name'])
                except req.exceptions.JSONDecodeError:
                    self.output.append("Failed to fetch versioning.json.")
                    return

                self.output.append("Successfully fetched versioning.json.")

        self.main_content_layout.addLayout(self.frame_2_layout, 1)

def set_icons(app):
    if platform.system() == "Windows":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("me.ivanmatthew.paperback.selfdiagnosis")
    app_icon = QIcon(path.join(base_dir, 'app.ico'))
    app.setWindowIcon(app_icon)

def main():
    has_mitm = detect_mitm()

    if has_mitm:
        print("Mitmproxy is installed!")
        app = QApplication(sys.argv)
        set_icons(app)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

            # print()

            # json_payload = {
            #     "target_url": "https://example.com"
            # }

            # with open('latest.json', 'w') as file:
            #     file.write('{"target_url": "https://example.com"}') 
    else:
        # os = platform.system()
        # if os == "Windows":
        #     ctypes.windll.user32.MessageBoxW(0, "Mitmproxy is not installed. Please install it to use this tool.", "Mitmproxy Not Installed", 0)
        # elif os == "Darwin":
        #     subprocess.run(['osascript', '-e', f'display dialog "Mitmproxy is not installed. Please install it to use this tool." with title "Mitmproxy Not Installed"'], check=True)
        # else:
        #     print("For this tool to work, you will need to install mitmproxy.")
        QMessageBox.critical(None, "Mitmproxy Not Installed", "Mitmproxy is not installed. Please install it to use this tool.")
        sys.exit(1)

if __name__ == "__main__":
    main()
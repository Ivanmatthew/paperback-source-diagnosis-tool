import json
from mitmproxy.ctx import master
from mitmproxy.http import HTTPFlow
from shutil import move as rename_file
from pathlib import Path
from datetime import datetime
import signal


TARGET_FILE_NAME = 'latest.json'
target_file_path = Path(TARGET_FILE_NAME)

@staticmethod
def get_target_urls():
    if not target_file_path.exists() or not target_file_path.is_file():
        raise FileNotFoundError("File with target URLs not found. Did you run this script by itself?")
    with open(TARGET_FILE_NAME, 'r') as file:
        data = json.load(file)
        return data['target_urls']

@staticmethod
def write_logged_flows(logged_flows: list):
    serializable_flows = []
    for flow in logged_flows:
        serializable_flows.append({
            "request": {
                "url": flow['request'].url,
                "host": flow['request'].host,
                "port": flow['request'].port,
                "method": flow['request'].method,
                "scheme": flow['request'].scheme,
                "authority": flow['request'].authority,
                "path": flow['request'].path,
                "http_version": flow['request'].http_version,
                "headers": dict(flow['request'].headers),
                #"content": flow['request'].content.decode('utf-8') if flow['request'].content else None,
                "content": None,
                "trailers": dict(flow['request'].trailers) if flow['request'].trailers else None,
                "timestamp_start": flow['request'].timestamp_start,
                "timestamp_end": flow['request'].timestamp_end
            },
            "response": {
                "http_version": flow['response'].http_version,
                "status_code": flow['response'].status_code,
                "reason": flow['response'].reason,
                "headers": dict(flow['response'].headers),
                #"content": flow['response'].content.decode('utf-8') if flow['response'].content else None,
                "content": None,
                "trailers": dict(flow['response'].trailers) if flow['response'].trailers else None,
                "timestamp_start": flow['response'].timestamp_start,
                "timestamp_end": flow['response'].timestamp_end
            }
        })
        try:
            serializable_flows[-1]['request']['content'] = flow['request'].content.decode('utf-8')
        except UnicodeDecodeError:
            pass
        try:
            serializable_flows[-1]['response']['content'] = flow['response'].content.decode('utf-8')
        except UnicodeDecodeError:
            pass

    with open(target_file_path, 'r+') as file:
        original_data = json.load(file)
        original_data['logged_flows'] = serializable_flows
        file.seek(0) # Move the cursor to the beginning of the file, to overwrite the data.
        json.dump(original_data, file, indent=4)

    rename_file(target_file_path, Path(datetime.now().strftime("%d-%m-%Y-T%H-%M-%S") + '.json'))


interrupted = False
def interruption_handler(signum, frame):
    global interrupted
    interrupted = True
    signal.default_int_handler(signum, frame)

signal.signal(signal.SIGINT, interruption_handler)

def is_interrupted():
    return interrupted

class MitmLogTarget:
    def __init__(self):
        self.invalid_shutdown = True
        self.FLOWS_UNTIL_STOPPED = 20 # Will quit after 20 flows have been captured.
        self.logged_flows = []
        try:
            self.target_urls = get_target_urls()
            self.invalid_shutdown = False
        except FileNotFoundError:
            print("File with target URLs not found. Did you run this script by itself?")
            master.shutdown()

    async def response(self, flow: HTTPFlow) -> None:
        if self.invalid_shutdown:
            return

        if any(target_url in flow.request.url for target_url in self.target_urls):
            if len(self.logged_flows) > self.FLOWS_UNTIL_STOPPED:
                master.shutdown()
                return
            
            self.logged_flows.append({
                "request": flow.request,
                "response": flow.response
            })

    def done(self):
        if self.invalid_shutdown:
            print("Invalid shutdown detected. Exiting...")
            return

        if not is_interrupted():
            write_logged_flows(self.logged_flows)
            print("Flows logged succesfully.")
        else:
            print("The script was interrupted. No data will be saved.")

addons = [MitmLogTarget()]
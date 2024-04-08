# Paperback Self-Diagnosis Tool

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

The Paperback Self-Diagnosis Tool is a utility designed to assist users in identifying, resolving and properly reporting issues encountered while using the iOS Paperback manga reading app.

This tool does NOT guarantee or promise to fix all issues, but it aims to give source developers and users a better understanding of the problem they're experiencing.

This diagnosis tool is primarily focused on diagnosing source issues.

The tool is built to also work on other platforms, but only has documented support for Windows systems.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Building from Source](#building-from-source)
- [License](#license)

## Installation
### Pre-requisites
- Windows 7 or later
- Requires [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/) to be installed.

If you are unsure whether you have the prerequisities installed or not, you can find an executable on the [Releases](https://github.com/Ivanmatthew/paperback-source-diagnosis-tool/releases) page called 'prerequisite-setup.exe' to help you check and install the prerequisites.

### Installation Steps
1) Navigate to the [Releases](https://github.com/Ivanmatthew/paperback-source-diagnosis-tool/releases) page and download the latest (recommended) version of the Paperback Self-Diagnosis Tool.
2) Use the appropiate installer for your OS
3) Run the installer and follow the on-screen instructions
4) Once installed, run the Paperback Self-Diagnosis Tool (More information on how to use the tool can be found in the [Usage](#usage) section)

## Usage
### Pre-requisites
Before using the application, it is useful to already have the following things ready, as you will need them to properly diagnose the issue:
- A device with the Paperback app installed (screenshots are taken from an iPhone)
- A computer with the Paperback Self-Diagnosis Tool installed ([Installation](#installation))
- Both the devices on the same network
- The URL to the repository hosting the source you are having issues with

### Usage Steps
After installing the tool and starting it, you will be presented with a window that looks like the one shown below.
In thsi window, enter the repository URL of the source you are having issues with, and click the 'Start' button.
![Main Window](/readmeassets/mainscreen.png)

If everything's set up correctly, you should see a box appear with a list of sources you can choose from.
If this is not the case, it might be that you are using an outdated repository or an incorrect URL, you can see which one it is by looking at the text that will appear in the box.

Once you have selected a source, you can click on 'Start diagnosing source' to start the diagnosis process.
![Source Selection](/readmeassets/sourceselect.png)

In the example shown below, the source 'RizzComic' was selected, you can see the box displaying some inforamtion, ending with text that says 'mitmdump has started. Please make sure to set...'

The following steps will require you to set up a proxy on your device with the details given in the box.
Ensure you remember the numbers starting with '192.168' until the :8080 part.
![Output direction](/readmeassets/outputdirections.png)

On your phone, navigate to the settings section and click on the 'Wi-Fi' option.
![Wi-Fi Settings](/readmeassets/iphonesettingswifimenu.png)

Then head to the current Wi-Fi network you are connected to and click on the 'i' icon.
![Wi-Fi Network](/readmeassets/iphonesettingswifiselect.png)

Scroll down to the 'HTTP Proxy' section and click on 'Configure Proxy'.
![HTTP Proxy](/readmeassets/iphonesettingsproxyselect.png)

Select 'Manual' and enter the numbers you remembered from the box (excluding the :8080 part) in the 'Server' field and '8080' in the 'Port' field.
After entering the details, click on 'Save' and navigate to the Paperback app.
![Manual Proxy](/readmeassets/iphoneselectproxy.png)
![Manual Proxy Details](/readmeassets/iphoneinputproxy.png)

In the Paperback app, interact with the source you are having issues with. Until you see the following on your computer screen:
![Diagnosis Complete](/readmeassets/outputdirections2.png)

You have now successfully diagnosed the source issue. You can send the generated file to the source developer for further analysis.
The generated file will have the date and time stamped to it, as shown in the example below of the file explorer. (For you it may or may not say .json at the end)
![Output File](/readmeassets/explorerjsonview.png)


## Building from Source
### Pre-requisites
- Between Python 3.12 and 3.13
- Windows 7 or later
- Poetry (as a dependency manager)

### Building Steps
Because it is a python script, you can simply run it directly with python.
To ensure you have all the dependencies, you can use Poetry to install them.
```bash
poetry install
```
Then you can run it with
```bash
cd advanced_self_diagnosis
python main.py
```

## License

This project is licensed under the [MIT License](LICENSE).
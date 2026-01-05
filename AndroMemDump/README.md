# MemoryTool

> **Master's degree in Computer Engineering, Cybersecurity and Artificial Intelligence - University of Cagliari**

> **Thesis**

> **Authors**: Federico Moro 


***
# Table of Contents
1. [Overview](#overview)
2. [Project Structure](##project_structure)
3. [Installation](#installation)
4. [Use](#use)
5. [Helpful Links](##helpful_links)

***

## Overview
The Memorytool tool is designed to perform RAM memory acquisition of an emulated AVD device via the Android SDK suite. Key features include:
- Creation and configuration of custom AVDs;
- Management of created AVDs, with the possibility to delete them;
- Installation of applications via .apk files;
- Dumping of RAM memory, the main functionality of the tool.

The main objective of Memorytool is to support the forensic analysis of virtual devices by automating the RAM acquisition process. This procedure can be performed in two ways:
1. Full memory dump, using the LiME module.
2. Targeted acquisition of a single process, using the Frida tool.


## Project Structure

  ```bash
    /memorytool
      ├── apk_file/              # Contains APK files for app installations
      ├── dump/                  # Stores memory dump files
      ├── files/                 # Contains additional resources or data files
      ├── graphics/              # Manages graphical elements and UI components
      ├── modules/               # Handles AVD creation, deletion, and app installation
      ├── ram/                   # Contains Python scripts for memory acquisition functionalities
      ├── utils/                 # Utility scripts for various helper functions
      ├── requirements.txt       # Lists dependencies required for the project
      ├── README.md              # This README file
      └── main.py                # Main script to run the tool
  ```


## Installation

- Download the ZIP code or clone the repository with
  ```bash
  git clone https://github.com/Federico0307/memorytool.git
  ```
  
### Software Dependencies

- **Python 3**: This project is developed using Python 3. Please ensure that Python 3 is installed on your system.
- **pip 3**: Python's package manager, pip 3, is required to install the Python dependencies for the project.
- **Git**: Git is required for version control and to clone this repository.
- **Java**: Java is required for specific functionality in the project.

### Installation Instructions

#### Python3
```bash
  python3 --version
```
If it is not installed, you can download it from the official site:
[Python3 Official site](https://www.python.org/downloads/)

#### Pip3
```bash
  pip3 --version
```
If it is not installed, you can download it from the official site:
```bash
  python3 -m ensurepip --upgrade
```

#### Git
```bash
  git --version
```
If it is not installed, you can download it from the official site:
[Git Official site](https://git-scm.com/downloads)

#### Java
```bash
  java --version
```
If it is not installed, you can download it from the official site:
[Java Official site](https://www.oracle.com/it/java/technologies/downloads/)

### Frida
Install Frida and its tools with

```bash
pip3 install --target=~/Downloads/frida frida
pip3 install --target=~/Downloads/frida frida-tools
```
Download the correct version of frida-server for your device (frida-server-<frida's version>-android-<android's architecture of your mobile>) from
[Frida](https://github.com/frida/frida/releases), unzip the file and rename it as 'frida-server'.

### Fridump
Install Fridump with

```bash
git clone https://github.com/Nightbringer21/fridump.git ~/Downloads/
```

### Requirements

Install the requirements with

```bash
pip3 install -r requirements.txt
```
  
### Instructions

Follow the guide into repository
- Choose a proper kernel based on AVD'Android OS version
- Choose a proper compilator base on PC OS where you will compile the kernel
- Download and compile LiME module

After all of these procedures include in project repository, into /files, the compiled kernel (it has to be rename in 'ranchu-kernel') and the lime-goldfish.ko file of LiME after compilation.
It is important becuse the tool will search these files into this folder.
Add the desired .apk file into /apk_file 

## Use

Modify the file utils/config.py based on your configuration.
- It is possible choose API, ARCH of Android OS version
- Specify SDK folder path
- Specify AVD folder path

## Helpful Links

- [Android Command Line Tools](https://developer.android.com/studio)
- [Volatility's Guide](https://github.com/volatilityfoundation/volatility/wiki/Android)
- [LiME module](https://github.com/504ensicsLabs/LiME)
- [Frida](https://github.com/frida/frida)

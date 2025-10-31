# EpicSevenAssetRipper

> [!TIP]
> This tool supports both Epic Seven (E7) and Chaos Zero Nightamre (CZN)

<img width="900" height="730" alt="image" src="https://github.com/user-attachments/assets/a93be0ba-4a35-4ce0-b10f-9183099587a8" />

# Installation:

## Requirements
Python 3+

## How to install

[Download the latest version](https://github.com/CeciliaBot/EpicSevenAssetRipper/releases/latest) and extract all the files in a folder of your choice.

Open the command prompt (hold shift + right click inside the folder -> Power Shell on windows) and type

    pip install -r requirements.txt

This should take care of all the dependencies required

Now you can double click main.py or type py main.py in the command prompt to run the GUI

A folder named data.pack will be created, you can use this folder to organize your files or just ignore it


## SCT to PNG
To use the SCT to PNG 3 additional installations are required

    python3 -m pip install --upgrade Pillow

    python3 -m pip install texture2ddecoder

    python3 -m pip install lz4

# How to Use
<img width="900" height="730" alt="image" src="https://github.com/user-attachments/assets/00d005f6-f7c7-43db-8258-8ce088d7938d" />

1. Select the data.pack to use (this tool supports data.pack, .tar, .zip (No password)
2. Generate file tree or load file tree from json file. After generating this tool will automatically save the result to tree.json in the same folder as the data.pack, this tool will also try to automatically load the "tree.json" file in the same directory as the data.pack
3. All the assets inside the data.pack will now be displayed in the file tree. You can select and right click files to extract or preview. (You can enable automatic preview in the settings tab) Preview is only available for images only as of now.
4. (Optional) You can use the compare function to remove unchanged nodes when comparing to older file trees


# What's new in 2.0
SCT to PNG is now included, this hook allows to decode and convert sct and sct2 files to png

Multiselect in the file tree: you can hold CTRL + Left click to select different nodes in the file tree view

Reload hooks: Click the small refresh icon at the bottom right to relaod hooks (hooks dependencies wont be reloaded)

Settings tab: Here you can change some settings

Light and Dark themes: Improvments to the dark theme and new light theme

## Hooks

You can create your custom hooks to handle different file extensions. This tool provides the SCT to PNG and Webp loop hooks.

To create a hook create a python file named after the extension/file format you want to handle. Inside this file you need to define a maind function with one argument

```
def main(file):
  # the file argument is a class object
  content = file.bytes # -> This is a ByteArray which is a bytearray subclass with additional methods like seek, tell, read
  path = file.path # -> Destination path, set this to None if you want to prevent the default save function and handle it in your hook
  info = file.tree_file # -> The tree data
  thread = file.thread # -> You can check is_stopping() to check if the proccess was interrupted by the user or call progress((int, str)) NOTE: progress requires a tuple
  written = file.written # -> Check if the file has been written, this should be true if the hook is in the after_write folder
```

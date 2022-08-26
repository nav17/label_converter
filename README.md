# Label Converter

A simple GUI tool which formats and collates UK shipping labels generated from [Laced](https://www.laced.co.uk/) and [Alias](https://www.alias.org/) to print on thermal printers.

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/ss.png?raw=true)

## Usage
Simply choose the PDF files of the labels you want to print & submit

The tool will:
* Crop the shipping label and QR code to a standard 4x6" label size
* Darken the grey text which thermal printers struggle to display
* Collate all labels into single PDF
* Open new PDF with the default PDF viewer

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/ss2.png?raw=true)

## Prequisites
Requires Python 3.7 or above.

## Installation

Download the appropriate zip file for Windows or Mac.

* For Windows, open labelwin.exe to run the application. 
* For Mac, move the folder & app to your Applications folder.

It is recommended moving the extracted folder to an applications to prevent deleting necessary files by mistake.

Alternatively, use [pyinstaller](https://pyinstaller.org/) to generate the python app for your OS by running the following command 

```python
pyinstaller --onedir --windowed --icon="img/icon.png" "Label Converter.py"
```
# Label Converter

A simple GUI tool which crops, darkens and collates UK shipping labels from [Laced](https://www.laced.co.uk/), [Alias](https://www.alias.org/) and [StockX](https://www.stockx.com/) to print on thermal printers.

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/ss.png?raw=true)

## Usage
Simply choose the PDF files of the labels you want to print & submit

The tool will:
* Crop the shipping label and QR code to a standard 4x6" label size
* Darken the grey text which thermal printers struggle to display
* Collate all labels into single PDF
* Open new PDF with the default PDF viewer

Includes the option to auto-delete label files after submitting

For StockX labels which open as a web page you will need to print to PDF (right click -> Print -> change printer to PDF) to add them.

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/ss2.png?raw=true)

Try it out with the sample labels above!

## Prequisites
Requires Python 3.7 or above.

## Installation

Download the appropriate zip file for Windows or Mac.

* For Windows, open Label Converter.exe to run the application. 
* For Mac, move the folder & app to your Applications folder.

It is recommended moving the extracted folder to an applications to prevent deleting necessary files by mistake.

Alternatively, use [pyinstaller](https://pyinstaller.org/) to generate the python app by running the following command 

```python
pyinstaller --onedir --windowed --icon="img/icon.png" "Label Converter.py"
```

## Changelog
v0.2 - Added auto-delete option & unified scripts for both OS
v0.2.1 - Adjusted margins to match changes to laced labels
v0.3 - Added support for StockX and UPS Alias labels 
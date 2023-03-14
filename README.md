# Label Converter

A simple Python-based GUI tool which is designed to format and collate UK shipping labels from [Laced](https://www.laced.co.uk/), [Alias](https://www.alias.org/), [StockX](https://www.stockx.com/) and [Kick Game](https://www.kickgame.co.uk/) to a standard 4x6" label size for printing on thermal label printers.

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/tool.png?raw=true)

## Usage
To use the Label Converter tool, simply choose the PDF files of the labels you want to print and press "Submit". The tool will automatically perform the following functions:

* Crop the shipping label and QR code to a standard 4x6" label size
* Darken any grey text
* Collate all labels into a single PDF
* Open new PDF with the default PDF viewer

The tool also includes an option to automatically delete the label files after submission.

For StockX labels which open as a web page you will need to print to PDF (right click -> Print -> change printer to PDF) and ensure the PDF file name begins with 'StockX'

![Screenshot](https://github.com/nav17/label_converter/blob/master/img/example.png?raw=true)

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

v0.4 = Added support for Kick Game labels & Bug fixes
v0.3 - Added support for StockX and UPS Alias labels 
v0.2.1 - Adjusted margins to match changes to laced labels
v0.2 - Added auto-delete option & unified scripts for both OS
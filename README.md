## About PDFScrapper

PDFScrapper is a Python script designed to extract images from PDF files.

## Features

- Extract images from a single PDF file or multiple PDF files specified in a text file.
- Supports extracting images from specific pages or page ranges.
- Saves extracted images to the specified output directory.
- Extracts all images from every PDF file located within a specified directory 

### Prerequisites

- Python 3.x installed on your system.

## Installation Guide

```
git clone https://github.com/maniyaom/PDFScrapper
```

## Change Directory
```
cd PDFScrapper
```

## Recommended Python Version:

PDFScrapper currently supports **Python 3**.

* The recommended version for Python 3 is **3.7.x**

## Dependencies:

PDFScrapper depends on the `PyMuPDF`, `Pillow`, `Termcolor` and `Magic` python modules.

- `PyMuPDF` for working with PDF files.
- `Pillow` for image processing.
- `Termcolor` for colored output in the terminal.
- `Magic` for file type identification install the following libraries.

These dependencies can be installed using the requirements file:

- Installation on Windows or Linux:
```
pip install -r requirements.txt
```

Alternatively, each module can be installed independently as shown below.

#### PyMuPDF Module (https://pypi.org/project/PyMuPDF/)

- Install for Windows or Linux:
```
pip install PyMuPDF
```

#### Pillow Module (https://pypi.org/project/PyMuPDF/)

- Install for Windows or Linux:
```
pip install pillow
```

#### Termcolor Module (https://pypi.org/project/termcolor/)

- Install for Windows or Linux:
```
pip install termcolor
```

#### Magic Module (https://pypi.org/project/python-magic/)

- Install for Windows:
```
pip install python-magic-bin
```

- Install using pip on Linux:
```
sudo pip install python-magic
```

## Uninstallation
- For uninstall all the dependencies on Windows or Linux:
```
pip uninstall -r requirements.txt
```

## Usage

Options       | Description
------------- |-------------
-h, --help    | Show help menu
-d            | Input file path to extract images
-x            | Specify directory path to images from the all pdf from that directory
-o            | Output directory to save the extracted images
-n            | Specify the page number of the PDF
-r            | Specify a range of pages of the PDF
-f            | Specify a text file containing a list of PDF file paths

### Examples

* To list all the basic options and switches use -h switch:

```
python PDFScrapper.py -h
```

* To extract images from a PDF file:

```
python PDFScrapper.py -d D:\sample.pdf -o D:\images
```

* To extract images from a PDF file but extract images from specified page number:

```
python PDFScrapper.py -d D:\sample.pdf -o D:\images -n 3
```

* To extract images from a PDF file but extract images for a specified range of page number:

```
python PDFScrapper.py -d D:\sample.pdf -o D:\images -r 3-10
```

* Extracts all images from every PDF file located within a specified directory 

```
python PDFScrapper.py -x D:\sampledir -o D:\images
```

* To extract images from multiple PDF files :

```
python PDFScrapper.py -f D:\filenames.txt -o D:\images
```

* To extract images from multiple PDF files but for a specified range of page number:

```
python PDFScrapper.py -f D:\filenames.txt -o D:\images -r 4-19
```

## Example Text File
```
D:\sampledir\sample_1.pdf
D:\newdir\file_2.pdf
D:\otherdir\sample_2.pdf
C:\material\content.pdf
```

## License

PDFScrapper is licensed under the MIT License. take a look at the [LICENCE](https://github.com/maniyaom/PDFScrapper/blob/main/LICENSE) for more information.

## Author
* Om Maniya

## Version
**Current version is 1.0**
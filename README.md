# eSTAR File Conversion Tool
[![Build Windows Executable](https://github.com/hpfb-dgpsa/eSTAR-Conversion-Tool/actions/workflows/build-windows.yml/badge.svg)](https://github.com/hpfb-dgpsa/eSTAR-Conversion-Tool/actions/workflows/build-windows.yml)

## Overview
Python Conversion Tool is a file conversion tool that allows users to extract and organize embedded files from PDF and XML documents. It processes the attached files in a PDF, organizes them based on predefined chapter names, and extracts the attachments listed in the provided XML manifest into structured folders.
The tool supports the extraction of PDF, XML, and TXT files and will organize them into subfolders based on the content of the XML file and predefined mappings.

## Features:

•	Extracts embedded PDF and TXT files from a given PDF.
•	Organizes extracted files into subfolders based on XML manifest data.
•	Uses predefined chapter mappings for structured folder naming.
•	Provides clear error messages and warnings when files are open or unavailable.
•	Allows users to select files via a graphical file dialog.
•	Compresses extracted files into a zip archive after processing.


## How to Use:

1.	Launch the Tool:
     Run the Python app Conversion_Tool_PythonV4.exe to start the tool.
2.	Select Files:
    PDF File: A file dialog will appear prompting you to select a PDF file. 
    XML File: After selecting the PDF, the tool will prompt you to select the associated XML file. 
3.	Extraction and Folder Creation:
    The tool will extract the embedded files from the PDF and organize them based in the XML file.
    Files will be placed into specific folders based on the chapter name mappings provided in the code.
4.	Exported Files Location:
    The extracted files will be placed in a folder located at C:/Temp/Exported Files by default.
    After processing, the tool will zip the exported files into a .zip archive, stored in the path C:/Temp/Extracted_Files.zip.
5.	Complete the Process:
    Once the extraction is complete, you will receive a message box notification showing the location of the exported zip file.
    The original extracted files folder will be removed after the zip file is created.
6.	Error Handling:
    If a PDF file is open or locked, the tool will warn the user and prompt them to close the file before proceeding.
    If the XML file is invalid or cannot be parsed, the extraction process will be aborted.

## Troubleshooting:
1.	Error: "File is open. Please close the document to continue."
    This message appears if the selected PDF file is open. Please close the file and run the tool again.
2.	Error: "Invalid XML file. Extraction aborted."
    This indicates that the XML file you selected is not valid. Ensure that the file is well-formed and contains a valid <AttachmentManifest> section.



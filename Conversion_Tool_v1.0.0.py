# Conversion Tool: Diellza Mati v1.0.0
# Supports uploading .PDF and .XML files
# Extracts all .pdf and .txt files into designated folders and subfolders

#List of libraries used in the project below:

import os
import chardet
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox  # Import messagebox here
import xml.etree.ElementTree as ET
import re
import fitz  # PyMuPDF for PDF extraction


# Create a mapping for chapter names to subfolder names
chapter_name_mapping = {
    "CHAPTER 1": "1_REG ADMIN",
    "CH1.01": "1.01 Cover Letter",
    "CH1.02": "1.02 Submission ToC",
    "CH1.03": "1.03 List of Terms-Acronyms",
    "CH1.04": "1.04 Application Form-Administrative Info",
    "CH1.05": "1.05 Listing of Device(s)",
    "CH1.06": "1.06 QMS Full QS or Other Regulatory Certs",
    "CH1.07": "1.07 Free Sale Certificate",
    "CH1.08": "1.08 Expedited Review Documentation",
    "CH1.09": "1.09 User Fees",
    "CH1.10": "1.10 Pre-Submission Correspondence-Previous Regulator Interactions",
    "CH1.11": "1.11 Acceptance for Review Checklist",
    "CH1.12": "1.12 Statements-Certs-Decl of Conf",
    "CH1.12.01": "1.12.01 Performance-Voluntary Std",
    "CH1.12.02": "1.12.02 Enviro Assessment",
    "CH1.12.03": "1.12.03 Clinical Trial Certs",
    "CH1.12.04": "1.12.04 Indications w Rx and-or OTC",
    "CH1.12.05": "1.12.05 Truthful-Accurate Statement",
    "CH1.12.06": "1.12.06 USFDA Class III Summary and Cert",
    "CH1.12.07": "1.12.07 Decl of Conformity",
    "CH1.13": "1.13 Letters of Reference for Master Files",
    "CH1.14": "1.14 Letter of Authorization",
    "CH1.15": "1.15 Other Regional Administrative Info",
    "CHAPTER 2": "2_CONTEXT",
    "CH2.01": "2.01 Chapter ToC",
    "CH2.02": "2.02 General Summary of Submission",
    "CH2.03": "2.03 Summary-Certifications for Premarket Submissions",
    "CH2.04": "2.04 Device Description",
    "CH2.04.01": "2.04.01 Comprehensive Device Desc-Principle of Op",
    "CH2.04.02": "2.04.02 Description of Device Packaging",
    "CH2.04.03": "2.04.03 History of Development",
    "CH2.04.04": "2.04.04 Ref-Comparison to Similar and-or Previous Gen",
    "CH2.04.05": "2.04.05 Substantial Equivalence Discussion",
    "CH2.05": "2.05 Indications-Intended Use-Contraindications",
    "CH2.05.01": "2.05.01 Intended Use and Indications",
    "CH2.05.02": "2.05.02 Intended Environment-Setting",
    "CH2.05.03": "2.05.03 Pediatric Use",
    "CH2.05.04": "2.05.04 Contraindications",
    "CH2.06": "2.06 Global Market History",
    "CH2.06.01": "2.06.01 Global Market History",
    "CH2.06.02": "2.06.02 Global Incident Reports-Recalls",
    "CH2.06.03": "2.06.03 Sales Incident-Recall Rates",
    "CH2.06.04": "2.06.04 Evaluation-Inspection Reports",
    "CH2.07": "2.07 Other Submission Context Info",
    "CHAPTER 3": "3_NON-CLIN",
    "CH3.01": "3.01 Chapter ToC",
    "CH3.02": "3.02 Risk Management",
    "CH3.03": "3.03 Essential Principles (EP) Checklist",
    "CH3.04": "3.04 Standards",
    "CH3.04.01": "3.04.01 List of Standards",
    "CH3.04.02": "3.04.02 Declaration and-or Certification of Conformity",
    "CH3.05": "3.05 Studies",
    "CH3.05.01": "3.05.01 Physical-Mechanical",
    "CH3.05.01.01": "3.05.01.01 [Custom]",
    "CH3.05.01.01.01": "3.05.01.01.01 Summ",
    "CH3.05.01.01.02": "3.05.01.01.02 Report",
    "CH3.05.01.01.03": "3.05.01.01.03 Data",
    "CH3.05.02": "3.05.02 Chemical-Material",
    "CH3.05.02.01": "3.05.02.01 [Custom]",
    "CH3.05.02.01.01": "3.05.02.01.01 Summ",
    "CH3.05.02.01.02": "3.05.02.01.02 Report",
    "CH3.05.02.01.03": "3.05.02.01.03 Data",
    "CH3.05.03": "3.05.03 Electrical Systems",
    "CH3.05.03.01": "3.05.03.01 [Custom]",
    "CH3.05.03.01.01": "3.05.03.01.01 Summ",
    "CH3.05.03.01.02": "3.05.03.01.02 Report",
    "CH3.05.03.01.03": "3.05.03.01.03 Data",
    "CH3.05.04": "3.05.04 Radiation Safety",
    "CH3.05.04.01": "3.05.04.01 [Custom]",
    "CH3.05.04.01.01": "3.05.04.01.01 Summ",
    "CH3.05.04.01.02": "3.05.04.01.02 Report",
    "CH3.05.04.01.03": "3.05.04.01.03 Data",
    "CH3.05.05": "3.05.05 Software-Firmware",
    "CH3.05.05.01": "3.05.05.01 Description",
    "CH3.05.05.02": "3.05.05.02 Hazard Analysis",
    "CH3.05.05.03": "3.05.05.03 SRS",
    "CH3.05.05.04": "3.05.05.04 Architecture",
    "CH3.05.05.05": "3.05.05.05 SDS",
    "CH3.05.05.06": "3.05.05.06 Traceability Analysis",
    "CH3.05.05.07": "3.05.05.07 Softw Life Cycle Process Desc",
    "CH3.05.05.08": "3.05.05.08 Software V-V",
    "CH3.05.05.08.01": "3.05.05.08.01 [Custom]",
    "CH3.05.05.08.01.01": "3.05.05.08.01.01 Summ",
    "CH3.05.05.08.01.02": "3.05.05.08.01.02 Report",
    "CH3.05.05.08.01.03": "3.05.05.08.01.03 Data",
    "CH3.05.05.09": "3.05.05.09 Revision Level History",
    "CH3.05.05.10": "3.05.05.10 Unresolved Anomalies",
    "CH3.05.05.11": "3.05.05.11 Cybersecurity",
    "CH3.05.05.12": "3.05.05.12 Interoperability",
    "CH3.05.06": "3.05.06 Biocomp-Toxicology",
    "CH3.05.06.01": "3.05.06.01 [Custom]",
    "CH3.05.06.01.01": "3.05.06.01.01 Summ",
    "CH3.05.06.01.02": "3.05.06.01.02 Report",
    "CH3.05.06.01.03": "3.05.06.01.03 Data",
    "CH3.05.07": "3.05.07 Pyrogenicity",
    "CH3.05.07.01": "3.05.07.01 [Custom]",
    "CH3.05.07.01.01": "3.05.07.01.01 Summ",
    "CH3.05.07.01.02": "3.05.07.01.02 Report",
    "CH3.05.07.01.03": "3.05.07.01.03 Data",
    "CH3.05.08": "3.05.08 Bio Material Safety",
    "CH3.05.08.01": "3.05.08.01 Certificates",
    "CH3.05.08.02": "3.05.08.02 [Custom]",
    "CH3.05.08.02.01": "3.05.08.02.01 Summ",
    "CH3.05.08.02.02": "3.05.08.02.02 Report",
    "CH3.05.08.02.03": "3.05.08.02.03 Data",
    "CH3.05.09": "3.05.09 Sterility",
    "CH3.05.09.01": "3.05.09.01 End-User",
    "CH3.05.09.01.01": "3.05.09.01.01 [Custom]",
    "CH3.05.09.01.01.01": "3.05.09.01.01.01 Summ",
    "CH3.05.09.01.01.02": "3.05.09.01.01.02 Report",
    "CH3.05.09.01.01.03": "3.05.09.01.01.03 Data",
    "CH3.05.09.02": "3.05.09.02 Manufacturer",
    "CH3.05.09.02.01": "3.05.09.02.01 [Custom]",
    "CH3.05.09.02.01.01": "3.05.09.02.01.01 Summ",
    "CH3.05.09.02.01.02": "3.05.09.02.01.02 Report",
    "CH3.05.09.02.01.03": "3.05.09.02.01.03 Data",
    "CH3.05.09.03": "3.05.09.03 Residual Tox",
    "CH3.05.09.3.01": "3.05.09.3.01 [Custom]",
    "CH3.05.09.3.01.01": "3.05.09.3.01.01 Summ",
    "CH3.05.09.3.01.02": "3.05.09.3.01.02 Report",
    "CH3.05.09.3.01.03": "3.05.09.3.01.03 Data",
    "CH3.05.09.4": "3.05.09.4 Clean-Disinfect Val",
    "CH3.05.09.4.01": "3.05.09.4.01 [Custom]",
    "CH3.05.09.4.01.01": "3.05.09.4.01.01 Summ",
    "CH3.05.09.4.01.02": "3.05.09.4.01.02 Report",
    "CH3.05.09.4.01.03": "3.05.09.4.01.03 Data",
    "CH3.05.09.5": "3.05.09.5 Reprocessing of SUDs",
    "CH3.05.09.5.01": "3.05.09.5.01 [Custom]",
    "CH3.05.09.5.01.01": "3.05.09.5.01.01 Summ",
    "CH3.05.09.5.01.02": "3.05.09.5.01.02 Report",
    "CH3.05.09.5.01.03": "3.05.09.5.01.03 Data",
    "CH3.05.10": "3.05.10 Animal Testing",
    "CH3.05.10.01": "3.05.10.01 [Custom]",
    "CH3.05.10.01.01": "3.05.10.01.01 Summ",
    "CH3.05.10.01.02": "3.05.10.01.02 Report",
    "CH3.05.10.01.03": "3.05.10.01.03 Data",
    "CH3.05.11": "3.05.11 Usability-Human Factors",
    "CH3.05.11.01": "3.05.11.01 [Custom]",
    "CH3.05.11.01.01": "3.05.11.01.01 Summ",
    "CH3.05.11.01.02": "3.05.11.01.02 Report",
    "CH3.05.11.01.03": "3.05.11.01.03 Data",
    "CH3.06": "3.06 Non-Clin Bibliography",
    "CH3.07": "3.07 Expiration Period-Package Val",
    "CH3.07.01": "3.07.01 Product Stability",
    "CH3.07.01.01": "3.07.01.01 [Custom]",
    "CH3.07.01.01.01": "3.07.01.01.01 Summ",
    "CH3.07.01.01.02": "3.07.01.01.02 Report",
    "CH3.07.01.01.03": "3.07.01.01.03 Data",
    "CH3.07.02": "3.07.02 Package Val",
    "CH3.07.02.01": "3.07.02.01 [Custom]",
    "CH3.07.02.01.01": "3.07.02.01.01 Summ",
    "CH3.07.02.01.02": "3.07.02.01.02 Report",
    "CH3.07.02.01.03": "3.07.02.01.03 Data",
    "CH3.08": "3.08 Other Non-Clin Evidence",
    "CH3.08.01": "3.08.01 [Custom]",
    "CH3.08.01.01": "3.08.01.01 Summ",
    "CH3.08.01.02": "3.08.01.02 Report",
    "CH3.08.01.03": "3.08.01.03 Data",
    "CHAPTER 4": "4_CLINICAL",
    "CH4.01": "4.01 Chapter ToC",
    "CH4.02": "4.02 Overall Clinical Evidence Summary",
    "CH4.02.01": "4.02.01 Clinical Evaluation Report",
    "CH4.02.02": "4.02.02 Device Specific",
    "CH4.02.02.01": "4.02.02.01 [Trial details]",
    "CH4.02.02.01.01": "4.02.02.01.01 Synopsis",
    "CH4.02.02.01.02": "4.02.02.01.02 Report",
    "CH4.02.02.01.03": "4.02.02.01.03 Data",
    "CH4.02.03": "4.02.03 Lit Review-Other Known Info",
    "CH4.03": "4.03 IRB Approved Informed Consent Forms",
    "CH4.04": "4.04 Investigators Sites-IRB Contact Info",
    "CH4.05": "4.05 Other Clinical Evidence",
    "CH4.05.01": "4.05.01 [Custom]",
    "CH4.05.01.01": "4.05.01.01 Summ",
    "CH4.05.01.02": "4.05.01.02 Report",
    "CH4.05.01.03": "4.05.01.03 Data",
    "CHAPTER 5": "5_LABELLING",
    "CH5.01": "5.01 Chapter ToC",
    "CH5.02": "5.02 Product-Package Labels",
    "CH5.03": "5.03 Package Insert-Instructions for Use",
    "CH5.04": "5.04 e-labelling",
    "CH5.05": "5.05 Physician Labelling",
    "CH5.06": "5.06 Patient Labelling",
    "CH5.07": "5.07 Technical-Operator Manual",
    "CH5.08": "5.08 Patient File Stickers-Cards-Implant Registration Cards",
    "CH5.09": "5.09 Product Brochures",
    "CH5.10": "5.10 Other Labelling-Promotional Material",
    "CHAPTER 6A": "6A_QMG PROCEDURES",
    "CH6A.01": "6A.01 Cover Letter",
    "CH6A.02": "6A.02 Chapter ToC",
    "CH6A.03": "6A.03 Administrative",
    "CH6A.03.1": "6A.03.1 Product Descriptive Info",
    "CH6A.03.2": "6A.03.2 General Manufacturing Info",
    "CH6A.03.3": "6A.03.3 Required Forms",
    "CH6A.04": "6A.04 QMS procedures",
    "CH6A.05": "6A.05 Management responsibilities procedures",
    "CH6A.06": "6A.06 Resource management procedures",
    "CH6A.07": "6A.07 Prod realization procedures",
    "CH6A.08": "6A.08 Design-develop procedures",
    "CH6A.09": "6A.09 Purchasing procedures",
    "CH6A.10": "6A.10 Production-service ctrls procedures",
    "CH6A.11": "6A.11 Ctrl monitoring-measuring procedures",
    "CH6A.12": "6A.12 QMS measurement analysis-improvement procedures",
    "CH6A.13": "6A.13 Other QS Procedures Info",
    "CHAPTER 6B": "6B_QMS DEVICE SPECIFIC",
    "CH6B.01": "6B.01 Chapter ToC",
    "CH6B.02": "6B.02 QMS info",
    "CH6B.03": "6B.03 Management responsibilities info",
    "CH6B.04": "6B.04 Resource management info",
    "CH6B.05": "6B.05 Device Specific Quality Plan",
    "CH6B.06": "6B.06 Prod realization info",
    "CH6B.07": "6B.07 Design-devel info",
    "CH6B.08": "6B.08 Purchasing info",
    "CH6B.09": "6B.09 Production-serv ctrls",
    "CH6B.10": "6B.10 Ctrl monitoring-measuring info",
    "CH6B.11": "6B.11 QMS measurement analysis-improvement info",
    "CH6B.12": "6B.12 Other Device Specific QMS info"
}


# Function to check if a file is open or locked
def is_file_open(file_path):
    try:
        with open(file_path, 'r+'):
            return False  # File is not open
    except IOError:
        return True  # File is locked or in use

# Function to display a message box if the file is open
def show_message_for_open_pdf(pdf_path):
    if is_file_open(pdf_path):
        messagebox.showwarning(
            "File Open Warning", 
            f"The file {os.path.basename(pdf_path)} is open. Please close the document to continue. You may restart the process once it's closed."
        )



# Function to select files using a file dialog
def select_file(title, file_type):
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title=title, filetypes=[(file_type, f"*.{file_type.lower()}")])
    return file_path

# Check if XML is valid
def is_valid_xml(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        ET.fromstring(content)
        return True
    except Exception as e:
        print(f"Error in XML file: {e}")
        return False

# Extract embedded files from PDF file
def extract_from_pdf(pdf_path, output_dir):
    pdf_file = fitz.open(pdf_path)
    
    # Checking the files attached to the PDF file
    for i in range(pdf_file.embfile_count()):
        file_info = pdf_file.embfile_info(i)  
        file_name = file_info['filename']  # Extract file name
        file_data = pdf_file.embfile_get(i)  # Extract the actual file data of the pdf or txt
        
        # Save the embedded file to the output directory
        output_file_path = os.path.join(output_dir, file_name)
        with open(output_file_path, 'wb') as f:
            f.write(file_data)
            print(f"Extracted: {file_name} to {output_file_path}")

    pdf_file.close()

def extract_attachments(xml_path, pdf_path, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    if not is_valid_xml(xml_path):
        print("Invalid XML file. Extraction aborted.")
        return

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return

    # Extract files from the PDF itself
    extract_from_pdf(pdf_path, output_directory)

    # Get the AttachmentManifest from XML
    manifest = root.find('.//AttachmentManifest')
    if manifest is not None:
        attachments_str = manifest.text.strip()

        # Extract file info from the manifest using regex
        pattern = r'<<([^|]+)\|([^>]+)>>'
        attachments = re.findall(pattern, attachments_str)

        # Process each attachment found
        for file_name, folder_path in attachments:
            clean_folder_path = folder_path.strip('/')

            # Verify that the folder path matches the chapter mapping
            chapter_parts = clean_folder_path.split('/')
            mapped_parts = [chapter_name_mapping.get(part.strip(), part.strip()) for part in chapter_parts]
            subfolder_name = '/'.join(mapped_parts)  
            
            if subfolder_name:
                full_folder_path = os.path.join(output_directory, subfolder_name)
                os.makedirs(full_folder_path, exist_ok=True)
                
                # Checking if the file has already been extracted from the PDF
                extracted_file_path = os.path.join(output_directory, file_name.strip())
                if os.path.exists(extracted_file_path):
                    # Move or copy the extracted file into the correct subfolder
                    destination_path = os.path.join(full_folder_path, file_name.strip())
                    shutil.move(extracted_file_path, destination_path)
                    print(f"Exported into: {file_name.strip()} to {destination_path}")
                else:
                    print(f"Attachment file does not exist: {extracted_file_path}")
            else:
                print(f"No matching subfolder for: {clean_folder_path}")

    else:
        print("No AttachmentManifest found in the XML.")

    # Save the original PDF file to the specified folder only
    pdf_destination_folder = os.path.join(output_directory, "1_REG ADMIN", "1.04 Application Form-Administrative Info")
    os.makedirs(pdf_destination_folder, exist_ok=True)
    pdf_destination_path = os.path.join(pdf_destination_folder, os.path.basename(pdf_path))
    
    # Copy the PDF file to the desired location
    shutil.copy(pdf_path, pdf_destination_path)
    print(f"Saved PDF to: {pdf_destination_path}")


def main():
    pdf_file = select_file("Select PDF File", "PDF")
    if not pdf_file:
        print("No PDF file selected. Exiting.")
        return

    xml_file = select_file("Select XML File", "XML")
    if not xml_file:
        print("No XML file selected. Exiting.")
        return

    # Location of the exported files: output of the extracted attachments
    output_path = "C:/Temp/Exported Files"
    extract_attachments(xml_file, pdf_file, output_path)

    # Zip file location
    zip_file_path = 'C:/Temp/Extracted_Files.zip'

    # Function to create a zip file of the extracted folder
    def zip_extracted_folder(folder_path, zip_file_path):
        # Create a zip archive of the extracted folder
        shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', folder_path)

    # Call the function to zip the folder after extracting files
    zip_extracted_folder(output_path, zip_file_path)

    # Remove the exported files folder after zipping
    shutil.rmtree(output_path)

    # Show message after extraction
    messagebox.showinfo("Export Successful", f"The exported files are located at: {zip_file_path}")

if __name__ == "__main__":
    main()


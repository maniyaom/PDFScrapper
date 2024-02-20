import io
import os
import fitz 
import magic
from PIL import Image
from termcolor import colored

# filepath parameter is absolute path
def validate_file_path(filepath,forPDF=False,forTxt=False):
    if forTxt == True:
        if os.path.isfile(filepath):
            mime = magic.Magic(mime=True)
            file_format = mime.from_file(filepath)

            if file_format == 'text/plain':
                return True
            else:
                return "[-] Provided File is not a text file or It is empty !!"
        else:
            return "[-] Text File doesn't exist !!\n"
        
    elif forPDF == True:
        if os.path.isfile(filepath):
            mime = magic.Magic(mime=True)
            file_format = mime.from_file(filepath)

            if file_format == 'application/pdf':
                return True
            else:
                return "[-] Provided File is not a pdf file !!"
        else:
            return "[-] pdf File doesn't exist !!\n"

# Text file path is validated and it is absolute path
def extract_filepaths_from_textfile(textfile):
    filename_list = None
    with open(textfile,'r') as f:
        lst = [i.strip() for i in f.readlines()]
    filename_list = [i for i in lst if i!='']
    
    if len(filename_list) == 0:
        print(colored("[-] The given text file is empty\n",'red',attrs=['bold']))
        exit(0)
    else:
        return filename_list

# Directory path is validated and it is absolute path
def extract_filepaths_from_directory(dirpath):
    l = os.listdir(dirpath)
    d = []
    for i in l:
        filepath = os.path.join(dirpath,i)
        if validate_file_path(filepath,forPDF=True) == True:
            d.append(filepath)
    
    if len(d) == 0:
        print(colored(f"[-] There are no PDF files in this directory : {dirpath}\n",'red',attrs=['bold']))
        exit(0)
    else:
        return d

def extract_images(input_file_path,output_path,pagenumber,pagerange,output_format):

    # Fatches Images from a single page in a pdf
    if pagenumber != None:
        total = 0
        pdf_file = fitz.open(input_file_path)

        if pagenumber > len(pdf_file):
            print(colored(f"[-] Page number {pagenumber} is not found in the PDF File : {input_file_path}\n",'red',attrs=['bold']))
            return 0
        
        print(colored(f"Extracting Images from file : {input_file_path}\n",'green',attrs=['bold']))
        page = pdf_file[pagenumber - 1]
        image_list = page.get_images(full=True)

        if image_list:
            total += len(image_list)

            if not os.path.isdir(output_path) and total > 0:
                os.makedirs(output_path)
            
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                image.save(open(os.path.join(output_path, f"page{pagenumber}_image{image_index}.{output_format}"), "wb"),format=output_format.upper())

            print(colored(f"[+] Found a total of {len(image_list)} images in page {pagenumber}\n", 'green',attrs=['bold']))

        else:
            print(colored(f"[-] No images found on page {pagenumber}\n", 'red'))
        
        if total > 0:
            print(colored(f"[+] Images Stored at location : {output_path}\n", 'yellow', attrs=['bold']))
        return total
    
    else:
        total = 0
        pdf_file = fitz.open(input_file_path)

        start_page = 0
        end_page = len(pdf_file)

        # If page range is given we will iterate the loop over the defined page range
        if pagerange != None:
            start_page = pagerange[0] - 1
            end_page = pagerange[1]

        print(colored(f"Extracting Images from file : {input_file_path}\n",'green',attrs=['bold']))
        for page_index in range(start_page,end_page):

            if page_index + 1 > len(pdf_file):
                print(colored(f"\n[-] There are only {len(pdf_file)} pages in the PDF File : {input_file_path}",'red',attrs=['bold']))
                break
            
            page = pdf_file[page_index]

            image_list = page.get_images(full=True)

            if image_list:
                total += len(image_list)

                if not os.path.exists(output_path) and total > 0:
                    os.makedirs(output_path)
                
                for image_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(open(os.path.join(output_path, f"page{page_index + 1}_image{image_index}.{output_format}"), "wb"),format=output_format.upper())

                print(colored(f"[+] Found a total of {len(image_list)} images in page {page_index + 1}", 'green'))

            else:
                print(colored(f"[-] No images found on page {page_index + 1}", 'red'))
        
        print(colored(f"\n[+] Total Images found : {total}\n", 'green', attrs=['bold']))
        if total > 0:
            print(colored(f"[+] Images Stored at location : {output_path}\n\n", 'yellow', attrs=['bold']))
        return total

def extract_images_from_multiple_pdfs(filename_list,output_path,pagenumber,pagerange,output_format):
    total = 0
    if os.path.isdir(output_path) == False:
        os.makedirs(output_path)

    j = 0
    for i in filename_list:
        # Fetches List of directories in output path
        j += 1
        input_file_path = os.path.abspath(i)
        print(colored(f"File : [{j}]",'cyan',attrs=['bold']))
        
        input_file_name = os.path.basename(input_file_path)

        tempdir = os.path.join(output_path,input_file_name)

        if os.path.isdir(tempdir):
            k = 1
            while True:
                temp_input_file_name = input_file_name + '-' + str(k)
                tempdir = os.path.join(output_path,temp_input_file_name)

                if not os.path.isdir(tempdir):
                    input_file_name = temp_input_file_name
                    break
                k += 1

        if validate_file_path(input_file_path,forPDF=True) == True:
            output_dir_path = os.path.join(output_path,input_file_name)
            total += extract_images(input_file_path,output_dir_path,pagenumber,pagerange,"png")
        else:
            print(colored(f"[-] PDF File does not exists at location: {input_file_path}\n",'red',attrs=['bold']))
        
        
    print(colored(f"\nSummary:\n\n[+] Total Images found : {total}\n",'yellow',attrs=['bold']))
    
    if len(os.listdir(output_path)) == 0:
        os.rmdir(output_path)
    else:
        print(colored(f"[+] Images Stored at location : {output_path}\n",'yellow',attrs=['bold']))
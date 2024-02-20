import argparse
import os
from termcolor import colored
import functions

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        usage = colored(super()._format_usage(usage, actions, groups, prefix) + '\n\nUse -h or --help for more information\n\n', 'yellow', attrs=['bold'])
        return usage

banner = '''

██████╗ ██████╗ ███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝██║  ██║█████╗      ███████╗██║     ██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
██╔═══╝ ██║  ██║██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
██║     ██████╔╝██║         ███████║╚██████╗██║  ██║██║  ██║██║     ██║     ███████╗██║  ██║
╚═╝     ╚═════╝ ╚═╝         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                  
            # Coded by - Om Maniya - github.com/maniyaom                                                           
'''

parser = argparse.ArgumentParser(description='PDFScrapper is a Python script designed to extract images from PDF files',formatter_class=CustomHelpFormatter)

input_group = parser.add_mutually_exclusive_group(required=True)
pdf_page_group = parser.add_mutually_exclusive_group()

input_group.add_argument('-d','--pdf-file',metavar="<pdf-file-path>",type=str,help='Input file path to extract images')
input_group.add_argument('-f','--text-file',metavar='<text-file-path>',type=str,help='Specify Text file containing list of pdf file paths')
input_group.add_argument('-x','--dir',metavar='<directory-path>',type=str,help='Extracts all images from every PDF file located within a specified directory')

parser.add_argument('-o','--output-dir',metavar='<output-directory-path>',type=str,help='Output directory to save the extracted images',required=True)

pdf_page_group.add_argument('-n','--pagenumber',metavar='<page-number>',type=int,help='Specify page number of PDF')
pdf_page_group.add_argument('-r','--pagerange',metavar='<page-range>',type=int,help='Specify range of pages of PDF (i.e. -r 3 7)',nargs='+')

print(banner)
args = parser.parse_args()

# Argument Validation
##############################################################################################
if args.pdf_file != None:
    stat = functions.validate_file_path(os.path.abspath((args.pdf_file).strip()),forPDF=True)
    if stat != True:
        print(parser.format_usage())
        print(colored(stat,'red',attrs=['bold']))
        exit(0)
elif args.text_file != None:
    stat = functions.validate_file_path(os.path.abspath((args.text_file).strip()),forTxt=True)
    if stat != True:    
        print(parser.format_usage())
        print(colored(stat,'red',attrs=['bold']))
        exit(0)
else:
    if not os.path.isdir(os.path.abspath((args.dir).strip())):
        print(parser.format_usage())
        print(colored(f"[-] Error : Directory : {os.path.abspath((args.dir).strip())} doesn't exist !!",'red',attrs=['bold']))
        exit(0)

if args.pagenumber != None:
    if args.pagenumber <= 0:
        print(parser.format_usage())
        print(colored(f"[-] Error : Invalid Page number : {args.pagenumber}\n",'red',attrs=['bold']))
        exit(0)

elif args.pagerange != None:
    if len(args.pagerange) == 2:
        if((args.pagerange[0] <= 0) or (args.pagerange[1] <= 0) or (args.pagerange[0] > args.pagerange[1])):
            print(parser.format_usage())
            print(colored(f"[-] Error : Invalid page range : {args.pagerange[0]} - {args.pagerange[1]}\n",'red',attrs=['bold']))
            exit(0)
    else:
        print(parser.format_usage())
        print(colored(f"[-] Error : Invalid page range\n",'red',attrs=['bold']))
        exit(0)


params = {
    'input_file' : os.path.abspath((args.pdf_file).strip()) if args.pdf_file is not None else None,
    'input_dir' : functions.extract_filepaths_from_directory(os.path.abspath((args.dir).strip())) if args.dir is not None else None,
    'output_dir' : os.path.abspath((args.output_dir).strip()),
    'pagenumber' : args.pagenumber if args.pagenumber is not None else None,
    'pagerange' : args.pagerange if args.pagerange is not None else None,
    'filename_list' : functions.extract_filepaths_from_textfile(os.path.abspath((args.text_file).strip())) if args.text_file is not None else None
}
#####################################################################################################

if os.path.isdir(os.path.abspath(params['output_dir'])) == False:
    print(colored(f'[-] Error : Output directory does not exists !!', 'red'))

    output_path = params['output_dir']
    x = input(f"Do you want to create directory for path : {output_path}? (y/n) : ").lower()
    if x == 'y':
        try:
            os.makedirs(output_path)
        except:
            print(colored(f"\n[-] Cannot Create Directory for the given path : {output_path}\n", 'red', attrs=['bold']))
            exit(0)
    else:
        exit(0)
    print()

output_path = os.path.abspath(params['output_dir'])

# Fetches List of directories in output path
k = 1
dir_name = 'Extracted-Images'
tempdir = os.path.join(output_path,dir_name)

if os.path.isdir(tempdir):
    while True:
        new_dir_name = dir_name + '-' + str(k)
        tempdir = os.path.join(output_path,new_dir_name)

        if not os.path.isdir(tempdir):
            dir_name = new_dir_name
            break
        k += 1

# Extraction of Images
if params['input_dir'] != None:
    filename_list = params['input_dir']

if params['filename_list'] != None:
    filename_list = params['filename_list']

if params['filename_list'] != None or params['input_dir'] != None:
    functions.extract_images_from_multiple_pdfs(filename_list,os.path.join(output_path,dir_name),params['pagenumber'],params['pagerange'],'png')
    
else:
    output_path = os.path.join(output_path,dir_name)
    input_file_name = os.path.basename(params['input_file'])
    output_path = os.path.join(output_path,input_file_name)
    functions.extract_images(os.path.abspath(params['input_file']),output_path,params['pagenumber'],params['pagerange'],'png')
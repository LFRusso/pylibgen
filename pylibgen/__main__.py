from pylibgen import search_book
import os
import sys
import traceback
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cli_run(args=None):
    if args == None:
        args = sys.argv[1:]
    if (len(args)==1):
        results = search_book(args[0])
    elif (len(args)==2):
        results = search_book(args[0], args[1])
    else:
        sys.exit(1)
    pretty_print(results)

    selected_doc=input()
    try:
        selected_doc = int(selected_doc)-1
    except:
       return

    download_url = get_download_url(results[selected_doc])
    filename = results[selected_doc]["Title"].replace(' ', '') + '.' + results[selected_doc]["Extension"] 
    download_file(download_url, filename)

def download_file(url, filename):
    with open(filename, "wb") as f:
        print("Downloading %s"%filename)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
            print()

def get_download_url(doc_data):
    url = "http://111.90.145.72/get"+doc_data["Mirror_2"][20:]+"&mirr=1"
    return url

def pretty_print(results, jp2a=True):
    for i,result in enumerate(results):
        out_str = f"""
      {"[{:02d}]".format(i+1)}. {bcolors.HEADER}Tite:{bcolors.ENDC} {result['Title']}
            {bcolors.HEADER}Author:{bcolors.ENDC} {result['Author']}
            {bcolors.HEADER}Publisher:{bcolors.ENDC} {result['Publisher']}
            {bcolors.HEADER}Year:{bcolors.ENDC} {result['Year']}
            {bcolors.HEADER}Extension:{bcolors.ENDC} {result['Extension']}
            {bcolors.HEADER}Size:{bcolors.ENDC} {result['Size']}
            {bcolors.HEADER}Language:{bcolors.ENDC} {result['Language']}
        --
        """
        print(out_str)
    num_str = ' '.join([f"[{i+1}]" for i in range(len(results))])
    print(f"{bcolors.HEADER}SELECT A SOURCE: {num_str} default: quit{bcolors.ENDC}\n")

def run_with_catch(args=None):
    try:
        cli_run(args)
    except:
        print("An exception occurred:", traceback.format_exc())

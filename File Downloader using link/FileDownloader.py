## File Downloader ##
## Automation script which download all file. Link are mention in input text file and keep downloaded file in particular folder


import os
import requests
import  urllib.request
import sys
from urllib.parse import urlparse 

def IsDownloadable(url):
    # Checking if url link is downloadable or not
    h = requests.head(url, allow_redirects = True)
    header = h.headers
    content_type = header.get("content-type")
    print(content_type)
    if 'text' in content_type.lower():
        return False
    
    if 'html' in content_type.lower():
        return False
    return True

def isConnection():
    try:
        # hitting google site 
        urllib.request.urlopen(url = 'http://216.58.192.142',timeout = 4)
        
        # If it successfully open without any exception
        return True
    except urllib.error.URLError:
        return False


def GetFilenameFromCD(url):
    a = urlparse(url)
    return os.path.basename(a.path)

def Download(url, directive):

    allowed  = IsDownloadable(url)
    #allowed = True
    if allowed:
        # Downloading file
        try:
            print(url)
            filename = GetFilenameFromCD(url)
            destPath = os.path.join(directive,filename)

            res = requests.get(url, stream = True)
            with open(destPath , "wb") as fd:
                # Write in chunk
                for chunk in res.iter_content(chunk_size=1024): 
                    if chunk:
                        fd.write(chunk)


        except Exception:
            print("Exception")
            return False
    else:
        print("File is not downloadable")
        return False

def DownloadFiles(linkFile , directive):

    connection = isConnection()

    if connection:
        if not os.path.isabs(directive):
            directive = os.path.abspath(directive)

        if not os.path.exists(directive):
            os.mkdir(directive)

        if(os.path.exists(linkFile)):
            with open(linkFile , "r") as fp:
                for url in fp:
                    # download each file
                    Download(url,directive)
        else:
            print("File which content link is not found")
    else:
        print("No internet connection")

def main():
    # Filter of help and usage
    if len(sys.argv) < 2:
        print("FileDownloader_Error: Incorrect Argument")
        exit()

    #Help
    if sys.argv[1] == '-h' or sys.argv[1] == '-H':
        print("FileDownloader_Help: Download all the contents whose link is mention in one file and save in specfic directive.")
        exit()

    # Usage
    if sys.argv[1] == '-u' or sys.argv[1] == '-U':
        print(f"FileDownloader_Usage: {sys.argv[0]}  FileName  DirectiveName")
        print("FileName: File which content the link of file which must be download")
        print("DirectiveName: Directive name where all the downloaded file must be same")
        exit()
    
    #Filter for our own program
    if len(sys.argv) != 3:
        print("FileDownloader_Error: Incorrect Argument")
        exit()

    DownloadFiles(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
## File Downloader ##
## Automation script which download all file. Link is mention in input text file  and keep downloaded file in particular folder


import os
import requests

def downloadFile(linkFile , directive):

    if not os.path.isabs(directive):
        directive = os.path.abspath(directive)

    if not os.path.exists(directive):
        os.mkdir(directive)
    
    if(os.path.exists(linkFile)):
        
        icnt = 1
        # open the linkfile
        with open(linkFile , "r") as fp:
            for link in fp:
                # download each file
                try:
                    res = requests.get(link,stream = True)

                    destPath = os.path.join(directive,f"File{icnt}")
                    icnt += 1
                    
                    with open(destPath , "wb") as data:
                        for chunk in res.iter_content(chunk_size=1024): 
  
                        # writing one chunk at a time to pdf file 
                            if chunk: 
                                data.write(chunk) 
                except Exception:
                    pass


    else:
        print("File which content link is not found")

def main():
    downloadFile("links.txt","Download")

if __name__ == "__main__":
    main()
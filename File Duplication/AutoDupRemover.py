## imports
import sys
import os
import hashlib
import time
import urllib.request
import smtplib
import schedule # external
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


## return Checksum of file
def getFileCheckSum(filePath, blocksize = 1024):
    log_fp = open(filePath, "rb")
    hasher = hashlib.md5()
    buf = log_fp.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = log_fp.read(blocksize)
    log_fp.close()
    return hasher.hexdigest()


## Return Duplicate file list and number file scan
def findDuplicateFileList(dirName):

    listDup = dict() # hashtable <key><value> where key is checksum and value is list of path having that checksum
    fileScan = 0

    exist = os.path.isdir(dirName)

    if exist:

        # traversing the folder
        for folderName,subFolders,fileNames in os.walk(dirName):

            fileScan += len(fileNames)
            for fname in fileNames:
                # get checkSum
                fullpath = os.path.join(folderName,fname)
                chksm = getFileCheckSum(fullpath)
                
                #check if key exist or not
                if chksm in listDup:
                    listDup[chksm].append(fullpath)
                else:
                    listDup[chksm] = [fullpath]


        # filter the duplicate
        listDup = list(filter(lambda lst: len(lst) > 1,listDup.values()))

        # return duplicate list and no. file scan
        return listDup,fileScan

    else:
        print(f"Marvellous_Error: {dirName} is not directive or not found\n")


## Delete all duplicate file keep one file of each duplicate file and write on log
def DeleteDuplicate(dupList,outputFd):

    # Remove All duplicate but leaving One copy of each
    outputFd.write("Duplicate files: \n")
    i = 0
    no_of_duplicate = 0
    for sameFileList in dupList: 
        no_of_duplicate += len(sameFileList)
        i += 1
        outputFd.write(f"{i}. Deleting Below File as it's copy is present at : {sameFileList[0]}\n")
        for file in sameFileList[1:]:
            #os.unlink(file)
            outputFd.write(f"\t[deleted] {file}\n")
    return no_of_duplicate

def isConnection():
    try:
        # hitting google site 
        urllib.request.urlopen(url = 'http://216.58.192.142',timeout = 4)
        
        # If it successfully open without any exception
        return True
    except urllib.error.URLError:
        return False


## Send mail
def SendMail(SEND_TO, subject, body, LOG_PATH):
    
    # checking connection
    connection = isConnection()
    if not connection:
        print("There is no internet connection")
        return
    
    GMAIL_USER = "rohitkadam1407@gmail.com"
    GMAIL_PASSWORD = "---------" #input(f"Enter password of {GMAIL_USER}: ") ## put here password

    #  Forming MIME mail
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = SEND_TO
    msg['Subject'] = subject
    
    # Body
    # 1. attach text
    msg.attach( MIMEText(body,'plain'))
    # 2 attach document
    with open(LOG_PATH, 'rb') as fp:#file
        attachment = MIMEBase('application','octet-stream')
        attachment.set_payload(fp.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=LOG_PATH)
    msg.attach(attachment)

    ## SENDING MAIL via SMPT server
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login( GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER,SEND_TO, msg.as_string())
        server.close()
        print("Mail send successfully")
    except Exception:
        print(f"Error: Mail is not send.")
    
def startProcess():
    try:

        dupList = [] 
        startTime = time.ctime()
        # Duplicate list
        dupList, fileScan = findDuplicateFileList(sys.argv[1])
        
        # create log file
        separator = "-" * 80
        if not os.path.exists("log"):
            os.mkdir("log")

        log_path = os.path.join("log",f"MarvellousLog {startTime}.log")
        log_fp = open(log_path, "w")
        log_fp.write(separator+"\n")
        log_fp.write(f"Marvellous Infosystem Duplicate File Remover: {startTime} \n")
        log_fp.write(separator+"\n")
        log_fp.write("\n")

        # delete duplicate files
        no_of_duplicate = DeleteDuplicate(dupList,log_fp)
        log_fp.close()

        # Form mail content
        send_to = sys.argv[3]
        subject = "Duplicate File Remover Log Report"
        body = f'''
        Hello, {send_to}
            Welcome to my python automation script for removing duplicate file
            Attachment document which contains Log of delete file

            Statistic:--
                1. Scan started at: {startTime}
                2. Total Number of files scanned: {fileScan}
                3. Total number of duplicate files found: {no_of_duplicate}

            This is auto generated mail
            From,
            Rohit Kadam
        '''
        # send the mail
        SendMail(send_to,subject,body,log_path)

    except Exception as err:
        print(f"err{err}")
        pass


def Main():
    # Filter of help and usage
    if len(sys.argv) < 2:
        print("AutoDupRemover_Error: Incorrect Argument")
        exit()

    #Help
    if sys.argv[1] == '-h' or sys.argv[1] == '-H':
        print("AutoDupRemover_Help: Interval remove all duplicate file and maintain deleted file record and send record via mail ")
        exit()

    # Usage
    if sys.argv[1] == '-u' or sys.argv[1] == '-U':
        print(f"AutoDupRemover_Usage: {sys.argv[0]}  Directory_Name  Time_Interval(min)  Sender_Mail_ID")
        exit()
    
    #Filter for our own program
    if len(sys.argv) != 4:
        print("AutoDupRemover_Error: Incorrect Argument")
        exit()

    # Input data validation

    # schedule at every argv[2] min
    try:
        min = int(sys.argv[2])
        schedule.every(min).minutes.do(startProcess)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception:
        print("Invalid Argument")

if __name__ == "__main__":
    Main()
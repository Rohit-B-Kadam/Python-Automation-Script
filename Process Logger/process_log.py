# Design automation script which accept directory name from user and create log file in that directory which contains information of running processes as its name, PID, Username.

import psutil
import sys
import os
import time
import smtplib
import urllib.request
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


## Create Log file have running process info
def ProcessLogger(log_dir):
    
    # create folder is present or not 
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    if not os.path.isdir(log_dir):
        print("Given directive name is not directive")

    listProcess = []

    #Time
    checkTime = time.ctime()
    for proc in psutil.process_iter():
        try:
            #pinfo = proc.as_dict()  # for full info
            pinfo = proc.as_dict(attrs= ['pid','name','username'])
            
            vms = round(proc.memory_info().vms / (1014 * 1024),2)  # convert to mb
            pinfo["vms"] = vms
            listProcess.append(pinfo)
        except:
            pass

    
    # create log file
    separator = "-" * 80
    log_path = os.path.join(log_dir,f"MarvellousLog {checkTime}.log")
    fp = open(log_path, "w")
    fp.write(separator+"\n")
    fp.write(f"Marvellous Infosystem Process Logger: {checkTime} \n")
    fp.write(separator+"\n")
    fp.write("\n")

    # print all process info
    for element in listProcess:
        fp.write(f"{element}\n")
    
    fp.close()
    return log_path

## To check internet connection is there or not
def isConnection():
    try:
        # hitting google site 
        urllib.request.urlopen(url = 'http://216.58.192.142',timeout = 4)
        
        # If it successfully open without any exception
        return True
    except urllib.error.URLError:
        return False

## Send mail to param1 with file attachment param2
def SendMail(SEND_TO , LOG_PATH):
    
    connection = isConnection()
    if not connection:
        print("There is no internet connection")
        return
    
    # Mail send data
    GMAIL_USER = "rohitkadam1407@gmail.com"
    GMAIL_PASSWORD = input(f"Enter password of {GMAIL_USER}: ")
    print(LOG_PATH)
    subject = "Automation Process log Generated "
    body = f'''
    Hello, {SEND_TO}
        Welcome to my python automation script
        Attachment document which contains Log of running process
        This is auto generated mail
        From,
        Rohit Kadam
    '''

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
    except Exception as e:
        print(f"Error: Mail is not send.")
        print(e)


def main():
    # Filter of help and usage
    if len(sys.argv) < 2:
        print("Marvellous_Error: Incorrent Argument")
        exit()

    #Help
    if sys.argv[1] == '-h' or sys.argv[1] == '-H':
        print("Marvellous_Help: Design automation script which accept directory name from user and create log file in that directory which contains information of running processes as its name, PID, Username.")
        exit()

    # Usage
    if sys.argv[1] == '-u' or sys.argv[1] == '-U':
        print(f"Marvellous_Usage: {sys.argv[0]} ProcessName")
        exit()
    
    #Filter for our own program
    if len(sys.argv) != 3:
        print("Marvellous_Error: Incorrent Argument")
        exit()

    try:

        log_path = ProcessLogger(sys.argv[1])
        print("Log file is created")
        SendMail(sys.argv[2], log_path)

    except Exception as err:
        print(f"err{err}")
        pass


if __name__ == "__main__":
    main()
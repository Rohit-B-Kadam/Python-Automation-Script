# Periodic Process Logger

- In this project we create log file with the current time and store information about all running processes as its name, PID, memory usage, thread count number of child process.
- Our automation script executes periodically depends on the time specified by the user using scheduler of python.
- After periodic execution it sends the log file to the specified email address.

## How I Have Done

1. I have use iter_process() function from psutil module to get all the running process information.
1. Then I have create new log file with current time name (time.ctime) and record all the process infomation in it.
1. Using email and smtplib module I have send email to the user with attached log file.
1. All the above process is execute periodically depends on the time. This is done by using schedulepip module.

## Usage

        $process_log Directory_Name  Time_Interval(min)  Sender_Mail_ID

- AutoDupRemover : Name of python automation script.
- Directory_Name : Directory which may contains duplicate files.
- Time_Interval  : Time interval of script in minutes.
- Sender_Mail_ID : Mail ID of the receiver.

Before Running this project you have to change your gmail security.

___

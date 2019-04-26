# Duplicate File Remover

It is python script which continous scan and detect the duplicate file by considering the checksum of file. Delete all the duplicate file keep exist one copy of each file which can use to free space. It also keep log of delete file which is send to the user through mail.

## Feature

1. md5 algorithm is use to calculate checksum which can also handle big file.
1. Create log file which keep track of all the activate done by program ( list delete file)
1. Send mail with log file attachment to a mail.
1. Automatically scan after specified time interval

## Usage

        $AutoDupRemover Directory_Name  Time_Interval(min)  Sender_Mail_ID

- AutoDupRemover : Name of python automation script.
- Directory_Name : Directory which may contains duplicate files.
- Time_Interval  : Time interval of script in minutes.
- Sender_Mail_ID : Mail ID of the receiver.
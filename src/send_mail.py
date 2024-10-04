from pathlib import Path
ROOT=Path(__file__).parent.parent
import sys
sys.path.append(str(ROOT))

import pandas as pd
from datetime import datetime

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ENV={}

def load_env_values(envpath:Path):
    with open(envpath,"r",encoding="utf-8") as f:
        lines=[line.split("=") for line in f.readlines()]
    
    for key,val in lines:
        ENV[key]=val.replace("\n","")

    
def load_mail(mailpath:Path):
    with open(mailpath, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    message = MIMEText(html_content, "html")
    return message


def make_gmail(message:MIMEText,subject,from_mail,to_mail):
    # Create a MIMEMultipart object to combine headers and the MIMEText message
    gmail_message = MIMEMultipart()
    gmail_message['Subject'] = subject
    gmail_message['From'] = from_mail
    gmail_message['To'] = to_mail
    
    # Attach the MIMEText message to the MIMEMultipart object
    gmail_message.attach(message)
    
    return gmail_message


def send_gmail(gmail,my_gmail_address,ap_password):
    server = smtplib.SMTP_SSL(
        "smtp.gmail.com", 465,
        context = ssl.create_default_context())
    server.set_debuglevel(0)
    server.login(my_gmail_address, ap_password)
    server.send_message(gmail)


def load_shift(shiftpath:Path):
    shift=pd.read_csv(shiftpath)
    return shift

def load_gmail_subject(subjectpath:Path):
    with open(subjectpath,"r",encoding="utf-8") as f:
        lines=[line.split("=") for line in f.readlines()]
    
    subject_dct={}
    for key,val in lines:
        subject_dct[key]=val.replace("\n","")

    return subject_dct

def get_subject(subjectpath,today, shift_date):
    subjects=load_gmail_subject(subjectpath)
    first_week_subject=subjects["FIRST_WEEK_SUBJECT"]
    remind_week_subject=subjects["REMIND_WEEK_SUBJECT"]

    first_date=shift_date[0]
    if first_date==today: return first_week_subject
    elif today in shift_date[1:]: return remind_week_subject

def main():

    today=datetime.strftime(datetime.today().date(),"%Y-%m-%d")
    today="2024-10-07"

    shiftpath=ROOT/"output/shift.csv"
    shift=load_shift(shiftpath)
    
    if not today in shift["date"].values:
        print(f"今日({today})は送信日じゃありません")
        print(f"メール送信日：\n{shift['date'].values}")
    else:
        subjectpath=ROOT/"resource/gmail_subject.txt"
        subject=get_subject(
            subjectpath,
            today,shift_date=shift["date"].values
            )

        envpath=ROOT/"envs.txt"
        load_env_values(envpath)

        mailpath=ROOT/"output/mail.html"
        message=load_mail(mailpath)

        gmail=make_gmail(
            message,subject=subject,
            from_mail=ENV["MY_GMAIL_ADDRESS"],
            to_mail=ENV["TO_GMAIL_ADDRESS"]
            )
        send_gmail(
            gmail=gmail,
            my_gmail_address=ENV["MY_GMAIL_ADDRESS"],
            ap_password=ENV["AP_PASSWORD"]
        )


if __name__=="__main__":
    main()
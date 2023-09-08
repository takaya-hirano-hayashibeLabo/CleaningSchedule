import sys  
from pathlib import Path
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import pandas as pd
import argparse
import datetime
from math import floor
import random
import re


def main():

    #===シフトの生成
    parser=argparse.ArgumentParser()
    parser.add_argument("--start_date",default="2023/1/1") #掃除を開始する日付
    args=parser.parse_args()
    shift_date=datetime.datetime.strptime(args.start_date,"%Y/%m/%d")

    with open(f"{ROOT}/resource/labo_member.txt","r", encoding="utf-8") as f:
        labo_members:list="".join(f.readlines()).split("\n")
    random.shuffle(labo_members) #メンバーリストをシャッフル

    total_weaks=floor(len(labo_members)/2)
    shift=[[
        shift_date+datetime.timedelta(7*weak_i),
        labo_members.pop(),
        labo_members.pop()
    ] for weak_i in range(total_weaks)]
    shift=pd.DataFrame(shift,columns=["","member1","member2"])

    msg="===New Shift======================================"
    print(msg)
    print(shift)
    print("="*len(msg))

    # shift.to_csv(f"{ROOT}/output/shift.csv",index=False)
    #===


    #===送信用メールの生成
    with open(f"{ROOT}/resource/mail_template.html","r",encoding="utf-8") as f:
        template="".join(f.readlines())

    content=re.sub("%START_DATE",args.start_date,template)
    content=re.sub("%SHIFT",shift.to_html(index=False),content)
    # print(content)

    with open(f"{ROOT}/output/mail.html","w",encoding="utf-8") as f:
        f.writelines(content)
    msg="\n=== Check below link!! ==========================="
    print(msg)
    print("http://127.0.0.1:5500/output/mail.html")
    print("="*(len(msg)-1))
    #===



if __name__=="__main__":
    main()


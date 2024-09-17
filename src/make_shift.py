import sys  
from pathlib import Path
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import os
import pandas as pd
import argparse
import datetime
from math import floor
import random


def main():

    #===シフトの生成
    parser=argparse.ArgumentParser()
    parser.add_argument("--start_date",default="2023/1/1") #掃除を開始する日付
    args=parser.parse_args()
    shift_date=datetime.datetime.strptime(args.start_date,"%Y/%m/%d")

    with open(f"{ROOT}/resource/labo_member.txt","r", encoding="utf-8") as f:
        labo_members=[]
        for line in f.readlines():
            if not "#"==line[0] and not "\n"==line:
                labo_members.append(line)
        labo_members:list="".join(labo_members).split("\n")
    random.shuffle(labo_members) #メンバーリストをシャッフル

    total_weaks=floor(len(labo_members)/2)
    shift=[[
        shift_date+datetime.timedelta(7*weak_i),
        labo_members.pop(),
        labo_members.pop()
    ] for weak_i in range(total_weaks)]
    shift=pd.DataFrame(shift,columns=["date","member1","member2"])

    msg="===New Shift======================================"
    print(msg)
    print(shift)
    print("="*len(msg))

    output_file_path=f"{ROOT}/output/shift.csv"

    #-- いちおうバックアップは取っておく
    if os.path.isfile(output_file_path):
        shift_prev=pd.read_csv(output_file_path)
        shift_prev.to_csv(f"{ROOT}/output/shift_backup.csv",index=False,encoding="utf-8")
    #--

    shift.to_csv(output_file_path,index=False,encoding="utf-8")
    #===


if __name__=="__main__":
    main()


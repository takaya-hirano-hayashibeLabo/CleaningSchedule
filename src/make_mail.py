import sys  
from pathlib import Path
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)
import os 
import webbrowser

import pandas as pd
import re
    

def main():
    
    shift=pd.read_csv(f"{ROOT}/output/shift.csv")

    #===送信用メールの生成
    with open(f"{ROOT}/resource/mail_template.html","r",encoding="utf-8") as f:
        template="".join(f.readlines())

    content=re.sub("%START_DATE",shift["date"].values[0],template)
    content=re.sub("%SHIFT",shift.to_html(index=False,header=False),content)
    # print(content)

    with open(f"{ROOT}/output/mail.html","w",encoding="utf-8") as f:
        f.writelines(content)
    msg="\n=== Open below link!! ==========================="
    print(msg)
    print(f"{ROOT}/output/mail.html")
    webbrowser.open_new_tab(f"file:///{ROOT}/output/mail.html")
    print("="*(len(msg)-1))
    #===

if __name__=="__main__":
    main()
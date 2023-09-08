# 掃除当番のシフト&送信用メールを作るプログラム

## 使い方
### 1. 研究室のメンバーリストを用意
`resource/labo_member.txt`に1行づつメンバーの名前を入れておく.
~~~
Takashi
Hanako
etc...
~~~

### 2. pandas入れる
`pandas`が入ってなかったら入れる.  
いい感じに表示&csv出力用.
~~~bash
pip install pandas
~~~

### 3. 実行
`src/make_mail.py`を実行.  
`--start_date`はシフトテーブルの1周目の月曜日にしておく.  
~~~bash
python src/make_mail.py --start_date 2023/10/2
~~~

### 4. メールのテンプレをコピー
`http://127.0.0.1:5500/output/mail.html`にアクセス.  
表示された内容を全選択してgmailにコピペ.  
(表示できないときは`output/mail.html`をchromeかなんかで表示する.)  
表示される内容は, `resource/mail_template.html`に1周目の日付とシフトテーブルを追加したもの.
"""
ニュースが公開日になると自動的に公開になる
"""

import os
from datetime import datetime

import mysql.connector

# コネクションの作成
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='db-user',
    password='db-pass',
    database='database'
)

# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)

cursor = conn.cursor()

# データ更新
today = datetime.today()
today = str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2)
today_from = today + " 00:00:00"
today_to = today + " 23:59:59"
update_news_query = "UPDATE news SET is_published = True WHERE published_at >= %s AND published_at <= %s"
cursor.execute(update_news_query, (today_from, today_to))

# 変更を確定
conn.commit()

# 接続を閉じる
cursor.close()
conn.close()
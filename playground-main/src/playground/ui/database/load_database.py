import logging
from pathlib import Path

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import pandas as pd

# from modlunky2.constants import BASE_DIR

BASE_DIR = BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "static" / "data"
DB_CONFIG = {
    "user": 'root',
    "password": "0000",
    "host": 'localhost',
    "database": 'rtc_mario_kart_8_deluxe_betting_database',
}


def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    return


# Excel 파일 읽기
print(DATA_PATH / 'course.csv')
df = pd.read_csv(DATA_PATH / 'course.csv')


# MySQL 데이터베이스 연결
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# 테이블 생성
columns = df.columns
table_creation_query = f'''
CREATE TABLE IF NOT EXISTS train_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {', '.join([f'{col} VARCHAR(255)' for col in columns])}
)
'''

cursor.execute(table_creation_query)

# 데이터베이스에 데이터 추가
for index, row in df.iterrows():
    placeholders = ', '.join(['%s'] * len(row))
    columns = ', '.join(row.index)
    sql = f"INSERT INTO train_data ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(row))

# 변경사항 저장
conn.commit()

# 데이터베이스 연결 종료
conn.close()

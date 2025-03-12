# undetected seleniumのインストール　不可なのでseleniumでやるか　
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException,ElementClickInterceptedException,StaleElementReferenceException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.support.select import Select
import math
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from subprocess import CREATE_NO_WINDOW
import pandas as pd
import sys
import json
import re
import os
from collections import Counter
from csv import writer
import csv
import random
import threading
import gspread
import logging
import google.generativeai as genai






# それぞれのuRlにアクセスして、それぞれのスプレッドシートに収める
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
#ランダム数の作成
"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""
import time
import os
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
import string
randomC = random.uniform(1,7)

def google_sheet():
    # JSONキーファイルのパスを指定
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('gemini-api-438211-32992babf21f.json', scopes=scope)

    # クライアントを作成
    gc = gspread.authorize(creds)
    return gc

def write_to_sheet(sheet, row, col, text):
    sheet.update_cell(int(row), col, text)


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

#mamhdiet.gcp
# genai.configure(api_key='AIzaSyBOsGNpFm3qS5OqkR0sE4vvEefQBgAlp9c')
# mememori8888
# genai.configure(api_key='AIzaSyCjEX3uUzEjafFIY91130KXn6vj-C1mm4I')
# mamhidet.map
# genai.configure(api_key='AIzaSyCJb0vmJwoGHNFKX1Nr-61EliLjbg_MqTs')
# mamhidet.gemini
genai.configure(api_key='AIzaSyALDC8dXBD6Dk8cCuvsjHf1zN3woCAzYfQ')

# Create the model


# GoogleSheetからURLを取得して、URLを回す


def get_html_urllib(url):
    """
    urllibを用いてHTMLを取得する関数
    """
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')  # UTF-8でデコード

    return html


def extract_text(html):

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text


# sheet_name = 'シート2'
# gc = google_sheet()
# # スプレッドシートのIDを指定して開く
# spreadsheet_id = '1kfrAZHK6R4u3rGchXSkNYjkp5uvTLVdo6rsk390YoKA'
# sheet = gc.open_by_key(spreadsheet_id).worksheet(sheet_name)
# #A行の値を取得
# a_row_values = sheet.col_values(1)
# company_names = sheet.col_values(2)
# count = len(a_row_values)
# URLにアクセスして、HTMLを取得する。

#fletでテキスト入力と、結果出力を作る
#入力したテキストとAI出力結果をmysqlにためていく。
# result_textにテキストを入れる






import flet as ft
import mysql.connector
import datetime

# MySQLデータベースの設定
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mamhidet_mysql',
    'database': 'gemini_programming',
}

def main(page: ft.Page):
    page.title = "AI応答アプリ"

    input_text = ft.TextField(label="質問を入力してください")
    output_text = ft.Text()
    ai_response = ft.TextField(label="AI応答", read_only=False, multiline=True, expand=True)  # TextFieldに変更

    def send_request(e):
        question = input_text.value
        response = get_ai_response(question)  # AI応答を取得する関数を呼び出す
        output_text.value = f"質問: {question}"
        ai_response.value = f"AI応答: {response}"  # AI応答をテキストコントロールに設定
        page.update()

        # MySQLにデータを保存
        save_to_mysql(question, response)

    send_button = ft.ElevatedButton("送信", on_click=send_request)

    page.add(
        input_text,
        send_button,
        output_text,
        ai_response,  # AI応答を表示するテキストコントロールを追加
    )

def get_ai_response(question):
    try:
        response = model.generate_content( 
        f'''対象のテキストを熟練のプログラマとして答えてください。日本語と英語両方用意してください。
        [{question}] |
        ''',
        generation_config = genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.1,
            )
        )
        time.sleep(3)
        result_text= response.text
        # write_to_sheet(sheet, row, 5, text)
        # write_to_sheet(sheet, row, 6, title)
        # print(f'{text}/n{row}を更新しました。')
    except Exception as e:
          # write_to_sheet(sheet, row, 5, f'{str(e)}')
          # write_to_sheet(sheet, row, 6, title)
          print('GeminiAPIエラー')
          result_text = "GeminiAPIエラー"
          time.sleep(10)

    return result_text

def save_to_mysql(question, response):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        query = "INSERT INTO responses (question, response, timestamp) VALUES (%s, %s, %s)"
        values = (question, response, datetime.datetime.now())
        cursor.execute(query, values)

        conn.commit()
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
    finally:

        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    ft.app(target=main)

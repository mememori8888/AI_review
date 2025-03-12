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

#ランダム数の作成
randomC = random.uniform(1,7)


##chormeのオプションを指定
options = webdriver.ChromeOptions()
# options.add_argument("--headless")# ヘッドレスで起動するオプションを指定
options.page_load_strategy = 'eager'

# options.add_argument("--incognito")
# options.add_argument("--no-startup-window")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200,1200")
options.add_argument("--no-sandbox")
options.add_argument("--enable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--enable-webgl")
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--ignore-certificate-errors")
options.add_argument('--enable-unsafe-swiftshader')
options.add_argument('blink-settings=imagesEnabled=false')  # 画像の読み込みを無効化
options.add_argument('--disable-cache')


path = os.getcwd()
CHROMEDRIVER = path + r'\chromedriver.exe'


driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)



# それぞれのuRlにアクセスして、それぞれのスプレッドシートに収める
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
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


sheet_name = 'シート2'
gc = google_sheet()
# スプレッドシートのIDを指定して開く
spreadsheet_id = '1kfrAZHK6R4u3rGchXSkNYjkp5uvTLVdo6rsk390YoKA'
sheet = gc.open_by_key(spreadsheet_id).worksheet(sheet_name)
#A行の値を取得
a_row_values = sheet.col_values(1)
company_names = sheet.col_values(2)
count = len(a_row_values)
# URLにアクセスして、HTMLを取得する。
for i in range(27,count,1):
    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    url = a_row_values[i]
    company_name = company_names[i]
    row = i + 1
    print(f'{i}番目/{url}')
    if 'itp' in url or '該当なし' in url or 'ビジネスプロフィール' in url or 'navitime' in url or 'pdf' in url:
        continue
    else:
        try:
            driver.get(url)
            # driver.delete_all_cookies()
            # # 全ての要素を取得
            # elements = driver.find_elements(By.XPATH, "//*")
            # elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*")))
            page_source = driver.page_source
            # BeautifulSoupオブジェクトを作成
            soup = BeautifulSoup(page_source, 'html.parser')

            # 全てのテキストを取得
            result_text = soup.get_text()
            
            title = driver.title
            html_text = ""
            # for element in elements:
            #     text = element.text
            #     html_text += text + "\n"

            # print(f'html_textは{html_text}')
            # result_text = extract_text(html_text)
            # print(result_text)
            reuslt_text = result_text.replace(' ','').replace('\n', '').replace('/n','')
            # write_to_sheet(sheet,row,result_text)
            
            try:
                response = model.generate_content( 
                f'''対象のテキストから|電話番号を取得してください。目的は|ホテル|飲食店|の営業リスト作成です。|電話番号はできるだけ一つで出力してください。
                対象のテキストから|事業カテゴリ|を推測し、電話番号を抽出してください。|
                
                [{result_text}] |
                
                書き方は、
                本社の場合は、【本社】○○|
                ホテルの場合は、【ホテル】○○|
                対象のテキストが地図サイトやデータベースサイトの場合は、【データベースサイト】○○|
                介護事業の場合は【介護】という形にしてください。|
                つまり、【事業カテゴリ】○○|という書き方にしてください。
                電話番号がない場合、または|対象のテキストがない場合|は、電話番号の掲載がありません。|
                と指定してください。それ以外の書き方は拒否してください。余計なスペース入れないでください。|
                複数ある場合は、本社のみ抽出してください。
                
                ''',
                generation_config = genai.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.1,
                    )
                )
                time.sleep(3)
                text= response.text
                write_to_sheet(sheet, row, 5, text)
                write_to_sheet(sheet, row, 6, title)
                print(f'{text}/n{row}を更新しました。')
            except Exception as e:
                write_to_sheet(sheet, row, 5, f'{str(e)}')
                write_to_sheet(sheet, row, 6, title)
                print('GeminiAPIエラー')
                time.sleep(10)
                continue

            print('書き込み完了')
            # time.sleep(5)
            
        except WebDriverException as e:
            print(f"URL Error: {e}")
            write_to_sheet(sheet, row, 5, 'アクセスエラー')
            # write_to_sheet(sheet, row, 6, title)
        # except:
        #     write_to_sheet(sheet, row, 5, 'エラー')
        #     continue




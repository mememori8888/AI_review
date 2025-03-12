import flet as ft
import mysql.connector
import datetime
import google.generativeai as genai
import time

# MySQLデータベースの設定 (デフォルト)
MYSQL_CONFIG_DEFAULT = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mamhidet_mysql',
}

genai.configure(api_key='AIzaSyCkm2LyaYtP934_WEcije6MjbLMg_tCmrw')

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

seven_text = """

あなたは、相手の立場や感情を深く理解し、共感的なコミュニケーションを促進するプロフェッショナルなライターです。以下の状況において、相手の視点を最大限に尊重し、理解に徹した上で、あなたの考えを伝える文章を作成してください。

状況: [状況を具体的に記述]

指示:

1.  まず、相手の立場、感情、意図を深く理解するために、どのような質問をすべきかをリストアップしてください。
2.  リストアップした質問に対する回答を、相手の立場に立って想像し、記述してください。
3.  上記で得られた理解に基づき、相手の感情に共感し、理解を示す文章を作成してください。
4.  相手の理解を得られたと感じた上で、あなたの考えや提案を、相手が理解しやすいように論理的かつ共感的に伝えてください。
5.  最後に、相手との建設的な対話を促すための質問を提示してください。

制約条件:

* 文章は、相手への敬意と共感に満ちたものであること。
* あなたの意見は、相手の理解を深めた上で、丁寧に提示すること。
* 常に相手の視点を考慮し、対話を通じて相互理解を深めることを目指すこと。

"""

# ボタンのラベルとプロンプト
button_data = [
    {"label": "ビジネスコンサル", "prompt": "対象のテキストをビジネスコンサルタントとして答えてください。日本語と英語両方用意してください。"},
    {"label": "七つの習慣フリーランス", "prompt": f"対象のテキストを{seven_text}を参考にフリーランスとして答えてください。日本語と英語両方用意してください。"},
    {"label": "HTML解析", "prompt": "対象のHTMLを解析して、seleniumでのデータ抽出に必要な要素を教えてください。"},
    {"label": "ビジネスメール", "prompt": "対象のテキストをビジネスメール形式にしてください。日本語と英語両方用意してください。"},
    {"label": "program", "prompt": "対象のテキストを熟練のプログラマとして答えてください。日本語と英語両方用意してください。"},
    {"label": "レシピ", "prompt": "対象のテキストを栄養の効率のいい組み合わせを取り入れて料理研究家として答えてください。日本語と英語両方用意してください。"},
    {"label": "翻訳", "prompt": "対象のテキストを日本語に翻訳してください。日本語と英語両方用意してください。"},
    {"label": "YouTube", "prompt": "対象のyoutube動画を要約してください。日本語と英語両方用意してください。"},

]

# 各ボタンに対応するデータベース名
database_names = [
    "gemini_brain_knock",
    "gemini_business_sujest",
    "gemini_parse",
    "gemini_mail",
    "gemini_programming",
    'gemini_recipe',
    'gemini_translation',
    'gemini_youtube',
]

# 各ボタンに対応するテーブル名
table_names = [
    "responses",
    "responses",
    "responses",
    "responses",
    "responses",
    "responses",
    "responses",
    "responses",
]

def main(page: ft.Page):
    page.title = "AI応答アプリ"

    input_text = ft.TextField(label="質問を入力してください")
    # output_text = ft.Text()
    output_text = ft.TextField(label="質問", read_only=False, multiline=True, expand=True)
    ai_response = ft.TextField(label="AI応答", read_only=False, multiline=True, expand=True)

    def send_request(e):
        button_index = int(e.control.data)
        question = input_text.value
        prompt = button_data[button_index]["prompt"]
        database_name = database_names[button_index]
        table_name = table_names[button_index]

        response = get_ai_response(question, prompt)
        output_text.value = f"質問: {question}"
        ai_response.value = response
        page.update()
        save_to_mysql(question, response, database_name, table_name)

    buttons = []
    for i, data in enumerate(button_data):
        button = ft.ElevatedButton(text=data["label"], on_click=send_request, data=i)
        buttons.append(button)

    page.add(
        input_text,
        ft.Row(controls=buttons),
        output_text,
        ft.Column([ai_response], expand=True),
    )

def get_ai_response(question, prompt):
    try:
        response = model.generate_content(
            f'''{prompt}
            [{question}] |
            ''',
            generation_config=genai.GenerationConfig(
                max_output_tokens=50000,
                temperature=0.1,
            )
        )
        time.sleep(3)
        result_text = response.text
    except Exception as e:
        print('GeminiAPIエラー')
        result_text = "GeminiAPIエラー"
        time.sleep(10)

    return result_text

def save_to_mysql(question, response, database_name, table_name):
    try:
        # デフォルト設定で接続 (データベース作成用)
        conn_default = mysql.connector.connect(**MYSQL_CONFIG_DEFAULT)
        cursor_default = conn_default.cursor()

        # データベースが存在しない場合は作成
        cursor_default.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        conn_default.commit()
        cursor_default.close()
        conn_default.close()

        # データベースに接続
        MYSQL_CONFIG = {**MYSQL_CONFIG_DEFAULT, 'database': database_name}
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # テーブルが存在しない場合は作成
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT,
                response TEXT,
                timestamp DATETIME
            )
        """)
        conn.commit()

        # データを挿入
        query = f"INSERT INTO {table_name} (question, response, timestamp) VALUES (%s, %s, %s)"
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
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
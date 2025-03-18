first commit データベースの内容がmodelに反映されていない。データベースにはデータがあるのは確認済みだが、djangoに反映されていない。接続に問題はなさそうだ。
mysqlの内容を表示できた　model.pyにmetaクラスを追加して、manage=false db_table = 'responses'というコードを追加した後、python manage.py inspectdb > models.py コマンドを実行して、既存のデータベースからモデルを自動生成。
　　　　　　　　　　　　python manage.py makemigrations　python manage.py maigrateをするとデータを表示できた。また、改行が欲しかったので、list.htmlにquestion|linebreakersbrを追加した。

<h1>AI Review List</h1>
<ul>
{% for review in reviews %}
<li>
<strong>Timestamp:</strong> {{ review.timestamp }}<br>
<strong>Question:</strong> {{ review.question|linebreaksbr }}<br>
<strong>Response:</strong> {{ review.response|linebreaksbr }}<br>
</li>
{% endfor %}
</ul>

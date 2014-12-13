from flask import Flask
from flask import request
from flask import render_template
import sqlite3


app = Flask(__name__)
database = sqlite3.connect("crawl_info.db", check_same_thread=False)
database.row_factory = sqlite3.Row
cursor = database.cursor()


@app.route("/")
def hello():
    file = open("search.html", "r")
    html = file.read()
    file.close()
    return html


@app.route("/search/")
def search_result():
    key_word = request.args.get("search_word", "")
    query = cursor.execute("""SELECT * FROM page WHERE title LIKE ? OR url LIKE ?""",
                           ('%'+key_word+'%', '%'+key_word+'%'))
    result = []
    for row in query:
        result.append([row['title'].decode(encoding='utf-8'), row['url']])
    return render_template("result.html", links=result)


if __name__ == "__main__":
    app.run(debug=True)

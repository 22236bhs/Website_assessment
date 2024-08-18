from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

DATABASE = "SteamDb.db"

@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute("SELECT name, picture_link FROM steam_library ORDER BY hours DESC;")
        names = cursor.fetchall()
    return render_template("index.html", names=names)




if __name__ == "__main__":
    app.run(debug=True)
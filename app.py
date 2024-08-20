from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

DATABASE = "SteamDb.db"

def ExQuery(string):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute()

@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, picture_link FROM steam_library ORDER BY hours DESC;")
        names = cursor.fetchall()
    return render_template("index.html", names=names)

@app.route("/game/<int:id>")
def Game(id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT steam_library.id, name, studios.studio_name, hours, steam_release_date, steam_description, picture_link 
FROM steam_library 
JOIN studios ON steam_library.studio_id = studios.id 
WHERE steam_library.id = ?''', (id,))
        game = cursor.fetchone()
        game = {"id": game[0],
                "name": game[1],
                "studio_name": game[2],
                "hours": game[3],
                "release_date": game[4],
                "description": game[5],
                "pic_link": game[6]}
    return render_template("game.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)
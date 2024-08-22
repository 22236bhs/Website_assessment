from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

DATABASE = "gamedb.db"

def ExQuery(string, params=()):
    with sqlite3.connect(DATABASE) as db:
        return db.cursor().execute(string, params).fetchall()

@app.route("/")
def home():
    names = ExQuery("SELECT id, name, picture_link FROM steam_library ORDER BY hours DESC;")
    return render_template("index.html", names=names)

@app.route("/game/<int:id>")
def Game(id):
    game = ExQuery('''SELECT steam_library.id, name, studios.studio_name, hours, steam_release_date, steam_description, picture_link, my_rating, my_review
FROM steam_library 
JOIN studios ON steam_library.studio_id = studios.id 
WHERE steam_library.id = ?''', (id,))
    game = game[0]
    game = {"id": game[0],
            "name": game[1],
            "studio_name": game[2],
            "hours": game[3],
            "release_date": game[4],
            "description": game[5],
            "pic_link": game[6],
            "my_rating": game[7],
            "my_review": game[8]}
    game["description"] = game["description"].replace("\\n", "\n")
    return render_template("game.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)
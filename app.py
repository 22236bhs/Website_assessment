from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

DATABASE = "gamedb.db"

def ExQuery(string, params=()):
    with sqlite3.connect(DATABASE) as db:
        return db.cursor().execute(string, params).fetchall()

@app.route("/")
def home():
    games = ExQuery("SELECT id, name, picture_link FROM steam_library ORDER BY hours DESC;")
    for i in range(len(games)):
        games[i] = {"id": games[i][0],
                    "name": games[i][1],
                    "pic_link": games[i][2]}
    return render_template("index.html", games=games)

@app.route("/game/<int:id>")
def Game(id):
    game = ExQuery('''SELECT steam_library.id, name, studios.studio_name, hours, steam_release_date, steam_description, picture_link, my_rating, my_review, steam_rating, steam_price
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
            "my_review": game[8],
            "steam_rating": game[9],
            "steam_price": game[10]}
    game["description"] = game["description"].replace("\\n", "\n")
    return render_template("game.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)
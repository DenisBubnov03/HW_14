from flask import Flask, jsonify

from main import DataBaseFilm


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/movie/<title>')
def movie_by_title_page(title):
    return jsonify(DataBaseFilm().get_film_by_title(title))

@app.route('/movie/<int:f_year>/to/<int:s_year>')
def movie_year_to_year_page(f_year, s_year):
    return jsonify(DataBaseFilm().get_film_year_to_year(f_year, s_year))

@app.route('/rating/children/')
def movie_with_rating_children():
    return jsonify(DataBaseFilm().get_film_by_rating(('G', 'G')))

@app.route('/rating/family/')
def movie_with_rating_family():
    return jsonify(DataBaseFilm().get_film_by_rating(("G", "PG", "PG-13")))

@app.route('/rating/adult/')
def movie_with_rating_adult():
    return jsonify(DataBaseFilm().get_film_by_rating(("R", "NC-17")))

@app.route('/genre/<genre>')
def movie_with_description(genre):
    return jsonify(DataBaseFilm().get_film_by_description(genre))


if __name__ == '__main__':
    app.run()

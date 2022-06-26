import json
import sqlite3
from pprint import pp


class DataBaseFilm:
    """init class and connect cursor"""

    def __init__(self, path="netflix.db", name="netflix"):
        self.path = path
        self.name = name

        with sqlite3.connect(path) as connection:
            self.cursor = connection.cursor()

    def get_film_by_title(self, title):
        """get a film list by title"""
        self.cursor.execute("""
                        SELECT title, country, release_year, listed_in, description
                        FROM {}
                        WHERE title = '{}'
                        ORDER BY release_year DESC
                        """.format(self.name, title))

        film_info = self.cursor.fetchone()
        return dict(zip(["title", "country", "release_year", "director", "description"], film_info))

    def get_film_year_to_year(self, first_year: int, second_year: int):
        """get a film list by year to year """
        self.cursor.execute("""
                            SELECT title, release_year
                            FROM {}
                            WHERE release_year BETWEEN {} AND {}
                            LIMIT 100
                            """.format(self.name, first_year, second_year))
        film_infos = self.cursor.fetchall()
        return [dict(zip(["title", "release_year"], film_info)) for film_info in film_infos]

    def get_film_by_rating(self, ratings: str | tuple | list | set):
        """get a film list by rating children/family/adult"""
        self.cursor.execute("""
                            SELECT title, rating, description
                            FROM {}
                            WHERE rating IN {}
                            LIMIT 100
                            """.format(self.name, ratings))
        return [dict(zip(["title", "rating", "description"], film_info)) for film_info in self.cursor.fetchall()]

    def get_film_by_description(self, genre: str):
        """"get a film list by description"""
        self.cursor.execute(f"""
                            SELECT title, description, listed_in
                            FROM {self.name}
                            WHERE listed_in LIKE '%{genre}%'
                            ORDER BY release_year DESC
                            LIMIT 10 
                            """)
        return [dict(zip(["title", "description", "list"], film_info)) for film_info in self.cursor.fetchall()]

    def get_actors(self, *actors):
        """Getting a list of actors who have played more than 2 times"""
        self.cursor.execute(f"""
                            SELECT "cast"
                            FROM {self.name}
                            WHERE "cast" LIKE '%{actors[0]}%'
                            AND "cast" LIKE '%{actors[1]}%'
                            """)
        s_data = self.cursor.fetchall()
        names_actor = []
        for item in s_data:
            names = set(item[0].split(', ')) - set(actors)
            names_actor += list(names)
        return {names for names in names_actor if names_actor.count(names) > 2}

    def get_type_films(self, type, year, genre):
        """Get a json list of movies by type"""
        self.cursor.execute(f"""
                            SELECT title, description
                            FROM {self.name}
                            WHERE "type" LIKE '%{type}%'
                            AND release_year = {year}
                            AND listed_in LIKE '%{genre}%'
                            limit 10
                            """)

        return json.dumps([dict(zip(["title", "description"], film_info)) for film_info in
                           self.cursor.fetchall()])

# for test functions
# print(DataBaseFilm().get_type_films("Movie", 2017, "Dramas"))
# pp(DataBaseFilm().get_actors("Rose McIver", "Ben Lamb"))

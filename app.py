from flask import Flask, render_template, g, request, jsonify
import sqlite3
from flask_wtf import FlaskForm
from wtforms import SelectField
import logging
from spoonacularAPI import Spoonacular
app = Flask(__name__)
app.debug = True

DATABASE = 'database/ingredients.db'
HEADINGS = ("Photo", "Name", "Ingredients")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db_list():
    ls = []
    for ingr in query_db('select * from INGREDIENTS'):
        ls.append((ingr[1]))
    return ls


def fix_input_to_sp(ls: list):
    return ','.join(ls)


@app.route('/', methods=['GET', 'POST'])
def index():
    sp = Spoonacular()
    import pprint
    if request.method == 'POST':
        res = request.form.getlist('ingredients')
        input_str = fix_input_to_sp(res)
        items = sp.get_recipe_with_ingredients(input_str)
        to_show, tuples = sp.to_flask_dict(items)
        return render_template('results.html', data=tuples, headings=HEADINGS)

    ingredients = get_db_list()
    return render_template('index.html', ingredients=ingredients)


if __name__ == "__main__":
    app.run()

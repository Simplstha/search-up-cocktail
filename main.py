from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
alcohol_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i="

load_dotenv("C:\\Users\\sharm\\PycharmProject\\todo-list\\.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/show_cocktail', methods=["GET", "POST"])
def show_cocktail():
    try:
        cocktail = request.form['cocktail']
        tail = cocktail.replace(" ", "_").lower()
        response = requests.get(f"{cocktail_url}{tail}")
        data = response.json()
        ingredients = []
        for i in range(15):
            ingredient = data['drinks'][0][f"strIngredient{i + 1}"]
            if ingredient:
                ingredients.append(ingredient)
        measures = []
        for i in range(15):
            measure = data['drinks'][0][f"strMeasure{i + 1}"]
            if measure:
                measures.append(measure)
        img_url = data['drinks'][0]["strImageSource"]
        instruction = data['drinks'][0]["strInstructions"]
        return render_template('index.html', img_url=img_url, instruction=instruction, measures=measures, ingredients=ingredients)
    except:
        error = "Sorry! The item you searched was not found."
        return render_template('index.html', error=error)


@app.route('/show_info', methods=['GET', 'POST'])
def show_info():
    try:
        alcohol = request.form['alcohol']
        alco = alcohol.replace(" ", "_").lower()
        response = requests.get(f"{alcohol_url}{alco}")
        data = response.json()
        info = data['ingredients'][0]['strDescription']
        return render_template('index.html', info=info)
    except:
        error = "Sorry! The item you searched was not found."
        return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
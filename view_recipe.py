
# from flask import Flask, render_template, request
from flask import Flask
from flask import render_template
from flask import request
import requests
from urllib.parse import unquote

app = Flask(__name__)

API_KEY = '6cd3c6afc5d64d2ab516f2cf5980cefd'


# Define the route for the "Home" button
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html', recipes=[], search_query='')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        query = request.form.get('search_query', '')
        #search for recipes with the given query
        recipes = search_recipes(query)
        # Render the main page with the search results and the search query
        return render_template('index.html', recipes=recipes, search_query=query)
    
    # If it's a GET request or no form submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    
    recipes = search_recipes(decoded_search_query)
    
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)

# function to search for recipes based on the provided query
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    #end a GET request to the Spoonacular API with the query parameters
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:           #200 if successful and 400 if it shows error
        # Parse the API response as JSON data
        data = response.json()
        # Return the list of recipe results
        return data['results']
    # If the API call is not successful
    return []

# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL query parameters
    search_query = request.args.get('search_query', '')
    # Build the URL to get information about the specific recipe ID from Spoonacular API
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    # Send a GET request to the Spoonacular API to get the recipe information
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
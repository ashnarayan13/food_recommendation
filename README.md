# food_recommendation

This is a simple web scraper that gets vegetarian recipes from <https://veenasvegnation.com/>

*Warning - This is simple project to practice webscraping and build a simple recommender*

## Webscraper
The webscraper is written using scrapy.

To create a json file with the recipes

scrapy runspider recipe_scraper.py

## Cleaning the data

The data contains some empty recipes or pages which don't contain well formated HTML recipe lists. These are cleaned.

Since scrapy is asynchronous, the cleaning of the data also arranges the data in order of the recipe 'Name'.

json_writer.py does the cleaning of the json file.

**This has to be done before the running of the recommender**

## Recommender
The recommender reads the json file and uses the ingredients to suggest recipes.

It currently uses the ingredients list to suggest recipes

Input: 
Number of ingredients, Ingredients list.

Output: List of recipes based on ingredients and also the best match (currently just picks the one with the most hits)

The code is availble as jupyter notebook found in recommender.ipynb

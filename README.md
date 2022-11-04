# RoboChef
Rik Peters, 2022
Final project for Ironhack Data Analytics bootcamp

Try it at [https://rjpeters-robochef-robochef-zz6qun.streamlit.app/|this link]

## Introduction
You have some leftovers in your fridge - half an onion, some apples, and lettuce that is about to go bad. What do you do? Wait for it to go bad and throw it out? Put it all into a pan and make soup? Or would you prefer to make something worth eating? 
Enter RoboChef.
RoboChef is an app that recommends ingredients and/or recipes, based on the user's input.  
This prototype recognizes 812 ingredients, and picks its recommendations from a database of over 100,000 recipes, from four different sources. It was written in python, using Streamlit. 

## Table of contents
### The active files
[robochef.py] : the python code for the app itself. 
[requirements.txt] : a list of python modules to load
[data/matrix.csv] : the encoded matrix of ingredients. Each row corresponds to a recipe. 
[data/df_final.csv] : the dataframe with the recipe name, url, and list of ingredients. Indices correspond to the index of the matrix. 

## The background process
The 'notebooks' folder contains the jupyter notebooks where I did all the work. Some of these contain dead ends that did not make it into the final product, in all of them the output has been suppressed to make it easier to scroll through. It's all a bit gory, but here is what happens: 
### Scraping
[notebooks/webscraping.ipynb] : Scraping the New York Times website
[notebooks/webscraping2.ipynb] : Scraping allrecipes.com and epicurious.com
[notebooks/webscraping3.ipynb] : Scraping bonappetit.com
### Cleaning
Note: some of the cleaning was done by hand, line-by-line, in a .txt file. That process is not replicated in these notebooks. 
[notebooks/cleaning_1.ipynb] : Cleaning a kaggle dataset (data from food.com) that I ended up discarding, and applying the same process to the NYT data
[notebooks/cleaning_2.ipynb] : The bulk of the real cleaning.
[notebooks/cleaning_3.ipynb] : Some more cleaning, much of it finally discarded. 
### Exploring
[notebooks/exploration.ipynb] : Exploration: the (successful) attempt to encode the recipes into a matrix of Boolean/numerical values. Includes logistic regression to test how well ingredients can be predicted from other ingredients.
### Building and generating
[notebooks/building.ipynb] : Where I build the function that does the heavy lifting in the app.
[notebooks/generating.ipynb] : Where I generate the final versions of the data, that the app itself uses. 
### Presentation
[presentation/presentation.pdf] : The in-class presentation.

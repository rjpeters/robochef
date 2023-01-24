# Imports
import streamlit as st
import pandas as pd
import random
from textblob import Word
import requests
from nltk.stem import WordNetLemmatizer

# Define 'functions' to load data into user's cache
@st.cache(allow_output_mutation=True)
def get_matrix():
    return(pd.read_csv('data/matrix.csv'))

@st.cache(allow_output_mutation=True)
def get_masterlist():
    return list(get_matrix().columns)

@st.cache(allow_output_mutation=True)
def get_recipes():
    return pd.read_csv('data/df_final.csv', sep = '|')

@st.cache()
def lemmatizer():
    return(WordNetLemmatizer())


# The big function that does the recommending 
def recommend(inputlist, random_rec = True, recipe = False):

    # Load the data
    matrix = get_matrix()
    masterlist = get_masterlist()
    df = get_recipes()
    names = df['name']
    urls = df['url']

    if len(inputlist) == 0:
        if recipe == False:
            index = random.randint(0, len(masterlist))
            return masterlist[index]

        elif recipe == True:
            index = random.randint(0, len(names))
            url = urls[index]
            name = names[index]
            site = url.split('.')[1]
            recommendation = f"[{name}]({url})"
            return (recommendation, len(names), site)


    # Deal with the first ingredient directly from the matrix
    options = matrix[matrix[inputlist[0]]==1].copy()
    
    # Check if there are any other ingredients
    if len(inputlist)>1:
        for i in range(1, len(inputlist)):
            options = options[options[inputlist[i]]==1].copy()
   
    # Generate a droplist. First add the ingredients from the input: 
    # These need to be dropped so that you don't recommend the imput itself.
    droplist = []
    for item in inputlist: 
        droplist.append(item)
    
    # Then add all the 'irrelevant' columns to the droplist
    for column in masterlist: 
        if options[column].sum() == 0: 
            droplist.append(column)
    
    # Then drop those columns
    options.drop(columns = droplist, inplace = True)
    
    # Get list of relevant columns (column names of 'options')
    mylist = [item for item in masterlist if item not in droplist]
                     
    
    # Here comes the actual recommendation: 
    if recipe == False:
        # First option: totally random recommendation 
        # Picked from ingredients that occur in combination with the input ingredients at least once
        if random_rec == True: 
            recommendation = mylist[random.randint(0, (len(mylist)-1))]
            return recommendation

        # Second option: non-random recommendation
        # Option 2a: the 'most likely' next ingredient
        elif random_rec == False: 
            countlist = []
            for column in mylist: 
                countlist.append(options[column].sum())

            # This is an obvious point at which I could refine the process some more: 
            # divide the possibilities into groups depending on their likelihood

            recomm_index = countlist.index(max(countlist))
            recommendation = mylist[recomm_index]
            return recommendation

    # Recommend a recipe containing the ingredients
    elif recipe == True:
        indexoptions = list(options.index)
        chosenindex = random.randint(0, len(options)-1)
        myrecipe = indexoptions[chosenindex]
        url = urls[myrecipe]
        site = url.split('.')[1]
        name = names[myrecipe]
        recommendation = f"[{name}]({url})"
        return (recommendation, len(indexoptions), site)
        # This returns a tuple, with item 0 being the recipe, 
        # item 1 being the number of available recipes with that list  
    




# The app itself

st.markdown("<h1 style='text-align: center'>RoboChef</h1>", unsafe_allow_html=True)

#col1, col2, col3 = st.columns(3)
#with col2:
#    st.image("logo.png")


st.markdown("<p style='text-align: center'>Enter ingredients, get recommendations</p>", unsafe_allow_html=True)



# Placeholder for list of input
@st.cache(allow_output_mutation=True)
def get_data():
    return []

# input form
with st.form("ingr_input"):
    text = st.text_input(label = 'Enter ingredient')

    submitted = st.form_submit_button("Submit", type = 'primary')

    if submitted:
        if text.strip() == '':
            pass
        else: 
            result = Word(text).correct()

            #Scenario 1: the input ingredient is in the masterlist.
            if result.lower() in get_masterlist():
                get_data().append(result.lower())
            else:
                #Try to lemmatize
                newresult = lemmatizer().lemmatize(result)
                if newresult in get_masterlist():
                    get_data().append(newresult.lower())
                else:
                #Scenario 2: lemmatization does not work
                    try: 
                        for item in get_masterlist():
                            if newresult in item:
                                st.write(f"Expanded {newresult} to {item}")
                                get_data().append(item)
                                break
                    except:
                        st.write("Unknown ingredient")




# Save the output into cache, to allow further use
@st.cache(allow_output_mutation=True)
def store_output():
    return []

col1, col2, col3 = st.columns(3)

# Recommendation buttons. 1: ingredient
with col1: 
    ing = st.button("Recommend ingredient", type = 'primary')
    if ing:
        recommendation = recommend(get_data())
        store_output().append(recommendation)
    # Possibility to add the output ingredient to your input list
    try:
        if st.button(store_output()[-1]):
            get_data().append(store_output()[-1])
            store_output().clear()
    except:
        pass
# store_output().clear()





with col2: 
    pass

# Recommendation buttons. 2: recipe
with col3:
    rec = st.button("Recommend recipe", type = 'primary')
    if rec:

        recipe = recommend(get_data(), recipe = True)
        print(recipe)
        try:
            recipe = recommend(get_data(), recipe = True)
            st.write(recipe[0])
            st.write(f'Source: {recipe[2]}')
            st.write(f"({recipe[1]} recipes found with these ingredients)")
        except: 
            st.write("Sorry, no recipe found. Maybe delete some ingredients and try again?")
col1, col2, col3 = st.columns(3)

#Show the input, with the option to clear all

with col2:
    st.write("You entered: ")
    for i in range(len(get_data())): 
        try:
            ingredient = get_data()[i]
        
            if st.button(ingredient, key = i):
                get_data().remove(ingredient)
        except: 
            pass

    clearall = st.button("Clear all", type = 'primary')
    if clearall == True:
        get_data().clear()
        store_output().clear()

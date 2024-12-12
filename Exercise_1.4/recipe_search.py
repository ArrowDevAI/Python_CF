import pickle
import os
import sys

def load_data(file):   
    # Check if the user wants to abort or create a new file
    while True:
        if file.lower() == 'exit':
            print('*')
            print("Input Aborted by User")
            print('*')
            sys.exit()

        if file.lower() == 'create':
            # Logic for creating a new file
            while True:
                new_filename = input("Enter the name of the new file (e.g., 'holiday_recipes.bin'): ")
                
                if not new_filename.lower().endswith('.bin'):
                    print("Error: File must have a .bin extension. Please try again.")
                    continue  # Prompt for a valid filename again
                
                if os.path.exists(new_filename):
                    print(f"Error: The file '{new_filename}' already exists. Please choose a different name.")
                    continue  # Prompt for a different name if the file exists
                
                try:
                    # Create a new file with initial empty data
                    data = {"Ingredients List" : [], "Recipes List": []}
                    with open(new_filename, 'wb') as new_file:
                        pickle.dump(data, new_file)
                        print(f"File '{new_filename}' created successfully. Run Script again to use.")
                    sys.exit()
                except Exception as error:
                    print(f"An unexpected error occurred while creating the file: {error}")
                    
        
        elif os.path.exists(file):
            try:
                # If the file exists, load the data
                with open(file, 'rb') as ingredients_file:
                    data = pickle.load(ingredients_file)
                    print("Data loaded successfully.")
                    return data  # Return the loaded data
            except Exception as error:
                print("!")
                print(f"An unexpected error occurred while handling the file: {error}")
                print("!")
        
        else:
            # If the file doesn't exist, prompt again
            print("!")
            print(f"File '{file}' does not exist. Try again or type 'create' to create a new file, or enter 'exit' to abort.")
            print("!")
            file = input("Enter Filename For Ingredients List: ")
          
        

# Example of calling the function with a filename
filename = input("Enter Filename For Ingredients List: ")
data = load_data(filename)

def display_recipe(recipe_data):
    for recipe in recipe_data:
        recipe_name = recipe["Name"]
        recipe_ingredients = recipe["Ingredients"]
        recipe_difficulty = recipe["Difficulty"]
        recipe_cooktime = recipe["Cook Time"]
        print("----------------------------------")
        print(f"Name: {recipe_name}")
        print("Ingredients:")
        for ingredient in recipe_ingredients:
            print(f"- {ingredient}")
        print(f"Cook Time: {recipe_cooktime} minutes")
        print(f"Difficulty: {recipe_difficulty}")
        print("----------------------------------")

def search_Ingredient(data):
    # Print the ingredients list
    ingredients = list(enumerate(data["Ingredients List"], 1))
    for item in ingredients:  
        print(f"Item {item[0]}: {item[1]}")
    
    if not ingredients:
        print("No Ingredients in this List")
        return  # Exit the function if there are no ingredients

    matched_ingredient = None  # Initialize matched_ingredient

    while matched_ingredient is None:  # Keep looping until a valid ingredient is found
        try:
            ingredient_searched = input("Select a number to find recipes with that ingredient: ").strip()

            # If the input is empty, prompt again
            if not ingredient_searched:
                print("No input provided. Please select a valid ingredient number.")
                continue  # Re-prompt the user for input

            ingredient_searched = int(ingredient_searched)

            # Search for the matching ingredient
            for ingredient in ingredients:
                if ingredient[0] == ingredient_searched:
                    matched_ingredient = ingredient
                    break  # Exit the loop once a match is found

            if matched_ingredient is None:
                print("Please choose a valid number from the list.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as error:
            print(f"An error occurred: {error}")

    # Print the matched recipe or notify no match
    if matched_ingredient:
        recipes = data["Recipes List"]
        print("Ingredient: ", matched_ingredient[1])
        print(f"Recipe(s) with {matched_ingredient[1]}:")
        for recipe in recipes:
            for ingredient in recipe["Ingredients"]:
                if ingredient == matched_ingredient[1]:
                    matched_recipe = recipe
                    print("--------------------------------")
                    print(f"Name: {matched_recipe['Name']}")
                    print(f"Cook Time: {matched_recipe['Cook Time']} minutes")
                    print(f"Difficulty: {matched_recipe['Difficulty']}")
                    print("Ingredients:")
                    for ingredient in matched_recipe["Ingredients"]:
                        print(f"  - {ingredient}")

# execute function if the user does not exit or create a new .bin file
if filename != 'exit' and filename != 'create':
    search_Ingredient(data)


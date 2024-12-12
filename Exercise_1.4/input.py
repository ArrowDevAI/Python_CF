import pickle
import os
while True:
    filename = input("Enter the Filename where you will store your recipe(s): ")    
# If the user chooses to exit early
    if filename.lower() == 'exit':
        
        print('*')
        print("Input Aborted by User")
        print('*')
        break
# If the user chooses to create a new .bin file
    if filename.lower() == 'create':
        while True:
            new_filename = input("Enter the name of the new file (e.g., 'holiday_recipes.bin'): ")
        
        # Check if the filename ends with .bin extension
            if not new_filename.lower().endswith('.bin'):
                print("Error: File must have a .bin extension. Please try again.")
                continue  # Prompt the user to enter a valid file name again
            if os.path.exists(new_filename):
                print(f"Error: The file '{new_filename}' already exists. Please choose a different name.")
                continue
            try:
            # Attempt to create the file 
                data = {"Ingredients List" : [],"Recipes List": []}
                with open(new_filename, 'wb') as new_file:
                    pickle.dump(data, new_file)
                    print(f"File '{new_filename}' created successfully.")
                break  # Break out of the loop if the file is created successfully
            except Exception as error:
                print(f"An unexpected error occurred while creating the file: {error}")
            # Let the user retry in case of error
                continue
# If the filename is found in the current directoy
    elif os.path.exists(filename):
        try:
            with open(filename, 'rb') as recipe_file:  # Open the file in read-binary mode
                data = pickle.load(recipe_file)  # Load the existing data (if necessary)
                print("File loaded successfully.")

                recipes_list = data["Recipes List"]
                all_ingredients = data["Ingredients List"]
                
                break         
        except Exception as error:
            print("!")
            print(f"An unexpected error occurred while handling the file: {error}")
            print("!")

   
# If the filename is not found   
    else:
        print("!")
        print(f"File '{filename}' does not exist. Try again or type 'create' to create a new file, or enter 'exit' to abort.")
        print("!")
while True:
        try:
            num_recipe = int(input("How many recipes would you like to enter? :"))
            break
        except ValueError:
            print("Please Enter a Valid Number")
       
 # Function to calculate difficulty of each recipe in the recipes_list
def calc_difficulty(recipe):
    cook_time = recipe["Cook Time"]
    num_ingredients = len(recipe["Ingredients"])
    if num_ingredients < 4 and cook_time < 10:
        difficulty = "Easy"
    elif cook_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cook_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else: 
        difficulty = "Hard"
    recipe["Difficulty"] = difficulty
# Function allowing users to add a recipe
def take_recipe(): 
    ingredients = []
    while True:
            name = input("Recipe Name: ").strip()
            if len(name) > 0 and not name.isdigit():
                break
            else:
                print("Please Enter a Valid Name")
    while True:
        try:
            cook_time=int(input("Cook Time (in minutes): ").strip())
            break
        except ValueError:
            print("Please Enter Valid number")
    while True:
        ingredient = input("Enter an Ingredient (type 'done' when finished) : ").strip()
        if len(ingredient)<=0:
            print("Enter Valid Ingredient")
            continue
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    recipe = {"Name": name, "Cook Time": cook_time, "Ingredients": ingredients, "Difficulty":""}
    
    calc_difficulty(recipe)
    print("---------------------------------------------------")
    print(f"Name: ", recipe["Name"])
    print(f"Cook Time: {recipe['Cook Time']} minutes")
    print("Ingredients:")
    for ingredient in recipe["Ingredients"]:
        print(f"  - {ingredient}")
    print(f"Difficulty: ", recipe["Difficulty"])
    print("---------------------------------------------------")
    recipes_list.append(recipe)
    for ingredient in recipe["Ingredients"]:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)   

for _ in range(num_recipe):
        take_recipe()


print("Recipe Added Successfully")
   
# run functions for num_recipe, add ingredients to ingredients_list if it is not present
data = {"Ingredients List": all_ingredients, "Recipes List": recipes_list}

with open(filename, "wb") as file:
    pickle.dump(data, file)
print("Recipe Stored")


        
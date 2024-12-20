import mysql.connector
import sys

# Establish connection to mySQL and print if succesful

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    passwd = 'password',
    database = 'task_database'
)

cursor = conn.cursor()
cursor.execute("USE task_database")
cursor.execute("SELECT DATABASE()")
current_database=cursor.fetchone()
if conn:
    print(f"Connected to Database: {current_database}\n")

# main menu functions

def create_recipe(conn, cursor):

    while True:
        name = input("\nName: ")
        if len(name) < 1:
            print("Enter a valid name")
        else:
            break  # Exit the loop if a valid name is entered
    # Request Cook Time
    while True:
        try:
            cooking_time = int(input("Cook Time (in Minutes): "))
            if cooking_time <= 0:
                print("Please enter a positive number for cook time.")
                continue
            break  # Exit the loop if a valid cooking time is entered
        except ValueError:
            print("Please enter a valid number for cook time.")
    #Gather Ingredients
    ingredients = []
    while True:
        ingredient = input("Enter an Ingredient (type 'done' when finished) : ").strip()
        if len(ingredient)<=0:
            print("Enter Valid Ingredient")
            continue
        if ingredient.lower() == 'done':
            break
     
        ingredients.append(ingredient)

    recipe_ingredients = ','.join(ingredients)
    difficulty = calc_difficulty(cooking_time,recipe_ingredients)

    sql = ('''INSERT INTO recipes
    (name, cooking_time, ingredients, difficulty) 
    VALUES (%s, %s, %s, %s)''')

    val = (name, cooking_time, recipe_ingredients, difficulty)

    print(f"{val} = RECIPE ")

    cursor.execute(sql,val)
    conn.commit()

    print(f"Recipe '{name}' created and added to Recipes ")

    main_menu(conn, cursor)

def calc_difficulty(cook_time, ingredients):
    num_ingredients = len(ingredients)
    if num_ingredients < 4 and cook_time < 10:
        difficulty = "Easy"
    elif cook_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cook_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else: 
        difficulty = "Hard"
    return difficulty
        
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()
    all_ingredients = []

    for recipe in results:
        ingredients = recipe[0].split(',')
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
        if not ingredients:
            print("No Ingredients in this List")

    print("All Ingredients:\n")
    ingredients = list(enumerate(all_ingredients, 1))
    for item in ingredients:  
        print(f"Item {item[0]}: {item[1]}")

    matched_ingredient = None  # Initialize matched_ingredient

    while matched_ingredient is None:  # Keep looping until a valid ingredient is found
        try:
            ingredient_searched = input("\nSelect a number to find recipes with that ingredient: ").strip()

            # If the input is empty, prompt again
            if not ingredient_searched:
                print("No input provided. Please select a valid ingredient number.\n")
                continue  # Re-prompt the user for input

            ingredient_searched = int(ingredient_searched)

            # Search for the matching ingredient
            for ingredient in ingredients:
                if ingredient[0] == ingredient_searched:
                    matched_ingredient = ingredient
                    break  # Exit the loop once a match is found

            if matched_ingredient is None:
                print("Please choose a valid number from the list.")
                continue

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as error:
            print(f"An error occurred: {error}")

    if matched_ingredient:
        print(f"Ingredient Selected: {matched_ingredient[1]}\n")
    cursor.execute("SELECT * from recipes")
    all_recipes = cursor.fetchall()
   
    for recipe in all_recipes:
        for ingredient in recipe[2].split(','):
            if matched_ingredient[1].lower() == ingredient.lower():
                print(f"Recipes with {matched_ingredient[1]}: \n")
                print(f"Name: {recipe[1]}")
                print("Ingredients:")

                list_ingredients = recipe[2].split(',')
                for ingredient in list_ingredients:
                    print(f"  - {ingredient}")
                print(f"Cook Time (minutes): {recipe[3]}")
                print(f"Difficulty: {recipe[4]}\n")
                break
    main_menu(conn, cursor)

def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()

    recipes = list(enumerate(results, 1))

    # Display available recipes
    for item in recipes:
        print(f"\nItem {item[0]}: {item[1][1]}")

    # Select a recipe to update
    to_update = int(input("\nChoose a Recipe by number to update: "))
    
    for recipe in recipes:
        if recipe[0] == to_update:
            selected_recipe = recipe
            break

    if not selected_recipe:
        print("Invalid selection.")
        return

    # Display details of the selected recipe
    print(f"\n1. Name: {selected_recipe[1][1]}")
    list_ingredients = selected_recipe[1][2].split(',')
    print("2. Ingredients: ")
    for ingredient in list_ingredients:
        print(f"  - {ingredient}")
    print(f"3. Cook Time (minutes): {selected_recipe[1][3]}")

    # Select column to update
    selected_column = input("\nSelect the number of what you will update: ")

    if selected_column == '1':
        new_name = input("\nInput New Name: ")
        sql = 'UPDATE recipes SET name=%s WHERE id=%s'
        val = (new_name, selected_recipe[1][0])
        cursor.execute(sql, val)
        conn.commit()
        print(f"\nRecipe name updated successfully to {new_name}")

    elif selected_column == '2':
        new_ingredients=[]
        while True:
            new_ingredient = input("\nInput New Ingredient (type 'done' when finished): ")
            if new_ingredient.lower() == 'done':
                break
            if new_ingredient not in new_ingredients:
                new_ingredients.append(new_ingredient)

        difficulty = calc_difficulty(selected_recipe[1][3],new_ingredients)
        list_ingredients.extend(new_ingredients)
        updated_ingredients = ','.join(list_ingredients)
        sql = "UPDATE recipes SET ingredients=%s, difficulty=%s WHERE id=%s"
        val = (updated_ingredients, difficulty, selected_recipe[1][0])
        cursor.execute(sql, val)
        conn.commit()
        print("\nIngredients updated successfully!")

    elif selected_column == '3':
        list_ingredients = selected_recipe[1][2].split(',')
        new_cook_time = int(input("\nInput New Cook Time (in minutes): "))
        difficulty = calc_difficulty(new_cook_time,list_ingredients)
        sql = 'UPDATE recipes SET cooking_time=%s, difficulty=%s WHERE id=%s'
        val = (new_cook_time, difficulty, selected_recipe[1][0])
        cursor.execute(sql, val)
        conn.commit()
        print(f"\nCook time updated successfully to {new_cook_time} minutes")

    else:
        print("\nInvalid option selected.")
    main_menu(conn,cursor)

def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()

    if not results:
        print("No recipes found to delete.")
        main_menu(conn, cursor)
        return

    # Display available recipes
    print("\nAvailable Recipes:")
    recipes = list(enumerate(results, 1))
    for item in recipes:
        print(f"\nItem {item[0]}: {item[1][1]}")  # Display recipe names with item number

    # Select a recipe to delete
    try:
        to_delete = int(input("\nChoose a Recipe by number to delete: "))
        if to_delete < 1 or to_delete > len(recipes):
            print("Invalid selection. Please choose a valid recipe number.")
            delete_recipe(conn, cursor)
            return

        selected_recipe = recipes[to_delete - 1]  # Select recipe based on user input

        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete the recipe '{selected_recipe[1][1]}'? (y/n): ").lower()
        if confirm == 'y':
            sql = 'DELETE FROM recipes WHERE id=%s'
            val = (selected_recipe[1][0],)
            cursor.execute(sql, val)
            conn.commit()
            print(f"\nRecipe '{selected_recipe[1][1]}' has been deleted.")
        else:
            print("\nDeletion canceled.")

    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
    
    main_menu(conn, cursor)

def main_menu(conn, cursor):
    
    print("\nWhat would you like to do?\n")
    print("1. Create a new recipe")
    print("2. Search for a recipe")
    print("3. Update a recipe")
    print("4. Delete a recipe\n")
    print("Type 'quit' to exit the program\n")

    
    while True:
        choice = input("Input choice: ")

        if choice.lower() == "quit":
            print('\nExiting...')
            conn.close()
            print('\nDatabase Connection Closed')
            sys.exit()
        elif choice == "1":
            create_recipe(conn,cursor)
            break
        elif choice == "2":
            search_recipe(conn,cursor)
            break
        elif choice == "3":
            update_recipe(conn,cursor)
            break
        elif choice == "4":
            delete_recipe(conn,cursor)
            break
        else:
            print(f"\nPlease Enter a number from the list or type 'quit' \n")
            continue

if __name__ == "__main__":
    try:
        main_menu(conn, cursor)
    except KeyboardInterrupt:
        print('\nExiting...')
        conn.close()
        print('\nDatabase Connection Closed')
        sys.exit()
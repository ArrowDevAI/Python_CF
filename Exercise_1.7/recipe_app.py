from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
import sys

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + "Name: " + self.name + " " + "Difficulty: " + self.difficulty + ">" 
    
    def __str__(self):
        output= "Name: " + self.name + '\n'
        output += "Ingredients: \n"
        for ingredient in self.ingredients.split(","):
            output+= "\t - " + ingredient.strip() + "\n"
        output+= "Difficulty: " + self.difficulty + "\n"
        output+= "Cooking Time (minutes): " + str(self.cooking_time)

        return output
    
    def calc_difficulty(self):

        cook_time = self.cooking_time
        num_ingredients = len(self.ingredients)

        if num_ingredients < 4 and cook_time < 10:
            self.difficulty = "Easy"
        elif cook_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif cook_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else: 
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        
        return self.ingredients.split(',')

Base.metadata.create_all(engine)
    
def create_recipe():
    while True:
        try:
            recipe_name = input("Enter Recipe Name: ")
            if recipe_name.isnumeric():
                print("Please Enter a valid Name")
                continue
           
            elif len(recipe_name) <= 50:
                break
            
            else:
                print("Recipe Name has too many characters. Try again.")
        except ValueError:
            print("Enter Valid Name")

    while True:
            try:
                cooking_time = int(input("Cooking Time (In Minutes): "))
                if cooking_time <= 0:
                    print("Please enter a valid positive number for cooking time.")
                else:
                    break
            except ValueError:
                    print("Please enter a valid number.")
        
    num_ingredients = int(input("How many ingredients would you like to add?: "))
    ingredients = []

    for i in range(num_ingredients):
        ingredient = input(f"Ingredient {i+1}: ")
        ingredients.append(ingredient.strip())
        
    ingredients_list = ','.join(ingredients)
    
    recipe_entry = Recipe (
        name = recipe_name,
        ingredients = ingredients_list,
        cooking_time = cooking_time,
        difficulty = ''
    )
    recipe_entry.calc_difficulty()

    session.add(recipe_entry)
    session.commit()

    print("Recipe Added Successfully.")

def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no entries in the database.")
        return None
    for recipe in recipes:
        print(recipe)
        return None

def search_by_ingredients():
    count = session.query(Recipe).count()
    if not count:
        print("No Entries Found")
        return None

    #Retrieve list of all recipes
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []

    #Parse each tuple for the ingredients and populate all_ingredients (without repeating)
    for recipe in results:
        ingredients = recipe[0]
        split_ingredients = ingredients.split(',')
        for ingredient in split_ingredients:
            ingredient = ingredient.strip()
            if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

    #Print numbered list for user to view          
    print("Ingredients List")
    ingredient_list = [(index, ingredient.strip()) for index, ingredient in enumerate(all_ingredients, start=1)]
    for item in ingredient_list:
        print(f"{item[0]}. {item[1]}")

    
    # Gather list of chosen recipes by number
    while True:
        try:
            total_ingredients = len(all_ingredients)
            ingredient_nums = input("Select the number(s) of an ingredient to retrieve corresponding recipes (separated by spaces): ")
            num_list = ingredient_nums.strip().split()
            joined_nums = [','.join(num_list)]
            
            for i in num_list:
                i = int(i)
                if i > total_ingredients:
                    print(f"{i} is not on the list.")
                    raise ValueError
    
        except ValueError:
            print("Please enter valid number(s) within the list range (separated by spaces).\n")
            continue
        else:
            break

    #Retrieve the ingredients associated with the user selected numbers and store them 
    searched_ingredients=[]        
    for i in ingredient_list:
            index=int(i[0])
            for n in num_list:
                n = int(n)
                if index == n:
                    searched_ingredients.append(i[1])
    conditions = []
    for r in searched_ingredients:
        like_term = Recipe.ingredients.like(f"%{r}%")
        conditions.append(like_term)
    
    matched_recipes = session.query(Recipe).filter(*conditions).all()
    if len(matched_recipes) == 0:
            print("No Recipes Match all Ingredients")
            return None
    else:
        for recipe in matched_recipes:
            print(str(recipe))

def edit_recipe():
    count = session.query(Recipe).count()
    if not count:
        print("No Entries Found")
    # Initialize an empty list for all recipes
    results = []
    # Retrieve all recipes  
    results = session.query(Recipe.name).all()
    num_results = len(results)
    # Display all recipes for user to choose
    print("\nRecipes Available\n")

    enum_results = []
    for index, (name,) in enumerate(results, start=1):
        enum_results.append((index,name))
        print(f"{index}. {name}")
    
    while True:
        try:
            selected_recipe = int(input("\nChoose recipe to be edited by entering associated number: "))
            if selected_recipe > num_results:
                print("Please Select a number from Recipes Available.")
                continue
            break
        except ValueError:
            print("Please Input a Valid Selection")
        
    for r in enum_results:
        if r[0] == selected_recipe:
            recipe_name = r[1]
            print(f"\nRecipe to Edit: {r[1]}\n")
    
    recipe_to_edit = session.query(Recipe).filter(Recipe.name == recipe_name).one()
    
    while True:  
        print(f"1. Name: {recipe_to_edit.name}")
        print(f"2. Ingredients: {recipe_to_edit.ingredients}")
        print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")
        
        try:
            selection = int(input(f"\nChoose a number of the section to edit: "))
        except ValueError:
            print("Please Input a Valid Selection")
            continue

        if selection == 1:
            new_name = input("\nInput New Name: ")
            session.query(Recipe).filter(Recipe.name == recipe_name).update({Recipe.name: new_name})
            session.commit()
            print(f"\nSuccessfully Updated Name from {recipe_name} to {new_name}")
            break
            return None

        elif selection == 2:
            new_ingredients = []
            current_ingredients = recipe_to_edit.ingredients.split(', ')
            while True:
                new_ingredient = input("\nInput New Ingredient (type 'done' when finished): ")
                if new_ingredient.lower() == 'done':
                    break
                if new_ingredient not in new_ingredients:
                    new_ingredients.append(new_ingredient.strip())

            all_ingredients = current_ingredients + new_ingredients
            new_ingredients_str = ', '.join(all_ingredients)
            session.query(Recipe).filter(Recipe.name == recipe_name).update({Recipe.ingredients: new_ingredients_str})
            session.commit()
            print("\nSuccessfully Updated Ingredients list")
            break
            return None  

        elif selection == 3:
            new_cook_time = int(input("\nInput New Cook Time (in minutes): "))
            session.query(Recipe).filter(Recipe.name == recipe_name).update({Recipe.cooking_time: new_cook_time})
            session.commit()
            print(f"\nNew Cooking Time set to {new_cook_time} minutes")
            break  
        else:
            print("\nInvalid option selected. Please choose a valid option.")
            continue  
    
    session.refresh(recipe_to_edit)
    recipe_to_edit.calc_difficulty()
    session.commit()

def delete_recipe():
    count = session.query(Recipe).count()
    if not count:
        print("No Entries Found")
    # Initialize an empty list for all recipes
    results = []
    # Retrieve all recipes  
    results = session.query(Recipe.name).all()
    num_results = len(results)
    # Display all recipes for user to choose
    print("\nRecipes Available\n")

    enum_results = []
    for index, (name,) in enumerate(results, start=1):
        enum_results.append((index,name))
        print(f"{index}. {name}")
    
    while True:
        try:
            num_to_delete = int(input("\nEnter the corresponding number of the recipe to be deleted: \n"))
            if num_to_delete < 1 or num_to_delete > num_results:
                print("\nPlease Choose a valid Number\n")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    for r in enum_results:
        if r[0] == num_to_delete:
            recipe_to_delete = r
      

    del_selection = input(f"Are you sure you want to delete {recipe_to_delete[1]}? :  y / n : ")
    recipe_to_be_deleted = session.query(Recipe).filter(Recipe.name == recipe_to_delete[1]).one()
    if del_selection.lower() == 'y':
        session.delete(recipe_to_be_deleted)
        session.commit()
        print(f"Successfully Deleted {recipe_to_delete[1]}")
        return None

    if del_selection.lower() == 'n':
        print("\nAborted Delete")
        return None
     
def main_menu():
    
    print("---" * 15)
    print("\nWhat would you like to do?\n")
    print("1. Create a new recipe")
    print("2. View All Recipes")
    print("3. Search for Recipes by Ingredients")
    print("4. Edit a recipe")
    print("5. Delete a recipe")
    print("Type 'quit' to exit the program\n")

    
    while True:
        choice = input("Input choice: ")

        if choice.lower() == "quit":
            print('\nExiting...')
            session.close()
            print('\nDatabase Connection Closed')
            sys.exit()
        elif choice == "1":
            create_recipe()
            break
        elif choice == "2":
            view_all_recipes()
            break
        elif choice == "3":
            search_by_ingredients()
            break
        elif choice == "4":
            edit_recipe()
            break
        elif choice == "5":
            delete_recipe()
            break
     
        else:
            print(f"\nPlease Enter a number from the list or type 'quit' \n")
            continue

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nExiting...')
        session.close()
        print('\nDatabase Connection Closed')
        sys.exit()

main_menu()
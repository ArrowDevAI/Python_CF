recipes_list = []
ingredients_list = []

while True:
    try:
        n = int(input("How Many Recipes Would You Like to enter? : "))
        break
    except ValueError:
            print("Please enter valid number")


def take_recipe():
    ingredients = []
    
    while True:
        name = input("Recipe Name: ")
        letter_count = len(list(filter(str.isalpha, name)))
        if letter_count > 0 :
            break
        else:
            print("Plese Enter Valid Name")
  
    while True :
        try:
            cook_time = int(input("Cook Time (in minutes): "))
            break
        except ValueError:  
            print("Please enter a valid number.")
    
    while True:
        ingredient = input("Enter an Ingredient (type 'done' when finished): ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
        
    recipe = {"Name": name, "Cook Time": cook_time, "Ingredients": ingredients, "Difficulty":""}
    recipes_list.append(recipe)

for _ in range(n):
    take_recipe()
    for recipe in recipes_list:
         for ingredient in recipe["Ingredients"]:
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)
for recipe in recipes_list:
        cook_time = recipe["Cook Time"]
        num_ingredients = len(recipe["Ingredients"])
        if cook_time < 10 and num_ingredients < 4:
             difficulty = "Easy"
        elif cook_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cook_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        else:  # cook_time >= 10 and num_ingredients >= 4
            difficulty = "Hard"

        recipe["Difficulty"] = difficulty

               

print("\nRecipes List:")
for recipe in recipes_list:
    print(f"Recipe: {recipe['Name']}, Cook Time: {recipe['Cook Time']} minutes, Ingredients: {', '.join(recipe['Ingredients'])}, Difficulty: {recipe['Difficulty']}")
print("\nAll Ingredients Through all Recipes")
for ingredient in ingredients_list:
    print(ingredient)


class Recipe:

    all_ingredients = []
    recipes_list = []

    def __init__(self, name, ingredients, cook_time, difficulty):
        self.name = name
        self.ingredients = ingredients
        self.cook_time = cook_time
        self.difficulty = difficulty

        Recipe.recipes_list.append(self)
    
    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_cook_time(self):
        return self.cook_time
    
    def set_cook_time(self, new_time):
        self.cook_time = new_time
        

    def add_ingredients(self):
        while True:
            ingredient = input("Enter an Ingredient (type 'done' when finished) : ").strip()
            if len(ingredient)<=0:
                print("Enter Valid Ingredient")
                continue
            if ingredient.lower() == 'done':
                break
            if not ingredient in self.ingredients:
                self.ingredients.append(ingredient)
                self.update_all_ingredients()
            else:
                print(f"{ingredient} is already in the list. Try another ingredient.")

    def getIngredents(self):
           return self.ingredients

    def calc_difficulty(self):

        cook_time = self.cook_time
        num_ingredients = len(self.ingredients)

        if num_ingredients < 4 and cook_time < 10:
            self.difficulty = "Easy"
        elif cook_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif cook_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else: 
            self.difficulty = "Hard"

        return self.difficulty
    
    def get_difficulty(self):
        output = self.difficulty
        if not self.difficulty:
            self.calc_difficulty()
        return self.difficulty()

    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                    Recipe.all_ingredients.append(ingredient)
    
    @staticmethod
    def recipe_search(recipes, search_term):
        for recipe in recipes:
            if recipe.search_ingredient(search_term):
                print(recipe, "\n")
        print("--------------------------------")
        
    def __str__(self):
        return f"Recipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCook Time: {self.cook_time} minutes\nDifficulty: {self.difficulty}"


tea = Recipe(
    name="Tea",
    ingredients=["Tea Leaves", "Sugar", "Water"],
    cook_time=5,
    difficulty=''
)
tea.calc_difficulty()


coffee = Recipe(
    name = "Coffee",
    ingredients=["Sugar","Butter","Eggs","Vanilla Extract", "Flour", "Baking Powder", "Milk"],
    cook_time = 5,
    difficulty = ''
)
coffee.calc_difficulty()

smoothie = Recipe(
    name = "Banana Smoothie",
    ingredients = ["Bananas", "Milk","Peanut Butter", "Sugar", "Ice Cubes"],
    cook_time = 5,
    difficulty = ''
)
smoothie.calc_difficulty()

print("\nSearching for ingredients with Water in the recipes: \n")
Recipe.recipe_search(Recipe.recipes_list, "Water")

print("\nSearching for ingredients with Sugar in the recipes: \n")
Recipe.recipe_search(Recipe.recipes_list, "Sugar")

print("\nSearching for ingredients with Bananas in the recipes: \n")
Recipe.recipe_search(Recipe.recipes_list, "Bananas")

print("\nAll recipes in recipes_list: \n")
for recipe in Recipe.recipes_list:
    print(recipe, "\n")  
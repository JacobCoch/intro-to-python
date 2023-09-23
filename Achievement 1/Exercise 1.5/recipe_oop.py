class Recipe:
    # Class variable to store all ingredients
    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficulty = ""

    # Getter method for name
    def get_name(self):
        return self.name

    # Setter method for name
    def set_name(self, name):
        self.name = name

    # Getter method for cooking_time
    def get_cooking_time(self):
        return self.cooking_time

    # Setter method for cooking_time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # Add ingredients to the recipe
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()

    # Getter method for ingredients
    def get_ingredients(self):
        for ingredient in self.ingredients:
            print("-" + ingredient)

    def calculate_difficulty(self, cooking_time, ingredients):
        if (cooking_time < 10) and (len(ingredients) < 4):
            difficulty_level = "Easy"
        elif (cooking_time < 10) and (len(ingredients) >= 4):
            difficulty_level = "Medium"
        elif (cooking_time >= 10) and (len(ingredients) < 4):
            difficulty_level = "Intermediate"
        elif (cooking_time >= 10) and (len(ingredients) >= 4):
            difficulty_level = "Hard"
        else:
            print("Something bad happened, please try again")

        return difficulty_level

    # Getter method for difficulty
    def get_difficulty(self):
        difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)
        output = "Difficulty: " + str(self.cooking_time)
        self.difficulty = difficulty
        return output

    # Search for ingredients in the recipe
    def search_ingredients(self, ingredient, ingredients):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    # Update the all_ingredients list
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.add(ingredient)

    # method to print the recipe details
    def __str__(self):
        output = (
            "Name: "
            + self.name
            + "\nCooking Time (in minutes): "
            + str(self.cooking_time)
            + "\nIngredients: "
            + str(self.ingredients)
            + "\nDifficulty: "
            + str(self.difficulty)
            + "\n--------------------------"
        )
        return output

    # Class method to search for recipes
    def recipe_search(self, recipes_list, ingredient):
        data = recipes_list
        search_term = ingredient
        for recipe in data:
            if self.search_ingredients(search_term, recipe.ingredients):
                print(recipe)


# Create some Recipe instances

recipes_list = []

tea = Recipe("Tea")
tea.add_ingredients("Water", "Tea Leaves", "Sugar")
tea.set_cooking_time(5)
tea.get_difficulty()

recipes_list.append(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee powder", "Water", "Milk")
coffee.set_cooking_time(5)
coffee.get_difficulty()

recipes_list.append(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Flour", "Sugar", "Eggs", "Milk", "Butter", "Vanilla Essence")
cake.set_cooking_time(50)
cake.get_difficulty()

recipes_list.append(cake)

bannana_smoothie = Recipe("Bannana Smoothie")
bannana_smoothie.add_ingredients("Bananas", "Milk", "Sugar", "Ice")
bannana_smoothie.set_cooking_time(5)
bannana_smoothie.get_difficulty()

recipes_list.append(bannana_smoothie)

print("--------------------------")
print("Recipes List")
print("--------------------------")
for recipe in recipes_list:
    print(recipe)

print("--------------------------")
print("Results for recipe_search with Water: ")
print("--------------------------")
tea.recipe_search(recipes_list, "Water")

print("--------------------------")
print("Results for recipe_search with Sugar: ")
print("--------------------------")
tea.recipe_search(recipes_list, "Sugar")

print("--------------------------")
print("Results for recipe_search with Bananas: ")
print("--------------------------")
tea.recipe_search(recipes_list, "Bananas")

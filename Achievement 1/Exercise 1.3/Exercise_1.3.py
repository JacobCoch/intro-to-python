recipes_list = []
ingredients_list = []


def take_recipe():
    recipe_name = str(input("Enter the recipe: "))
    cooking_time = int(input("Enter the cooking time: "))
    ingredients = list(input("Enter the ingredients seperated by a comma.").split(","))
    recipe = {
        "recipe_name": recipe_name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }
    return recipe


n = int(input("How many recipes do you want to add? "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) <= 4:
        recipe["difficulty"] = "easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) > 4:
        recipe["difficulty"] = "medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "hard"

    print("========================")
    print("recipe:", recipe["recipe_name"])
    print("cooking_time(min): ", recipe["cooking_time"])
    print("ingredients: ", recipe["ingredients"])
    print("diffuculy: ", recipe["difficulty"])


def print_ingredients():
    ingredients_list.sort()

    print("========================")
    print("Ingredients available for all recipes")
    print("-----------------------")
    for ingredient in ingredients_list:
        print(ingredient)


print_ingredients()

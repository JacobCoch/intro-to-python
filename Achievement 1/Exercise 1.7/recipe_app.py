from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Integer, String, Column

# Create an engine object
engine = create_engine("mysql://cf-python:password@localhost/my_database")
# Create a connection object


# Base is a class from which all mapped classes should inherit
Base = declarative_base()


# Create a sessionmaker object that connects to the database
Session = sessionmaker(bind=engine)
session = Session()


class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + ", name: "
            + self.name
            + ", difficulty: "
            + self.difficulty
            + ">"
        )

    def __str__(self):
        return f"""
        Name: {self.name}
        Ingredients:
        {self.format_ingredients()}
        Cooking Time: {self.cooking_time} minutes
        {self.difficulty}
        """

    def format_ingredients(self):
        ingredients_list = self.ingredients.split(",")
        formatted_ingredients = "\n".join(
            [f"- {ingredient.strip()}" for ingredient in ingredients_list]
        )
        return formatted_ingredients


# This creates the table
Base.metadata.create_all(engine)


def calc_difficulty(cooking_time, ingredients):
    difficulty_levels = {
        "Easy": "Easy 😄",
        "Medium": "Medium 😅",
        "Intermediate": "Intermediate 😓",
        "Hard": "Hard 😰",
    }

    if (cooking_time < 10) and (len(ingredients) < 4):
        difficulty = "Easy"
    elif (cooking_time < 10) and (len(ingredients) >= 4):
        difficulty = "Medium"
    elif (cooking_time >= 10) and (len(ingredients) < 4):
        difficulty = "Intermediate"
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
        difficulty = "Hard"
    else:
        print("Something bad happened, please try again")

    return difficulty_levels.get(difficulty)


def return_ingredients_as_list():
    recipes_list = session.query(Recipe).all()
    for recipe in recipes_list:
        print("Recipe: ", recipe)
        print("recipe.ingredients: ", recipe.ingredients)
        recipe_ingredients_list = recipe.ingredients.split(", ")
        print(recipe_ingredients_list)


def create_recipe():
    ingredients = []
    name = str(input("Enter the name of the recipe: ").title().strip())
    while True:
        cooking_time = input("Enter the cooking time (minutes): ")
        if cooking_time.isnumeric():
            cooking_time = int(cooking_time)
            break
        else:
            print("Invalid input. Please try again.")

    while True:
        num_ingredients = input("Enter the number of ingredients: ")
        if num_ingredients.isnumeric():
            num_ingredients = int(num_ingredients)
            break
        else:
            print("Invalid input. Please try again.")

    for i in range(num_ingredients):
        ingredient = (
            input(f"Enter an ingredient ({i+1}/{num_ingredients}): ").title().strip()
        )
        ingredients.append(ingredient)
    recipe_ingredients = ", ".join(ingredients)
    difficulty = calc_difficulty(cooking_time, recipe_ingredients)

    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=recipe_ingredients,
        difficulty=difficulty,
    )
    print(recipe_entry)

    session.add(recipe_entry)
    session.commit()
    print("Recipe saved in the database.")


def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    else:
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []

        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredients_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredients_split)

        all_ingredients = list(dict.fromkeys(all_ingredients))

        all_ingredients_list = list(enumerate(all_ingredients))

        print("\nAll ingredients list:")
        print("------------------------")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0] + 1) + ". " + tup[1])

    try:
        ingredient_searched_nber = input(
            "\nEnter the number corresponding to the ingredient you want \nto select from the above list. You can enter several numbers. \nIn this case, numbers shall be separated by a space: "
        )

        ingredients_nber_list_searched = ingredient_searched_nber.split(" ")

        ingredient_searched_list = []
        for ingredient_searched_nber in ingredients_nber_list_searched:
            ingredient_searched_index = int(ingredient_searched_nber) - 1
            ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

            ingredient_searched_list.append(ingredient_searched.strip())

        print(
            "\nHere are the recipes for the following ingredient(s): ",
            ingredient_searched_list,
        )

        conditions = []
        for ingredient in ingredient_searched_list:
            like_term = "%" + ingredient + "%"
            condition = Recipe.ingredients.like(like_term)
            conditions.append(condition)

        searched_recipes = session.query(Recipe).filter(*conditions).all()

    except:
        print(
            "An unexpected error occurred. Make sure to select a number from the list."
        )

    else:
        for recipe in searched_recipes:
            print(recipe)


def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None
    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

        print("\nList of available recipes: ")
        for recipe in results:
            print("\nId: ", recipe[0])
            print("Name: ", recipe[1])

        recipe_id_for_edit = int(
            (input("\nEnter the id of the recipe you want to edit: "))
        )

        recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipes_id_list = []

        for recipe_tup in recipes_id_tup_list:
            recipes_id_list.append(recipe_tup[0])

        if recipe_id_for_edit not in recipes_id_list:
            print("Not in the ID list, please try again later.")
        else:
            print("Ok you can continue")

            recipe_to_edit = (
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).one()
            )

            print("\nWARNING: You are about to edit the following recipe: ")
            print(recipe_to_edit)

            print("\n1. Name")
            print("2. Cooking Time")
            print("3. Ingredients")
            column_for_update = int(
                input(
                    "\nPlease enter the corresponding number for what you want to update:"
                )
            )

            if column_for_update == 1:
                print("You want to update the name of the recipe")
                updated_value = input("\nEnter the new name for the recipe: ")
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.name: updated_value}
                )
                session.commit()

            elif column_for_update == 2:
                print("You want to change the cooking time of the recipe")
                updated_value = input("\nEnter the new cooking time for the recipe: ")
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.cooking_time: updated_value}
                )
                session.commit()

            elif column_for_update == 3:
                print("You have updated the ingredients of the recipe")

                # Collect the updated ingredients from the user
                updated_ingredients = []
                num_updated_ingredients = input("Enter the number of ingredients: ")

                if num_updated_ingredients.isnumeric():
                    num_updated_ingredients = int(num_updated_ingredients)
                else:
                    print("Invalid input. Please try again.")

                for i in range(num_updated_ingredients):
                    updated_ingredient = (
                        input(
                            f"Enter an ingredient ({i + 1}/{num_updated_ingredients}): "
                        )
                        .title()
                        .strip()
                    )
                    updated_ingredients.append(updated_ingredient)

                    # Convert the updated ingredients list to a comma-separated string
                updated_value = ", ".join(updated_ingredients)

                # Update the recipe in the database
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.ingredients: updated_value}
                )
                session.commit()

            else:
                print("Wrong input, please try again.")
            updated_difficulty = calc_difficulty(
                recipe_to_edit.cooking_time, recipe_to_edit.ingredients
            )
            print("updated_difficulty: ", updated_difficulty)
            recipe_to_edit.difficulty = updated_difficulty
            session.commit()
            print("Modification done.")


def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print("There are no recipes in the database.")
        return None
    else:
        print("\nAll recipes:")
        print("------------------------")

        for recipe in all_recipes:
            print(recipe)


def main_menu():
    while True:
        print("\nWelcome to the Recipe Database!")
        print("================================")
        print("\nMain Menu")
        print("================================")
        print("\nWhat would you like to do? Pick a choice!")
        print("1. Create a recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "5":
            view_all_recipes()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


main_menu()
session.close()

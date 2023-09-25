import mysql.connector

conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)"""
)


def create_recipe(conn, cursor):
    recipe_ingredients = []
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time (minutes): "))
    ingredients = input("Enter the ingredients: ")
    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe_ingredients.append(ingredients)
    recipe_ingredients_str = ", ".join(recipe_ingredients)

    sql = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, recipe_ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe saved in database.")


def calc_difficulty(cooking_time, ingredients):
    print("Run the calc_difficulty with: ", cooking_time, ingredients)

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

    print("Difficulty level: ", difficulty)
    return difficulty


def search_recipe(conn, cursor):
    return


def update_recipe(conn, cursor):
    return


def delete_recipe(conn, cursor):
    return


def view_all_recipes(conn, cursor):
    return


def main_menu(conn, cursor):
    choice = ""
    while choice != "6":
        print("\nWelcome to the Recipe Database!")
        print("================================")
        print("\nMain Menu")
        print("================================")
        print("\nWhat would you like to do? Pick a choice!")
        print("1. Create a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            view_all_recipes(conn, cursor)
        else:
            choice == "6"


main_menu(conn, cursor)
print("Goodbye!")

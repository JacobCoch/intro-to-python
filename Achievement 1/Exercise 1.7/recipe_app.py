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
        Recipe ID: {self.id}
        Name: {self.name}
        Ingredients:
        {self.format_ingredients()}
        Cooking Time: {self.cooking_time} minutes
        Difficulty: {self.difficulty}
        {self.display_difficulty_rating()}

        Enjoy your delicious meal!
        """

    def format_ingredients(self):
        ingredients_list = self.ingredients.split(",")
        formatted_ingredients = ""
        for ingredient in ingredients_list:
            formatted_ingredients += f"\t- {ingredient.strip()}\n"
        return formatted_ingredients

    def calc_difficulty(self, cooking_time, ingredients):
        print("Run the calc_difficulty with: ", cooking_time, ingredients)

        difficulty_levels = {
            "Easy": "😄 Easy Peasy!",
            "Medium": "😅 Not too shabby!",
            "Intermediate": "😓 A bit challenging!",
            "Hard": "😰 Master Chef territory!",
        }

        if cooking_time < 10:
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
        return f"Difficulty level: {difficulty_levels.get(self.difficulty, 'Unknown')}"


recipe_list = session.query(Recipe).all()
print(recipe_list)

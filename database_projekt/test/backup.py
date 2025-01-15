import sqlite3 as sql
import os

ANIMAL_PATH = "database_projekt\\animals.csv"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "zoo.db")

class zoo:
    def __init__(self, database_path:str, animals:str):
        #  variables
        self.DATABASE_PATH = database_path
        
        #functions
        def get_connection(database_path:str):
            return sql.connect(database_path)
        
        def init_animals(animals:str, database_cursor:sql.Cursor):
            #  formating data
            animal_table = []
            with open(animals, "r") as animal_data:
                for line in list(animal_data)[1:]:
                    line = line.split(";")
                    for a in range(len(line)):
                        line[a] = line[a].strip()
                    animal_table.append(line)
            print(animal_table)
            
            #  creating table
            database_cursor.execute(f"""CREATE TABLE IF NOT EXISTS animals(ChipNr INTEGER PRIMARY_KEY, Species TEXT, Age INTEGER, Name TEXT, Food TEXT, Cage_Nr INTEGER SECONDARY_KEY)""")
            #  inserting values
            for animal in animal_table:
                database_cursor.execute(f"""INSERT INTO animals VALUES({animal[0]}, "{animal[1]}", {animal[2]}, "{animal[3]}", "{animal[4]}", {animal[5]})""")
            
        DB_CONNECTION = get_connection(self.DATABASE_PATH)
        DB_CURSOR = DB_CONNECTION.cursor()
        init_animals(animals, DB_CURSOR)
        DB_CONNECTION.commit()
        
    def execute_command(cursor:sql.Cursor) -> list:
        cursor.execute("SELECT * FROM animals")
        return cursor.fetchall()
                    
        
                

def main():
    Zoo = zoo(DATABASE_PATH,ANIMAL_PATH)

if __name__ == "__main__":
    main()
import sqlite3, os

ANIMAL_PATH = "database_projekt\\animals.csv"

class zoo:
    def __init__(self, animals:str):
        def init_animals(animals:str):
            animal_table = []
            with open(animals, "r") as animal_data:
                for line in list(animal_data)[1:]:
                    line = line.split(";")
                    animal_table.append(line)
            print(animal_table)
        init_animals(animals)
                    
        
                

def main():
    Zoo = zoo(ANIMAL_PATH)

if __name__ == "__main__":
    main()
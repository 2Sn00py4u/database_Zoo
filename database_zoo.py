import sqlite3 as sql
import os

# TODO: Tierärzte hinzufügen

ANIMAL_PATH = "data\\tiere.csv"
WORKER_PATH = "data\\mitarbeiter.csv"
ENCLOSURE_PATH = "data\\gehege.csv"
EVENTS_PATH = "data\\events.csv"
ENCLOSURE_TO_WORKER_PATH = "data\\gehege_zu_mitarbeiter.csv"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "zoo.db")


class zoo:
    def __init__(self, database_path:str, animal_csv:str, worker_csv:str, enclosure_csv:str, event_csv:str, enclosure_to_worker_csv:str, create_tables:bool, insert_values:bool):
        #  variables
        self.DATABASE_PATH = database_path
        
        #functions
        def get_connection(database_path:str):
            return sql.connect(database_path)
        
        def init_table(data_file:str, database_cursor:sql.Cursor, table_name:str, *attributes:tuple):
            #  formating data
            data_table = []
            with open(data_file, "r") as data:
                for line in list(data)[1:]:
                    line = line.split(";")
                    for a in range(len(line)):
                        line[a] = line[a].strip()
                    data_table.append(line)
            
            #  creating table
            attribute_command = "("
            for i in range(len(attributes)-1):
                attribute_command += attributes[i] + ","
            attribute_command += attributes[len(attributes)-1] + ")"
            database_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}{attribute_command}""")
            #  inserting values
            if insert_values:
                for data_tuple in data_table:
                    insert_command = f"""INSERT INTO {table_name} VALUES("""
                    for i in range(len(data_tuple)-1):
                        if "TEXT" in attributes[i]:
                            insert_command += f'''"{data_tuple[i]}"''' + ","
                        else:
                            insert_command += data_tuple[i] + ","
                    insert_command += data_tuple[len(data_tuple)-1] + ")"
                    print(insert_command)
                    database_cursor.execute(insert_command)
            
        self.DB_CONNECTION = get_connection(self.DATABASE_PATH)
        self.DB_CURSOR = self.DB_CONNECTION.cursor()
        if create_tables:
            init_table(animal_csv, self.DB_CURSOR, "tiere", "ChipNr INTEGER PRIMARY_KEY", "Tierart TEXT", "'Alter' INTEGER", "Name TEXT", "Futter TEXT", "Gehege_Nr INTEGER")
            init_table(worker_csv, self.DB_CURSOR, "mitarbeiter", "ID INTEGER PRIMARY_KEY", "Vorname TEXT", "Name TEXT", "Job TEXT", "Gehalt INTEGER")
            init_table(enclosure_csv, self.DB_CURSOR, "gehege", "Nummer INTEGER PRIMARY_KEY", "Flaeche", "Biom TEXT", "Sicherheitslevel INTEGER")
            init_table(event_csv, self.DB_CURSOR, "events", "ID INTEGER PRIMARY_KEY","Name TEXT","Uhrzeit INTEGER","Dauer INTEGER","Gehege_Nr INTEGER","Mitarbeiter_ID INTEGER")
            init_table(enclosure_to_worker_csv, self.DB_CURSOR, "gehege_zu_mitarbeiter", "Gehege_Nr INTEGER","Mitarbeiter_ID INTEGER")
        self.DB_CONNECTION.commit()
        
    def execute_command(self, command:str) -> list:
        self.DB_CURSOR.execute(command)
        return self.DB_CURSOR.fetchall()
                    
        
                

def main():
    Zoo = zoo(DATABASE_PATH, ANIMAL_PATH, WORKER_PATH, ENCLOSURE_PATH, EVENTS_PATH, ENCLOSURE_TO_WORKER_PATH, False, False)
    return Zoo

def testing(Zoo: zoo):
    try:
        command = input(">>> ")
        if command == "exit":
           return False
        else:
            print(Zoo.execute_command(command))
            return True
    except Exception as e:
        print(e)
        return True

if __name__ == "__main__":
    Zoo = main()
    test = True
    while test:
        test = testing(Zoo)
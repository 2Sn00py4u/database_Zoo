import sqlite3 as sql
import os

ANIMAL_PATH = "data\\animals.csv"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "zoo.db")

class zoo:
    def __init__(self, database_path:str, animal_csv:str):
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
            #print(data_table)
            
            #  creating table
            attribute_command = "("
            for i in range(len(attributes)-1):
                attribute_command += attributes[i] + ","
            attribute_command += attributes[len(attributes)-1] + ")"
            database_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}{attribute_command}""")
            #  inserting values
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
        init_table(animal_csv, self.DB_CURSOR, "animals", "ChipNr INTEGER PRIMARY_KEY","Tierart TEXT","'Alter' INTEGER","Name TEXT","Futter TEXT","Gehege_Nr INTEGER")
        self.DB_CONNECTION.commit()
        
    def execute_command(self, command:str) -> list:
        self.DB_CURSOR.execute(command)
        return self.DB_CURSOR.fetchall()
                    
        
                

def main():
    Zoo = zoo(DATABASE_PATH,ANIMAL_PATH)
    print(Zoo.execute_command("SELECT * FROM animals"))
    print(Zoo.execute_command("""SELECT chipNr FROM animals WHERE 'Alter'=1"""))
    

if __name__ == "__main__":
    main()
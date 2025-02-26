import sqlite3 as sql
import os

#  global variables
ANIMAL_PATH = "zoo_data\\tiere.csv"
WORKER_PATH = "zoo_data\\mitarbeiter.csv"
ENCLOSURE_PATH = "zoo_data\\gehege.csv"
EVENTS_PATH = "zoo_data\\events.csv"
ENCLOSURE_TO_WORKER_PATH = "zoo_data\\gehege_zu_mitarbeiter.csv"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "zoo.db")


class zoo:
    def __init__(self, database_path:str, animal_csv:str, worker_csv:str, enclosure_csv:str, event_csv:str, enclosure_to_worker_csv:str):
        #  variables
        self.DATABASE_PATH = database_path
        
        #functions
        def get_connection(database_path:str):
            return sql.connect(database_path)
                
        def init_table(data_file:str, database_cursor:sql.Cursor, table_name:str, *attributes:tuple):
            try:
                #  formating data
                data_table = []
                with open(data_file, "r") as data:
                    for line in list(data)[1:]:
                        line = line.split(";")
                        for a in range(len(line)):
                            line[a] = line[a].strip()
                        data_table.append(line)
                    data.close()
                
                #  creating-table-command
                attribute_command = "("
                for i in range(len(attributes)-1):
                    attribute_command += attributes[i] + ","
                attribute_command += attributes[len(attributes)-1] + ")"
                database_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}{attribute_command}""")
                
                #  checking table wether to insert values or not
                database_cursor.execute(f"SELECT * FROM {table_name}")
                values = database_cursor.fetchall()
                if values != []:
                    insert_values = False
                elif values == []:
                    insert_values = True
                    
                #  inserting-values-command
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
            except Exception as e:
                print(e)
                
        self.DB_CONNECTION = get_connection(self.DATABASE_PATH)  #  get connection to db
        self.DB_CURSOR = self.DB_CONNECTION.cursor()  #  get cursor
        #  initialization of tables and values
        init_table(animal_csv, self.DB_CURSOR, "tiere", "ChipNr INTEGER PRIMARY_KEY", "Tierart TEXT", "'Alter' INTEGER", "Name TEXT", "Futter TEXT", "Gehege_Nr INTEGER")
        init_table(worker_csv, self.DB_CURSOR, "mitarbeiter", "ID INTEGER PRIMARY_KEY", "Vorname TEXT", "Name TEXT", "Job TEXT", "Gehalt INTEGER")
        init_table(enclosure_csv, self.DB_CURSOR, "gehege", "Nummer INTEGER PRIMARY_KEY", "Flaeche", "Biom TEXT", "Sicherheitslevel INTEGER")
        init_table(event_csv, self.DB_CURSOR, "events", "ID INTEGER PRIMARY_KEY","Name TEXT","Uhrzeit INTEGER","Dauer INTEGER","Gehege_Nr INTEGER","Mitarbeiter_ID INTEGER")
        init_table(enclosure_to_worker_csv, self.DB_CURSOR, "gehege_zu_mitarbeiter", "Gehege_Nr INTEGER","Mitarbeiter_ID INTEGER")
        self.DB_CONNECTION.commit()
        
    def execute_command(self, command:str) -> list:  #  execute a SQL-request and returns result
        try:
            self.DB_CURSOR.execute(command)
            return self.DB_CURSOR.fetchall()
        except Exception as e:
            print(e)
            
    def clear_table(self, table_name:str):  #  delete all values of a table
        try:
            return self.execute_command(f"DELETE FROM {table_name}")
        except Exception as e:
            print(e)

    def delete_table(self, table_name:str):  #  delete a table
        try:
            return self.execute_command(f"DROP TABLE {table_name}")
        except Exception as e:
            print(e)
            
    def list_tables(self):  #  returns a list of all tables
        try:
            return self.execute_command("SELECT name FROM sqlite_master WHERE type='table'")
        except Exception as e:
            print(e)
    
    def close_connection(self):  #  close connection to db
        self.DB_CONNECTION.close()         
        
                

def main(): #  creating a Zoo-instanz and returning it
    Zoo = zoo(DATABASE_PATH, ANIMAL_PATH, WORKER_PATH, ENCLOSURE_PATH, EVENTS_PATH, ENCLOSURE_TO_WORKER_PATH)
    return Zoo

def sqlite_shell(Zoo: zoo):  #  is a SQL-shell for interacting with the db
    try:
        command = input(">>> ")
        
        #  customcommands for interacting with the database via shell
        if command == ".exit":  #  close connection and exit the script 
            Zoo.close_connection()
            return False
        
        if command == ".ls":  #  lists all available tables in the db
            print(Zoo.list_tables())
            return True
        
        if command == ".restore":  #  restoring the whole database
            Zoo.close_connection()
            os.remove(DATABASE_PATH)
            Zoo = zoo(DATABASE_PATH, ANIMAL_PATH, WORKER_PATH, ENCLOSURE_PATH, EVENTS_PATH, ENCLOSURE_TO_WORKER_PATH)
            return Zoo

        if command.startswith(".del_table "):  #  delete a table
            Zoo.delete_table(command[10:])
            return True
        
        if command.startswith(".clear_table "):  # delete all values of a table
            Zoo.clear_table(command[12:])
            return True
        
        else:
            print(Zoo.execute_command(command))  #  execute SQL-command
            return True
        
    except Exception as e:
        print(e)
        return True

if __name__ == "__main__":
    try:
        Zoo = main()  #  passing the Zoo-instanz
        return_val = True
        while return_val:  #  processing shell until command '.exit'
            return_val = sqlite_shell(Zoo)
            if type(return_val) == zoo:  #  when getting a new instance (command '.restore') it should be updated
                Zoo = return_val
                return_val = True
                
    except KeyboardInterrupt:
        print("closing...")
def func(table_name, *attributes):
    attribute_command = "("
    for i in range(len(attributes)-1):
        attribute_command += attributes[i] + ", "
    attribute_command += attributes[len(attributes)-1] + ")"
    print(f"""CREATE TABLE IF NOT EXISTS {table_name}{attribute_command}""")
    #  inserting values
    
    
func("name", "Pc INTEGER PRIMARY", "Something TEXT")
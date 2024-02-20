import global_data

def write_to_db () : 
    with open("test.csv", 'w', encoding='utf-8') as db : 
        data_to_write = []
        for note in global_data.int_db_structure : 
            print(";".join(*note)+"\n")
        #    data_to_write.append(";".join(*note)+"\n")

        #print(data_to_write)
        # db.writelines(data_to_write)

write_to_db()

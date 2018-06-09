import pypyodbc

connection = pypyodbc.connect('Driver={ODBC Driver 11 for SQL Serve};'
                                'Server=windows;'
                                'Database=ootb_15_1_fp2;'
                                'uid=sa;pwd=admin')
connection.close()

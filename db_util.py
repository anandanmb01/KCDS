import sqlite3



class db():
    def __init__(self,url):
        try:

            # Connect to DB and create a cursor
            sqliteConnection = sqlite3.connect(url)
            cursor = sqliteConnection.cursor()
            print('DB init complete')
            self.cursor=cursor
            self.sqliteConnection=sqliteConnection

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred - ', error)
        
    def close(self):
        if self.sqliteConnection:
            self.cursor.close()
            self.sqliteConnection.commit()
            self.sqliteConnection.close()
            print('SQLite Connection closed')
        else:
            print("db connection closing error")
            
    def exec(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def insert_district(self,dis):
        res=self.cursor.execute(f'''select id from districts where districts.name=="{dis}"''').fetchall()
        if res==[]:
            self.cursor.execute(f"""
                                insert into districts (name)
                                values ('{dis}')
                                """)
            return self.cursor.execute(f'''select id from districts where districts.name=="{dis}"''').fetchall()
        else:
            return res
            
            
    def insert_localbodie(self,name,did):
        res=self.cursor.execute(f"""
                            select id from localbodies 
                            where name='{name}' and d_id ={int(did)}
                            """).fetchall()
        if res == []:
            self.cursor.execute(f"""
                                insert into localbodies (name,d_id)
                                values ('{name}',{int(did)})
                                """)
            res=self.cursor.execute(f"""
                            select id from localbodies 
                            where name='{name}' and d_id ={int(did)}
                            """).fetchall()
            return res
        else:
            return res
        
    def insert_ward(self,name,lid):
        res=self.cursor.execute(f"""
                            select id from wards 
                            where name='{name}' and l_id ={int(lid)}
                            """).fetchall()
        if res == []:
            self.cursor.execute(f"""
                                insert into wards (name,l_id)
                                values ('{name}',{int(lid)})
                                """)
            res=self.cursor.execute(f"""
                            select id from wards 
                            where name='{name}' and l_id ={int(lid)}
                            """).fetchall()
            return res
        else:
            return res
        
    def insert_polling_station(self,name,wid):
        res=self.cursor.execute(f"""
                            select id from polling_stations 
                            where name='{name}' and w_id ={int(wid)}
                            """).fetchall()
        if res == []:
            self.cursor.execute(f"""
                                insert into polling_stations (name,w_id)
                                values ('{name}',{int(wid)})
                                """)
            res=self.cursor.execute(f"""
                            select id from polling_stations 
                            where name='{name}' and w_id ={int(wid)}
                            """).fetchall()
            return res
        else:
            return res
        
    def insert_citizen(self,name,guardian,house_no,house_name,gender,age,id_card_no,pid):
        self.cursor.execute(f"""
                            insert into citizens (name,guardian,house_no,house_name,gender,age,id_card_no,p_id)
                            values ('{name}','{guardian}',{house_no},'{house_name}','{gender}',{int(age)},'{id_card_no}',{int(pid)})
                            """)


        
        
# import sqlite3
# sqliteConnection = sqlite3.connect("db.sqlite")
# cursor = sqliteConnection.cursor()
# def exec(cmd):
#     cursor.execute(cmd)
#     return cursor.fetchall()

# select id from localbodies where name='ptpm' and d_id ='1'
# insert into localbodies (name,d_id) values ('ptpm','1')
import sqlite3
import os

class db():
    
    def __init__(self,url):
        
        self.url=url

        file_name = self.url
        directory = "./"

        for root, dirs, files in os.walk(directory):
            if file_name in files:
                os.remove("./"+self.url)
                break
            else:
                pass
            
        self.conn=sqlite3.connect("./"+self.url, check_same_thread=False)  
    
    def initilize(self):
        # Create 'districts' table
        self.conn.execute("""
            CREATE TABLE districts (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(30)
            )
        """)

        # Create 'localbodies' table
        self.conn.execute("""
            CREATE TABLE localbodies (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(30), 
                d_id INTEGER, 
                FOREIGN KEY(d_id) REFERENCES districts(id)
            )
        """)

        # Create 'wards' table
        self.conn.execute("""
            CREATE TABLE wards (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(30), 
                l_id INTEGER, 
                FOREIGN KEY(l_id) REFERENCES localbodies(id)
            )
        """)

        # Create 'polling_stations' table
        self.conn.execute("""
            CREATE TABLE polling_stations (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(30), 
                w_id INTEGER, 
                FOREIGN KEY(w_id) REFERENCES wards(id)
            )
        """)

        # Create 'citizens' table
        self.conn.execute("""
            CREATE TABLE citizens (
                id INTEGER PRIMARY KEY, 
                p_id INTEGER, 
                name VARCHAR(30), 
                guardian VARCHAR(30), 
                house_no VARCHAR(30), 
                house_name VARCHAR(30), 
                gender VARCHAR(30), 
                age VARCHAR(30), 
                id_card_no VARCHAR(30), 
                FOREIGN KEY(p_id) REFERENCES polling_stations(id)
            )
        """)

    
    def insert_district(self,dis):
        res=self.cursor.execute(f'''select id from districts where districts.name=="{dis}"''').fetchall()
        if res==[]:
            self.conn.execute(f"""
                                insert into districts (name)
                                values ('{dis}')
                                """)
            return self.conn.execute(f'''select id from districts where districts.name=="{dis}"''').fetchall()
        else:
            return res
            
            
    def insert_localbodie(self,name,did):
        res=self.cursor.execute(f"""
                            select id from localbodies 
                            where name=? and d_id =?
                            """,(name,int(did))).fetchall()
        if res == []:
            self.cursor.execute(f"""
                                insert into localbodies (name,d_id)
                                values (?,?)
                                """,(name,int(did)))
            res=self.cursor.execute(f"""
                            select id from localbodies 
                            where name=? and d_id =?
                            """,(name,int(did))).fetchall()
            return res
        else:
            return res
        
    def insert_ward(self,name,lid):
        res=self.cursor.execute(f"""
                            select id from wards 
                            where name=? and l_id =?
                            """,(name,int(lid))).fetchall()
        if res == []:
            self.cursor.execute(f"""
                                insert into wards (name,l_id)
                                values (?,?)
                                """,(name,int(lid)))
            res=self.cursor.execute(f"""
                            select id from wards 
                            where name=? and l_id =?
                            """,(name,int(lid))).fetchall()
            return res
        else:
            return res
        
    def insert_polling_station(self,name,wid):
        res=self.cursor.execute("""
                            select id from polling_stations 
                            where name=? and w_id =?
                            """,(name,int(wid))).fetchall()
        if res == []:
            self.cursor.execute("insert into polling_stations (name,w_id) values (?,?)",(name,wid))
            res=self.cursor.execute(f"""
                            select id from polling_stations 
                            where name=? and w_id =?
                            """,(name,int(wid))).fetchall()
            return res
        else:
            return res
        
    def insert_citizen(self,name,guardian,house_no,house_name,gender,age,id_card_no,pid):
        # use a parameterized SQL query with placeholders
        sql = "INSERT INTO citizens (name, guardian, house_no, house_name, gender, age, id_card_no, p_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # print(sql)
        # execute the SQL command with the values as parameters
        self.cursor.execute(sql, (name, guardian, house_no, house_name, gender, age, id_card_no, pid))


    def close(self):
        self.conn.commit()
        self.conn.close()
        
def getText(element):
    return element.split('-')[-1].strip()

handler=open("people.csv","w")
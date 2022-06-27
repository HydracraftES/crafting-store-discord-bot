import json, mysql.connector, hashlib, random, datetime

class ExtraFunctions:
    
    def __mysql_connection(self, user, password, database, host):
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        
        return connection
    
    def check_permissions(self, permissions, rol_ids, user_id):
        self.permissions = permissions
        self.rol_ids = rol_ids
        self.user_id = user_id
        
        # Importing config file.
        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)
        
        whitelist_roles = config["rol_id"][self.permissions]
        admin_permissions = config["admin_permissions"]
        
        has_rol = False
        
        for rol in self.rol_ids:
            if(rol.id in whitelist_roles or self.user_id in admin_permissions):
                has_rol = True
                break
        
        return has_rol
    
    def save_gift_card(self, username, gift_id, gift_code, amount):
        
        self.username = username
        self.gift_id = gift_id
        self.gift_code = gift_code
        self.amount = amount
        user_id = self.username.id
        date = datetime.datetime.now()
        
        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)
        
        
        conn = self.__mysql_connection(
            user=config["db_config"]["bot"]["user"], 
            password=config["db_config"]["bot"]["password"], 
            database=config["db_config"]["bot"]["database"], 
            host=config["db_config"]["bot"]["host"]
        )
        
        cur = conn.cursor()
        
        cur.execute("INSERT INTO giftcards (gift_id, user_id, amount, date, giftcard) VALUES (%s, %s, %s, %s, %s)", (self.gift_id, user_id, self.amount, date, self.gift_code))
        conn.commit()
        conn.close()
        
        return {
            "status": True
        }

    def search_gift_card(self, user_id):

        self.user_id = user_id
        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)
            
        conn = self.__mysql_connection(
            user=config["db_config"]["bot"]["user"], 
            password=config["db_config"]["bot"]["password"], 
            database=config["db_config"]["bot"]["database"], 
            host=config["db_config"]["bot"]["host"]
        )
        
        query = conn.cursor()
        query.execute("SELECT * FROM giftcards WHERE user_id = %s", (self.user_id, ))
        
        res = query.fetchall()
        conn.close()
        
        if(len(res) > 0):
            return {
                "status": True,
                "response": res
            }
        else: 
            return {
                "status": False,
                "message": config["language"]["error_messages"]["user_no_giftcards"]
            }
    
    def get_gift_card_by_id(self, id):
        
        self.id = id
        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)
            
        conn = self.__mysql_connection(
            user=config["db_config"]["bot"]["user"], 
            password=config["db_config"]["bot"]["password"], 
            database=config["db_config"]["bot"]["database"], 
            host=config["db_config"]["bot"]["host"]
        )
        
        query = conn.cursor()
        query.execute("SELECT * FROM giftcards WHERE id = %s", (self.id, ))
        
        res = query.fetchone()
        conn.close()
        
        return {
            "status": True,
            "response": {
                "user_id": res[2],
                "gift_code": res[5],
                "date": res[4],
                "amount": res[3]
            }
        }

    def save_log(self, username, user_id, command):
        
        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)
        
        self.username = username
        self.user_id = user_id
        self.command = command
        self.bot_name = "Hydracraft Compras"
        date = datetime.datetime.now()
        
        conn = self.__mysql_connection(
            user=config["db_config"]["bot"]["user"], 
            password=config["db_config"]["bot"]["password"], 
            database=config["db_config"]["bot"]["database"], 
            host=config["db_config"]["bot"]["host"]
        )

        query = conn.cursor()
        query.execute("INSERT INTO logs (user, user_id, command, date, bot) VALUES (%s, %s, %s, %s, %s)", (str(self.username), self.user_id, self.command, date, self.bot_name))
        
        conn.commit()
        conn.close()
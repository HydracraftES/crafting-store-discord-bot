import json, sqlite3, hashlib, random, datetime

class ExtraFunctions:
    
    def __sqlite_connection(self):
        
        '''
            This is a private method which will return the local connection throught the database
        '''
        conn = sqlite3.connect("./database.db")
        
        return conn
    
    def check_permissions(self, permissions, rol_ids, user_id):
        
        '''
            This method will check if an user has the admin permissions or it has some of the needed roles.
        '''
        
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
    
    def save_gift_card(self, user, gift_id, gift_code, amount):
        
        '''
            This method will save the giftcards in the database.
        '''
                
        self.user = user
        self.gift_id = gift_id
        self.gift_code = gift_code
        self.amount = amount
        
        rand_tk = str(random.randint(6500, 100300)) + "" + self.user
        private_token = hashlib.sha1(rand_tk.encode()).hexdigest()
        
        conn = self.__sqlite_connection()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO gift_cards (gift_id, gift_code, user, private_token, amount) VALUES (?, ?, ?, ?, ?)", (self.gift_id, self.gift_code, self.user, private_token, self.amount))
        conn.commit()
        conn.close()
        
        return {
            "status": True,
            "response": private_token
        }
    
    def search_gift_card(self, private_token = None, user = None):
        
        '''
            This method will search at the database if there's the needed private token, or if it's searched by the username, it will return all the giftcards of the user.
        '''

        with open('./config.json', encoding="utf-8") as c:
            config = json.load(c)

        self.private_token = private_token
        self.user = user

        conn = self.__sqlite_connection()
        cur = conn.cursor()

        if(self.private_token == None and self.user == None):
            return {
                "status": False
            }
        elif(self.private_token != None and self.user != None):
            cur.execute("SELECT * FROM gift_cards WHERE private_token = ? AND user = ?" , (self.private_token, self.user))
            
            rows = cur.fetchone()
            conn.close()
            
            if(rows == None):
                return {
                    "status": False,
                    "message": config["language"]["error_messages"]["user_no_giftcards"]
                }
            else:
                return {
                    "status": True,
                    "response": {
                        "id": rows[0],
                        "gift_id": rows[1],
                        "gift_code": rows[2],
                        "user": rows[3],
                        "private_token": rows[4],
                        "amount": rows[5]
                    }
                }
            
        elif(self.private_token == None and self.user != None):
            
            # This one will return all giftcards available at the database.
            cur.execute("SELECT * FROM gift_cards WHERE user = ?" , (self.user,))
            
            rows = cur.fetchall()
            conn.close()
            
            if(rows == None):
                return {
                    "status": False,
                    "message": config["language"]["error_messages"]["user_no_giftcards"]
                }
            else:
                return {
                    "status": True,
                    "response": rows
                }
            
        elif(self.private_token != None and self.user == None):
            cur.execute("SELECT * FROM gift_cards WHERE private_token = ?" , (self.private_token,))

            rows = cur.fetchone()
            conn.close()
            
            if(rows == None):
                return {
                    "status": False,
                    "message": config["language"]["error_messages"]["user_no_giftcards"]
                }
            else:
                return {
                    "status": True,
                    "response": {
                        "id": rows[0],
                        "gift_id": rows[1],
                        "gift_code": rows[2],
                        "user": rows[3],
                        "private_token": rows[4],
                        "amount": rows[5]
                    }
                }

    def save_log(self, user, user_id, command):
        
        '''
            This method will save logs whenever a command is used by a staff.
        '''
        
        self.user = user
        self.user_id = user_id
        self.command = command
        date = datetime.datetime.now()
        
        conn = self.__sqlite_connection()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO logs (user, user_id, command, date) VALUES (?, ?, ?, ?)", (str(self.user), self.user_id, self.command, date))
        
        conn.commit()
        conn.close()
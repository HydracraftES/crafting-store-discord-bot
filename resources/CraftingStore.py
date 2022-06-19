import requests, json
from resources.ExtraFunctions import ExtraFunctions

class CraftingStore:
    
    # Constructor
    def __init__(self):
       
        # Importing config file
        with open("./config.json", encoding="utf-8") as c:
            config = json.load(c)

        # Setting values from the config file
        self.token = config["api_token"]
        self.url = config["url"]
        
        # Setting error messages
        self.error_message = config["language"]["api_messages"]["error_messages"]
        
    def  __check_api_status(self):
        
        '''
        
            This method will check if the API is working, if not, it will return an error message.
        
        '''
        
        r = requests.get(self.url + '/payments', headers={"token": self.token})

        r = json.loads(r.text)
        
        # Success will be "True" or "False" in their API.
        if(r["success"]):
            return r
        else:
            return False
        
    def get_bought_items(self, user):
        
        '''

            This method will return an array with all bought items.
            
        '''
        self.user = user
        
        r = CraftingStore().__check_api_status()
        
        if(r):
            
            list = requests.get(self.url + "/payments?player="+self.user, headers={"token": self.token})
            list = json.loads(list.text)
            
            if(len(list['data']) <= 0):
                return {
                    "status": "error",
                    "message": self.error_message["user_err"]
                }
            else:
                if(list['meta']['lastPage'] == 1):
                    return {
                        "status": "success",
                        "response": list["data"]
                    }
                else:
                    last_page = list["meta"]["lastPage"]
                    new_list = []
                    for i in range(1, last_page + 1):
                        p_lists = requests.get(self.url + '/payments?player='+self.user+'&page='+str(i), headers={"token": self.token})
                        p_lists = json.loads(p_lists.text)
                        for lists in p_lists["data"]:
                            new_list.append(lists)
                        
                    return {
                        "status": "success",
                        "response": new_list
                    }
        else:
            return {
                "status": "error",
                "message": self.error_message["connection_err"]
            }            
    
    def search_transaction(self, user, transaction_id):
        
        '''
        
            This method will itinerant every single page looking for the transaction id, if it match, it will return the list of information about the bought item.
            
        '''
        
        self.user = user
        self.transaction_id = transaction_id
        
        r = CraftingStore().__check_api_status()

        if(r):
            
            for i in r:
                b = requests.get(self.url + "/payments?player="+self.user+"&page="+str(i), headers={"token": self.token})
                b = json.loads(b.text)
                
                if(len(b["data"]) <=0):
                    return {
                        "status": "error",
                        "message": self.error_message["user_err"]
                    }
                else:
                    last_page = b["meta"]["lastPage"]

                    p = None

                    for i in range(1, last_page + 1):
                        for a in b["data"]:
                            if(a["transactionId"] == self.transaction_id):
                                p = a
                                break


                    if(p == None):
                        return {
                            "status": "error",
                            "message": self.error_message["transaction_err"]
                        }
                    else:
                        return {
                            "status": "success",
                            "response": p
                        }
        else:
            return {
                "status": "error",
                "message": self.error_message["connection_err"]
            }
    
    def create_gift_card(self, user, amount):
        
        '''
            This method will create a giftcard and saving it with a private token on a local database (sqlite3)
        '''
        
        self.user = user
        self.amount = amount
        
        r = CraftingStore().__check_api_status()
        
        if(r):
            b = requests.post(self.url + '/gift-cards', json={"amount": int(self.amount), "applyTo": 0}, headers={"token": self.token})
            b = json.loads(b.text)
            
            if(b["success"]):
                gift_id = b["data"]["id"]
                gift_code = b["data"]["code"]
                gift_amount = b["data"]["amount"]

                extra_fnc = ExtraFunctions()
                
                saved = extra_fnc.save_gift_card(user=self.user, gift_id=gift_id, gift_code=gift_code, amount=self.amount)
                
                if(saved["status"]):
                    return {
                        "status": "success",
                        "response": {
                            "gift_code": gift_code,
                            "amount": gift_amount,
                            "token": saved["response"]
                        }
                    }
                
            else:
                return {
                    "status": "error",
                    "message": self.error_message["exception_err"]
                }
        else:
            return {
                "status": "error",
                "message": self.error_message["connection_err"]
            }        

            
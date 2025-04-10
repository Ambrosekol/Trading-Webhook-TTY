from .Webhook_status import Webhook_Status
import audiohandler
import time

class Trader:
    db : dict[list[Webhook_Status]] = {}
    db_keys : list = []
    
    def __init__(self):
        pass
    
    
    def short_Term_Sync_Trigger(self, minutes_to_wait):
        tf_0  = self.get_wh_status(self.db.get(self.db_keys[0]))
        
        time.sleep(minutes_to_wait * 60) # convert mins to sec & wait
        
        tf_1 = self.get_wh_status(self.db.get(self.db_keys[1]))
        tf_2 = self.get_wh_status(self.db.get(self.db_keys[2]))
        
        if (tf_0.get('status') == tf_1.get('status')) and (tf_1.get('status') == tf_2.get('status')): # check if all three are same color
            if tf_1.get('status') == self.get_wh_status(self.db.get(self.db_keys[0])).get("status"): # check one more time against the lowest tf
                audiohandler.speak("HELLO THERE I AM the short Term Sync Trigger")
            
        
    def get_wh_status(self, webhook_db:list[Webhook_Status], start_location = 0): # This reads from the end of the list
        try:
            if start_location == 0:
                return webhook_db[len(webhook_db) - 1].__dict__ # return latest webhook obj if no args given
            start_index = len(webhook_db) - start_location # Ensures all indexes are positive
            webhook : Webhook_Status = webhook_db[abs(start_index)]
            return webhook.__dict__ # returns indexed webhook 
        except:
            return {}
    

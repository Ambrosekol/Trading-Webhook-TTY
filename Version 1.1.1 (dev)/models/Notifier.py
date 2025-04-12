from .webhook_status import Webhook_Status
import audiohandler
import time

class StatusNotifier:
    
    init_keys = None # Not used anywhere in code. created for future init settings
    webhooks_1_db: list[Webhook_Status] = []
    webhooks_2_db: list[Webhook_Status] = []
    webhooks_3_db: list[Webhook_Status] = []
    
    def __init__(self, **kwargs):
        if self.init_keys is None:
            self.init_keys = kwargs

    
    def save_webhook_data(self, **kwargs):
        webhook_name = kwargs.get("webhook_name")
        status = kwargs.get("status")
        other_info:dict = kwargs.get("other_info")
        #self.check_prev_webhook_status()
        if webhook_name == "webhook_one":
            self.webhooks_1_db.append(Webhook_Status(webhook_name, status, other_info))
        elif webhook_name == "webhook_two":
            self.webhooks_2_db.append(Webhook_Status(webhook_name, status, other_info))
        else:
            self.webhooks_3_db.append(Webhook_Status(webhook_name, status, other_info))
        
        
    def get_wh_status(self, webhook_db:list[Webhook_Status], start_location = 0): # This reads from the end of the list
        try:
            if start_location == 0:
                return webhook_db[len(webhook_db) - 1].__dict__ # return latest webhook obj if no args given
            start_index = len(webhook_db) - start_location # Ensures all indexes are positive
            webhook : Webhook_Status = webhook_db[abs(start_index)]
            return webhook.__dict__ # returns indexed webhook 
        except:
            return Webhook_Status.__dict__
    
    
    def check_validity(self):
        latest_wh_one_entry = self.get_wh_status(self.webhooks_1_db) #checks the most recent wh
        latest_wh_two_entry = self.get_wh_status(self.webhooks_2_db)
        latest_wh_three_entry = self.get_wh_status(self.webhooks_3_db)
        
        self.log(latest_wh_three_entry, latest_wh_two_entry, latest_wh_one_entry)

        if (latest_wh_one_entry.get('status') == 'Green') and (latest_wh_three_entry.get("status") == 'Green') and (latest_wh_two_entry.get('status') == 'Green'):
            self.talk('The three are green') # THIS IS WHAT IT SAYS IF THE 3 WEBHOOKS ARE GREEN
        elif (latest_wh_three_entry.get("status") == 'Green') and (latest_wh_two_entry.get('status') == 'Green'):
            self.talk('1 and 2 are Green') # THIS IS WHAT IT SAYS IF THE 2 WEBHOOKS ARE GREEN
        else:
            pass
        
        if (latest_wh_one_entry.get('status') == 'Red') and (latest_wh_three_entry.get("status") == 'Red') and (latest_wh_two_entry.get('status') == 'Red'):
            self.talk('he three are red') # THIS IS WHAT IT SAYS IF THE 3 WEBHOOKS ARE Red
        elif (latest_wh_three_entry.get("status") == 'Red') and (latest_wh_two_entry.get('status') == 'Red'):
            self.talk('1 and 2 are Red') # THIS IS WHAT IT SAYS IF THE 2 WEBHOOKS ARE Red
        else:
            pass
    
    def talk(self, sentence):
        audiohandler.speak(sentence)
    
    def execute_process(self):
        tf = self.init_keys.get('timeframes') # List of trading timeframes
        sec_to_wait = float(tf[0]) * 60 # convert lowest timeframe to time in secs
        
        audiohandler.threading.Thread(target=self.startProcess, args=(sec_to_wait,)).start()


    def startProcess(self, wait_time):
        time.sleep(wait_time)
        self.check_validity()
    
    def log(self, high:dict, mid:dict, low:dict):
        print("[Current DataBase Status ==>  H: {}, M: {}, L: {}]"
              .format(high.get('status'), mid.get('status'), low.get('status')))
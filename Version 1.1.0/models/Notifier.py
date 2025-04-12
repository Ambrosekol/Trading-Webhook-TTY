import requests
from .webhook_status import Webhook_Status
import audiohandler


class StatusNotifier:
    listening_url = "https://webhook.site/0e47862a-e384-45c7-9454-a733304b824f"
    
    three_green = "Green THREE" # THIS IS WHAT IT SAYS IF THE THREE WEBHOOKS ARE GREEN
    three_red = 'Red THREE' # THIS IS WHAT IT SAYS IF THE THREE WEBHOOKS ARE RED
    two_green = 'Green' # THIS IS WHAT IT SAYS IF THE TWO  WEBHOOK Mid & High ARE GREEN
    two_red = 'Red' # THIS IS WHAT IT SAYS IF THE TWO WEBHOOK Mid & High ARE RED
    
    
    init_keys = None # Not used anywhere in code. created for future init settings
    
    webhooks_1_db: list[Webhook_Status] = []
    webhooks_2_db: list[Webhook_Status] = []
    webhooks_3_db: list[Webhook_Status] = []
    
    def __init__(self, **kwargs):
        if self.init_keys is None:
            self.init_keys = kwargs.keys()
    
    def save_webhook_data(self, **kwargs):
        webhook_name = kwargs.get("webhook_name")
        status = kwargs.get("status")
        other_info:dict = kwargs.get("other_info")
        time_in = kwargs.get("received_when")
        
        #self.check_prev_webhook_status()
        if webhook_name == "low timeframe":
            self.webhooks_1_db.append(Webhook_Status(webhook_name, status, time_in, other_info))
            self.logger(webhook_name, self.webhooks_1_db[-1])
            
        elif webhook_name == "midimum timeframe":
            self.webhooks_2_db.append(Webhook_Status(webhook_name, status, time_in, other_info))
            self.logger(webhook_name, self.webhooks_2_db[-1])
            
        else:
            self.webhooks_3_db.append(Webhook_Status(webhook_name, status, time_in, other_info))
            self.logger(webhook_name, self.webhooks_3_db[-1])
        
        
    def get_wh_status(self, webhook_db:list[Webhook_Status], start_location = 0):
        try:
            if start_location == 0:
                return webhook_db[len(webhook_db) - 1].to_dict() # return latest webhook obj if no args given
            start_index = len(webhook_db) - start_location # Ensures all indexes are positive
            webhook : Webhook_Status = webhook_db[abs(start_index)]
            return webhook.to_dict() # returns indexed webhook 
        except:
            return Webhook_Status.__dict__
    
    
    def check_validity(self):
        latest_wh_one_entry = self.get_wh_status(self.webhooks_1_db) #checks the most recent wh
        latest_wh_two_entry = self.get_wh_status(self.webhooks_2_db)
        latest_wh_three_entry = self.get_wh_status(self.webhooks_3_db)
            
        if (latest_wh_one_entry.get('status') == 'Green') and (latest_wh_three_entry.get("status") == 'Green') and (latest_wh_two_entry.get('status') == 'Green'):
            self.talk(self.three_green)
            requests.post(self.listening_url, json={
                "Message" : self.three_green,
                "data" : [latest_wh_one_entry, latest_wh_two_entry, latest_wh_three_entry]
                }) # Send webhook alert
            
        elif (latest_wh_three_entry.get("status") == 'Green') and (latest_wh_two_entry.get('status') == 'Green'):
            self.talk(self.two_green)
            requests.post(self.listening_url, json={
                "Message" : self.two_green,
                "data" : [latest_wh_two_entry, latest_wh_three_entry]
                }) # Send webhook alert
            
        else:
            pass
        
        if (latest_wh_one_entry.get('status') == 'Red') and (latest_wh_three_entry.get("status") == 'Red') and (latest_wh_two_entry.get('status') == 'Red'):
            self.talk(self.three_red)
            requests.post(self.listening_url, json={
                "Message" : self.three_red,
                "data" : [latest_wh_one_entry, latest_wh_two_entry, latest_wh_three_entry]
                }) # Send webhook alert
            
        elif (latest_wh_three_entry.get("status") == 'Red') and (latest_wh_two_entry.get('status') == 'Red'):
            self.talk(self.two_red) # THIS IS WHAT IT SAYS IF THE 2 WEBHOOKS ARE Red
            requests.post(self.listening_url, json={
                "Message" : self.three_green,
                "data" : [latest_wh_two_entry, latest_wh_three_entry]
                }) # Send webhook alert
            
        else:
            pass
    
    def talk(self, sentence):
        audiohandler.speak(sentence)
        
    
    def logger(self, webhook, obj : Webhook_Status):
        print(
            "====> Webhook : {} || Status: {} || Time Registered: {} || Other Info : {} <====".format(
                webhook,
                obj.status,
                obj.time_registered.time(),
                obj.other_info)
        )


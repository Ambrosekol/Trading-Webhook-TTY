import requests
from .webhook_status import Webhook_Status
import audiohandler
from datetime import datetime


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
            
        elif webhook_name == "midimum timeframe":
            self.webhooks_2_db.append(Webhook_Status(webhook_name, status, time_in, other_info))
            
        else:
            self.webhooks_3_db.append(Webhook_Status(webhook_name, status, time_in, other_info))

        
        
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
                
        wh = [self.get_wh_status(self.webhooks_1_db), self.get_wh_status(self.webhooks_2_db), self.get_wh_status(self.webhooks_3_db)]
        
        if (wh[0].get('status') == 'Green') and (wh[2].get("status") == 'Green') and (wh[1].get('status') == 'Green'):
            
            self.talk(self.three_green)
            
            print("===================================================================================")
            for _ in range(3):
                self.logger(wh[_].get("name"), wh[_])
            print("===================================================================================")
            
            requests.post(self.listening_url, json={
                "Message" : self.three_green,
                "Time Notified" : str(datetime.now().time()),
                "data" : [wh[0], wh[1], wh[2]]
                }) # Send webhook alert
            
        elif (wh[2].get("status") == 'Green') and (wh[1].get('status') == 'Green'):
            
            self.talk(self.two_green)
            
            print("===================================================================================")
            for _ in range(1, 3):
                self.logger(wh[_].get("name"), wh[_])
            print("===================================================================================")
            
            requests.post(self.listening_url, json={
                "Message" : self.two_green,
                "Time Notified" : str(datetime.now().time()),
                "data" : [wh[1], wh[2]]
                }) # Send webhook alert
            
        else:
            pass
        
        if (wh[0].get('status') == 'Red') and (wh[2].get("status") == 'Red') and (wh[1].get('status') == 'Red'):
            
            self.talk(self.three_red)
            
            print("===================================================================================")
            for _ in range(3):
                self.logger(wh[_].get("name"), wh[_])
            print("===================================================================================")
            
            requests.post(self.listening_url, json={
                "Message" : self.three_red,
                "Time Notified" : str(datetime.now().time()),
                "data" : [wh[0], wh[1], wh[2]]
                }) # Send webhook alert
            
        elif (wh[2].get("status") == 'Red') and (wh[1].get('status') == 'Red'):
            
            self.talk(self.two_red) # THIS IS WHAT IT SAYS IF THE 2 WEBHOOKS ARE Red
            
            print("===================================================================================")
            for _ in range(1, 3):
                self.logger(wh[_].get("name"), wh[_])
            print("===================================================================================")
            
            requests.post(self.listening_url, json={
                "Message" : self.three_green,
                "Time Notified" : str(datetime.now().time()),
                "data" : [wh[1], wh[2]]
                }) # Send webhook alert
            
        else:
            pass
    
    def talk(self, sentence):
        audiohandler.speak(sentence)
        
    
    def logger(self, webhook, obj : dict):
        print(
            "====> Webhook : {} || Status: {} || Time Registered: {} || Other Info : {} <====".format(
                webhook,
                obj.get("status"),
                obj.get("time_registered"),
                obj.get("other_info"))
        )


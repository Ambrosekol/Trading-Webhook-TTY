from datetime import datetime

class Webhook_Status():
    def __init__(self, name, status, time_registered : datetime, other_info):
        self.name = name
        self.status = status
        self.time_registered = time_registered
        self.other_info = other_info
    
    def to_dict(self):
        return {
            "name" : self.name,
            "status" : self.status,
            "time_registered" : str(self.time_registered.time()),
            "other_info" : self.other_info
        }
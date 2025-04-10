from datetime import datetime

class Webhook_Status():
    def __init__(self, status, time_registered : datetime, other_info):
        self.status = status
        self.time_registered = time_registered
        self.other_info = other_info
from .Trader import Trader, Webhook_Status, audiohandler

class StatusNotifier:
    
    init_keys = None 
    trader = Trader()
    
    def __init__(self, **kwargs):
        if self.init_keys is None:
            self.init_keys = kwargs

        if self.init_keys.get("timeframes") is not None:
            tf_len = len(self.init_keys.get("timeframes"))
            
            for index in range(tf_len): # itrate through the list of timeframes
                self.trader.db[self.init_keys.get("timeframes")[index]] = [] # init the db
                
            self.trader.db_keys = self.init_keys.get("timeframes")


    def save_webhook_data(self, **kwargs):
        db_to_save_data = kwargs.get("db")
        status = kwargs.get("status")
        other_info:dict = kwargs.get("other_info")
        time_in = kwargs.get("received_when")
        
        if self.trader.db.get(db_to_save_data) is not None:
            self.trader.db[db_to_save_data].append(Webhook_Status(status, time_in, other_info))
            self.logger(db_to_save_data, self.trader.db[db_to_save_data][-1])

    
    def execute_process(self, caller = 0):        
        audiohandler.threading.Thread(target=self.trade_cases, args=(caller,)).start()


    def trade_cases(self , caller):
        if caller == 1:
            audiohandler.threading.Thread(target = self.trader.short_Term_Sync_Trigger, args=(6,)).start() # Pass the lower tf database
            
        
    
    def logger(self, timeframe, obj : Webhook_Status):
        print(
            "====> TimeFrame : {} || Status: {} || Time Registered: {} || Other Info : {} <====".format(
                timeframe,
                obj.status,
                obj.time_registered.time(),
                obj.other_info)
        )
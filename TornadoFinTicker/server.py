# -*- coding: utf-8 -*-

from tornado import websocket, web, httpserver
import tornado.ioloop as ioloop
import datetime, itertools, json

######### CONSTANTS ######################
TICK = itertools.count(2)
CONNECTIONSLIST = set()
priceDF = None
PLOTRANGE = 100
FREQ = 1
PORT = 8765

######### HELPER FUNCTIONS ###############

# Helper function to generate data from csv file
# only used for the beta version of the app and is very specific
def generateData():
    import pandas as pd
    df = pd.read_csv("data\AAPL.csv")
    df = df.drop("Open", 1)
    df = df.drop("High", 1)
    df = df.drop("Low", 1)
    df = df.drop("Adj Close", 1)
    df = df.drop("Volume", 1)
    return df

######### Web App settings ###############

class App(web.Application):
    
    def __init__(self):
        # Define routes
        handlers = [
            (r'/graph', graphHandler),
            (r'/', indexHandler)
        ]
 
        # define directories
        settings = {
            'template_path': 'template'
        }
        
        # Initialize Web App
        web.Application.__init__(self, handlers, **settings)
        
    
######### Page functions ##################

# redirect clients going to homepage to graph page
class indexHandler(web.RequestHandler):
    def get(self):
        self.render('stockGraph.html')


######### main client web page #############

# self = client
class graphHandler(websocket.WebSocketHandler):
    
    tick = 0 # a local copy of the TICK variable
    
    # Setting check_origin to true allows host to initialize connection
    # refer to https://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket
    def check_origin(self, origin):
        return True
    
    def open(self):
        
        # add new connections to subscribers list
        if self not in CONNECTIONSLIST:
            CONNECTIONSLIST.add(self)
            self.write_message("Welcome to SUTD Stock Exchange!")  
            
        # print("client {} connected.".format(self))
    def on_message(self, message):
        # If new client requests initial data
        if (message == "Request initial data"):
            
            # Only give latest {100} data points, defined by PLOTRANGE constant
            index = self.tick
            pRange = PLOTRANGE
            if (index - pRange < 0):
                pRange = index
            elif (index > priceDF.shape[0]):
                index = priceDF.shape[0]
            
            # Select last 100 rows
            rows = priceDF.iloc[index-pRange:index]
            
            # dump to json file
            jsonified = json.dumps({
                   'Date':rows["Date"].tolist(),
                   'Close':rows["Close"].tolist()
            })
            
            # Add custom protocol/signature and send
            jsonified = "initial`;" + jsonified
            self.write_message(jsonified)
    
    # Remove client from subscriber list once disconnected
    def on_close(self):
        if self in CONNECTIONSLIST:
            CONNECTIONSLIST.remove(self)
        # print("client {} disconnected.".format(self))
        
######### CALLBACK/PERIODIC FUNCTION ###############

# periodically send graph data to all clients at the same time
# called every {1} second(s), defined by FREQ
def sendGraphData():
    
    # Get next tick as index and copy to GraphHandler
    index = next(TICK)
    graphHandler.tick = index
    
    # select row and jsonify, add custom protocol "update `;"
    row = priceDF.iloc[index]
    jsonified = json.dumps({
                   'Date':[row["Date"]],
                   'Close':[row["Close"]]
            })
    jsonified = "update`;" + jsonified
    
    # send to all clients in connectionlist    
    try:
        for client in CONNECTIONSLIST:
            client.write_message(jsonified)
    
    # Once done, call this function again after {1} second(s), defined by FREQ
    finally:
        ioloop.IOLoop.instance().add_timeout(
                datetime.timedelta(seconds=FREQ), 
                sendGraphData
        )
        
        
################### initializer funtion ################

# Default main settings
def main():
    WebSocket_app = App()
    server = httpserver.HTTPServer(WebSocket_app)
    server.listen(PORT)
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=FREQ), sendGraphData)
    ioloop.IOLoop.instance().start()
        
    
if __name__ == '__main__':
    priceDF = generateData()
    main()
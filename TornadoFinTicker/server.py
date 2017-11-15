# -*- coding: utf-8 -*-

from tornado import websocket, web, httpserver
import tornado.ioloop as ioloop
import datetime, itertools, json

######### CONSTANTS ###########
TICK = itertools.count(2)
CONNECTIONSLIST = set()
priceDF = None
PLOTRANGE = 100
######### Web App settings ###############

class App(web.Application):
    def __init__(self):
        handlers = [
            (r'/graph', graphHandler),
            (r'/', indexHandler)
        ]
 
        settings = {
            'template_path': 'template'
        }
        web.Application.__init__(self, handlers, **settings)
        
    
################## Page functions ##########################
class indexHandler(web.RequestHandler):
    def get(self):
        self.render('stockGraph.html')


################# main client web page ###############

# self = client
class graphHandler(websocket.WebSocketHandler):
    
    tick = 0
    # For debugging purposes
    def check_origin(self, origin):
        return True
    
    def open(self):
        # add to subscribers list
        if self not in CONNECTIONSLIST:
            CONNECTIONSLIST.add(self)
            self.write_message("Welcome to SUTD SE!")
        
        print("client connected.")
        print("clients = ", CONNECTIONSLIST)

    def on_message(self, message):
        if (message == "Request initial data"):
            index = self.tick
            print(index)
            pRange = PLOTRANGE
            if (index - pRange < 0):
                pRange = index
            elif (index > priceDF.shape[0]):
                index = priceDF.shape[0]
            
            rows = priceDF.iloc[1:index]
            #jsonified = row.to_json()
            
            #print(type(jsonified))
            jsonified = json.dumps({
                   'Date':rows["Date"].tolist(),
                   'Close':rows["Close"].tolist()
            })
            jsonified = "initial`;" + jsonified
            self.write_message(jsonified)
    
    def on_close(self):
        if self in CONNECTIONSLIST:
            CONNECTIONSLIST.remove(self)
            
        print("client {} disconnected.".format("test"))
        
def generateData():
    import pandas as pd
    df = pd.read_csv("AAPL.csv")
    df = df.drop("Open", 1)
    df = df.drop("High", 1)
    df = df.drop("Low", 1)
    df = df.drop("Adj Close", 1)
    df = df.drop("Volume", 1)
    return df

# periodically send graph data to all clients at the same time
def sendGraphData():
    
    index = next(TICK)
    graphHandler.tick = index
    pRange = PLOTRANGE
    if (index - pRange < 0):
        pRange = index
    elif (index > priceDF.shape[0]):
        index = priceDF.shape[0]
    
    row = priceDF.iloc[index]
    jsonified = json.dumps({
                   'Date':[row["Date"]],
                   'Close':[row["Close"]]
            })
    #jsonified = row.to_json()
    try:
        for client in CONNECTIONSLIST:
            jsonified = "update`;" + jsonified
            client.write_message(jsonified)
    except Exception as e: print(e)
    finally:
        ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.5), sendGraphData)
################### main funtion ################

         
def main():
    PORT = 8886
    WebSocket_app = App()
    server = httpserver.HTTPServer(WebSocket_app)
    server.listen(PORT)
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.5), sendGraphData)
    ioloop.IOLoop.instance().start()
        
    
if __name__ == '__main__':
    priceDF = generateData()
    main()
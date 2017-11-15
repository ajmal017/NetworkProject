# -*- coding: utf-8 -*-

from tornado import websocket, web, httpserver
import tornado.ioloop as ioloop
import datetime, itertools

######### CONSTANTS ###########
TICK = itertools.count()
CONNECTIONSLIST = set()
priceDF = None

######### Web App settings ###############

class App(web.Application):
    def __init__(self):
        handlers = [
            (r'/graph', graphHandler)
        ]
 
        settings = {
            'template_path': 'templates'
        }
        web.Application.__init__(self, handlers, **settings)
        
    
################## Page functions ##########################

# Websocket connection (unused)
class WebSocketHandler(websocket.WebSocketHandler):
    def open(self):
        pass
 
    def on_message(self, message):
        self.write_message(u"Your message was: " + message)
 
    def on_close(self):
        pass

################# main client web page ###############

# self = client
class graphHandler(websocket.WebSocketHandler):
    
    def check_origin(self, origin):
        return True
    
    def open(self):
        # add to subscribers list
        if self not in CONNECTIONSLIST:
            CONNECTIONSLIST.add(self)
            self.write_message("Welcome to SUTDSE!")
        
        print("client {} connected.".format("test"))
        
        print("clients = ", CONNECTIONSLIST)

    def on_message(self, message):
        pass
    
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
    try:
        for client in CONNECTIONSLIST:
            row = priceDF.iloc[[index]].to_string(header=False, index=False, index_names=False).split("\n")
            row = [','.join(ele.split()) for ele in row]
            client.write_message(";".join(row))
        print("sending graph data")
    finally:
        ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=10), sendGraphData)
################### main funtion ################

         
def main():
    PORT = 8886
    WebSocket_app = App()
    server = httpserver.HTTPServer(WebSocket_app)
    server.listen(PORT)
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=5), sendGraphData)
    ioloop.IOLoop.instance().start()
        
    
if __name__ == '__main__':
    priceDF = generateData()
    main()
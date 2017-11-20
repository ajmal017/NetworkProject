# -*- coding: utf-8 -*-

from tornado import websocket, web, httpserver
import tornado.ioloop as ioloop
import datetime, itertools, json

######### CONSTANTS ######################
CONNECTIONSLIST = set()
NO_OF_HOSTS = {}
PORT = 12345

######### Web App settings ###############

class App(web.Application):
    
    def __init__(self):
        # Define routes
        handlers = [
            (r'/', connectionHandler),
        ]

        # Initialize Web App
        web.Application.__init__(self, handlers, **settings)

######### main client web page #############

# self = client
class connectionHandler(websocket.WebSocketHandler):
    # Setting check_origin to true allows host to initialize connection
    # refer to https://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket
    def check_origin(self, origin):
        return True
    
    def open(self):
        
        # add new connections to subscribers list
        if self not in CONNECTIONSLIST:
            CONNECTIONSLIST.add(self)

    def on_message(self, message):
        hosts_number = message.split(' ')
        if hosts_number[0] = "server":
            try:
                NO_OF_HOSTS[hosts_number[1]] = int(hosts_number[2])
            except:
                pass
        else:
            min_value = min(NO_OF_HOSTS.values())
            result = [key for key, value in NO_OF_HOSTS.iteritems() if value == min_value]
            self.write_message(result[0])
    
    # Remove client from subscriber list once disconnected
    def on_close(self):
        if self in CONNECTIONSLIST:
            CONNECTIONSLIST.remove(self)
        # print("client {} disconnected.".format(self))

################### initializer funtion ################

# Default main settings
def main():
    WebSocket_app = App()
    server = httpserver.HTTPServer(WebSocket_app)
    server.listen(PORT)
        
    
if __name__ == '__main__':
    main()
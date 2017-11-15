# -*- coding: utf-8 -*-

import websocket

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.create_connection("ws://127.0.0.1:8886/graph")
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    while True:
        result = ws.recv()
        print("Received {}".format(result))
        
    
    
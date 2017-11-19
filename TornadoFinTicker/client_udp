import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ip, 12345)

while True:
  print (s.recvform(512)[0])

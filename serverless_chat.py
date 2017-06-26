import socket
import struct
import time
import sys
import multiprocessing

def Rx():
    MCAST_GRP = '224.1.1.8'
    MCAST_PORT = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                                 # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
      rx_msg=sock.recv(10240)
      dcdmsg=rx_msg.decode("utf-8")
      print(dcdmsg)



def Tx(msg):
    MCAST_GRP = '224.1.1.8'
    MCAST_PORT = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    while True:
        msg=input(": ")
        msg=user+"# "+'"'+msg+'"'
        msg=bytes(msg, "ascii")
        sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
        time.sleep(1)


if __name__ == '__main__':


  print("Starting Chat Session\n")
  msg=""
  jobs = []
  user="kriswans"

  p = multiprocessing.Process(target=Rx)
  jobs.append(p)
  p.start()

  q = multiprocessing.Process(target=Tx(msg))
  jobs.append(q)
  q.start()

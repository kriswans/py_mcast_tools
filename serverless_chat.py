import socket
import struct
import time
import sys
import multiprocessing
import shutil


def Listen():
    userlist=[]
    MCAST_GRP = '224.1.1.8'
    MCAST_PORT = 5008
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                                 # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    userfile=open("userfile.txt","w")
    userfile.close()
    while True:
      list_user=sock.recv(10240)
      dcduser=list_user.decode("utf-8")
      if dcduser not in userlist:
        userfile=open("userfile.txt","a")
        userlist.append(dcduser)
        userfile.write(dcduser+'\n')
        userfile.close()
        time.sleep(1)
        print("{dcduser} has entered the chatroom\n".format(dcduser=dcduser))


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
      print(dcdmsg+"")

def DeleteUser():
    DEL_GRP ='224.1.1.8'
    DEL_PORT=5009
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DEL_PORT))  # use MCAST_GRP instead of '' to listen only
                                 # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(DEL_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
      rx_msg=sock.recv(10240)
      dcdmsg=rx_msg.decode("utf-8")
      del_f=open('userfile.txt','r')
      del_line=dcdmsg+'\n'
      userlist=del_f.readlines()
      print(userlist)
      userlist.remove(del_line)
      print(userlist)
      rewrite=open('rewrite.txt','w')
      for users in userlist:
          print(users)
          rewrite.write(users)
      rewrite.close
      shutil.copy("rewrite.txt","userfile.txt")



def Tx(msg, user):
    MCAST_GRP = '224.1.1.8'
    MCAST_PORT = 5007
    ADV_GRP = '224.1.1.8'
    ADV_PORT = 5008
    DEL_GRP ='224.1.1.8'
    DEL_PORT=5009

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    while True:
        useradv=("{user}".format(user=user))
        useradv=bytes(useradv, "ascii")
        sock.sendto(useradv, (ADV_GRP, ADV_PORT))

        while True:

            msg=input(": ")
            if msg == "exit":
                left="{user} has left the chatroom".format(user=user)
                left=bytes(left,"ascii")
                sock.sendto(left, (MCAST_GRP, MCAST_PORT))
                del_user=user
                del_user=bytes(del_user,"ascii")
                sock.sendto(del_user, (DEL_GRP, DEL_PORT))
                sys.exit()
            if msg == "who":
                who=open("userfile.txt","r")
                for lines in who:
                    print(lines)
                break
            else:
                hostname=(socket.gethostname())
                msg=user+'@'+hostname+"# "+'"'+msg+'"'
                msg=bytes(msg, "ascii")
                sock.sendto(msg, (MCAST_GRP, MCAST_PORT))

                useradv=("{user}".format(user=user))
                useradv=bytes(useradv, "ascii")
                sock.sendto(useradv, (ADV_GRP, ADV_PORT))
                time.sleep(1)
                break


    sys.exit()


if __name__ == '__main__':


  print("Starting Chat Session\n")
  msg=""
  jobs = []
  userlist=[]

  #user=input("Type chat handle: ")
  user=input("Please enter your chat handle: ")

  n = multiprocessing.Process(target=DeleteUser)
  jobs.append(n)
  n.start()

  o = multiprocessing.Process(target=Listen)
  jobs.append(o)
  o.start()

  p = multiprocessing.Process(target=Rx)
  jobs.append(p)
  p.start()

  q = multiprocessing.Process(target=Tx(msg, user))
  jobs.append(q)
  q.start()

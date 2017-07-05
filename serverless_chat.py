import socket
import struct
import time
import sys
import multiprocessing
import shutil
import datetime


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
        time.sleep(.5)
        print("{dcduser} has entered the chatroom\n".format(dcduser=dcduser))


def Rx():
    print("Starting Rx Process...")
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
      chatlog=open("chatlog.log","a")
      ts = time.time()
      st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
      chatlog.write(dcdmsg+": "+st+"\n")
      chatlog.close()

def DeleteUser():
    DEL_GRP ='224.1.1.8'
    DEL_PORT=5009
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DEL_PORT))  # use MCAST_GRP instead of '' to listen only
                                 # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(DEL_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    try:
        while True:
          rx_msg=sock.recv(10240)
          dcdmsg=rx_msg.decode("utf-8")
          del_f=open('userfile.txt','r')
          del_line=dcdmsg+'\n'
          userlist=del_f.readlines()
          userlist.remove(del_line)
          print("remaining users are: ")
          print(userlist)
          rewrite=open('rewrite.txt','w')
          for users in userlist:
              rewrite.write(users)
          rewrite.close
          shutil.copy("rewrite.txt","userfile.txt")
    except ValueError:
        pass
        DeleteUser()

def PrintTable(userlist,userlist1):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st+"\n")
        print("total users over time:\n")
        print (userlist)
        print ("active users:\n")
        print (userlist1)
        print ("users that have left:\n")
        print (list(set(userlist)-set(userlist1)))
        print("\n")

def UserTable():

        MCAST_GRP = '224.1.1.8'
        MCAST_PORT = 5008
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                                     # to MCAST_GRP, not all groups on MCAST_PORT
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        userlist1=[]
        userlist=[]

        while True:
            if len(userlist1) > 0:
                who=open('who','w')
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                who.write(st+"\n")
                who.write("total users over time:\n")
                who.write(str(userlist)+"\n")
                who.write("active users:\n")
                who.write(str(userlist1)+"\n")
                who.write("users that have left (since you logged in):\n")
                who.write(str(list(set(userlist)-set(userlist1))))
                who.write("\n")
                who.close()
            i=0
            try:
                userlist1=[]
            except:
                pass
            while i < (len(userlist1)+1)*6:
                list_user=sock.recv(10240)
                dcduser=list_user.decode("utf-8")
                userlist.append(dcduser)
                userlist=set(userlist)
                userlist=list(userlist)
                userlist1.append(dcduser)
                userlist1=set(userlist1)
                userlist1=list(userlist1)
                i=i+1

def InfHBeat():
    user=open("localuser","r")
    user=user.read()
    ADV_GRP = '224.1.1.8'
    ADV_PORT = 5008

    hostname=(socket.gethostname())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    while True:
        useradv=("{user}".format(user=user)+"@"+hostname)
        useradv=bytes(useradv, "ascii")
        sock.sendto(useradv, (ADV_GRP, ADV_PORT))
        time.sleep(5)


def Tx(msg, user):
    MCAST_GRP = '224.1.1.8'
    MCAST_PORT = 5007
    ADV_GRP = '224.1.1.8'
    ADV_PORT = 5008
    DEL_GRP ='224.1.1.8'
    DEL_PORT=5009

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    print("Starting Tx process.")

    hostname=(socket.gethostname())

    z = multiprocessing.Process(target=InfHBeat)
    jobs.append(z)
    z.start()

    while True:
        while True:
            msg=input(": ")
            if msg == "exit":
                user_d=("{user}".format(user=user)+"@"+hostname)
                left="{user} has left the chatroom".format(user=user_d)
                left=bytes(left,"ascii")
                sock.sendto(left, (MCAST_GRP, MCAST_PORT))
                del_user=user
                del_user=bytes(del_user,"ascii")
                sock.sendto(del_user, (DEL_GRP, DEL_PORT))
                sys.exit()
            if msg == "#who":
                who=open("who","r")
                for lines in who:
                    print(lines)
                break
            if msg == "#send":
                name=""
                name=input("Filename?: ")
                fn=open(name, "rb")
                for lines in fn:
                    lines=bytes(lines)
                    sock.sendto(lines, (MCAST_GRP, MCAST_PORT))
                fn.close()
                break
            if msg == "#help":
                hf=open("helpfile", "r")
                for lines in hf:
                    print(lines)
                hf.close()
                break
            if msg == "#log":
                cl=open("chatlog.log", "r")
                for lines in cl:
                    print(lines)
                cl.close()
                break


            else:
                hostname=(socket.gethostname())
                msg=user+'@'+hostname+"# "+'"'+msg+'"'
                msg=bytes(msg, "ascii")
                sock.sendto(msg, (MCAST_GRP, MCAST_PORT))


    sys.exit()


if __name__ == '__main__':


  print("Starting Chat Session\n")
  print("Type 'help or '?' for list of commands\n")
  msg=""
  jobs = []
  userlist=[]
  chatlog=open("chatlog.log","w")
  chatlog.close()


  #user=input("Type chat handle: ")
  user=input("Please enter your chat handle: ")
  localuser=open("localuser","w")
  localuser.write(user)
  localuser.close()

  m = multiprocessing.Process(target=DeleteUser)
  jobs.append(m)
  m.start()

  n = multiprocessing.Process(target=UserTable)
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

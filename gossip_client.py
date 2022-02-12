import socket
import threading
import random

port = 1250
header = 64

#server = '192.168.175.1'
s = socket.gethostbyname(socket.gethostname())
addr = (s, port)

disconnect_message = 'DISCONNECTING!'

infected_count = 0
clients= dict()

n = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(5)]


clients['P'] = ['infected',n[0],'The quick brown fox jumps over the lazy dogs']
clients['Q'] = ['susectible',n[1],'abcd']
clients['R'] = ['susectible',n[2],'efgh']
clients['S'] = ['susectible',n[3],'ijkl']
clients['T'] = ['susectible',n[4],'mnop']


def infect(msg,z):

    message=msg.encode('utf-8')

    msg_len = len(message)
    send_len=str(msg_len).encode('utf-8')

    send_len += b' ' * (header - len(send_len))

    clients[z][1].sendall(send_len)
    clients[z][1].sendall(message)



def node_sending(f):
    clients[f][1]=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients[f][1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
       clients[f][1].connect(addr)

       infect(clients['P'][2],f)
       infect(disconnect_message,f)

    except socket.error as e:
         pass

    clients[f][1].close()


def node_recv(g):
    clients[g][1]=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients[g][1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    try:

        clients[g][1].connect(addr)
        clients[g][2]=clients[g][1].recv(4096).decode('utf-8')

        if clients[g][2] == clients['P'][2]:
            clients[g][0] = 'infected'


        infect(disconnect_message,g)
    except socket.error as e:
        pass

    clients[g][1].close()


def rounds(infected_count):
    for k in clients.keys():
        if clients[k][1] == 'infected':

           infected_count+=1
    return infected_count/5


#round 1
node_sending('P')

node_recv('Q')

nodes=['Q','R','S','T']
count = 1
for i in nodes:
    nodes_a=[a for a in ['P','Q','R','S','T'] if a != i]
    j=random.choice(nodes_a)
    count+=1
    print('\nRound ',count,'Node:',i,'sending to Node:',j,'\n')
    node_sending(i)
    node_recv(j)
    if rounds(infected_count) >= 0.6:
        break


for i in clients.keys():
    print(clients[i][0],' ',clients[i][2])

print('\naborting message multicast!\n')

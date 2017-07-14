Breana Tate
brt2109
README.txt

Programmed in Python 2.7.6
Part 2: Implements the Go-Back-N Protocol
This version initializes a connection between the sender and receiver. The command line systax is:
python gbnnode.py <self-port> <peer-port> <window-size> [ -d <value-of-n> | -p <value-of-p>]
Where -d and -p denote the method used to determine how packets are dropped on the receiver side. The corresponding value of n and p denote the nth number packet being dropped, and the probability a packet is dropped, respectively. To send a message containing packets, the user types "send" and the message after the "node>" prompt. If send does not follow directly after, it will not send packets. The packet format is synthesized using python's struct, in which one is able to specify what types of data are in a message, "pack it", then have it "unpacked" on the other end. In this case, 'Ic' denotes that an integer (which is the ACK) and a character make up the packet. 

Packets messages are put into a sending buffer before sent, which was implemented as a list. When the corresponding acks are recieved, the messages are 'popped' from the sending buffer. The window does not entirely work, but is a collaboration between two integers, window_count and window_size, initialized as 0 and whatever the user inputed as the window size, respectively. The numbers are compared to see where the window is. The window doesn't move if the corresponding ACK has not been received. Window recognizes when the values have exceeded it's size, but isn't always reliable in what to do next.





Part 3: Implements the Distance-Vector Routing Algorithm

The routing table for each node is initialized as a dictionay, where the key is the source node, and the values are the rest of the command line inputs, which are the neighboring ports, followed by their distances from the source node. When the last node is added denoted by "last" at the end of the command line input, the nodes print their initial routing tables. 

Command line format:  python dvnode.py <local-port> <neighbor1-port> <loss-rate-1> <neighbor2-port> <loss-rate-2> ... [last]

**Note: "last" should end the line only if the user wants to begin routing table exchange

The nodes alert the user when they receive information from or send information to another node. 




Tests: 

gbnnode.py:
IN DETERMINISTIC DROPPING MODE:
**timer broken
SENDER:

python2.7 gbnode.py  1111 2222 5 -d 3
>node send abcdef
packet0 timeout
[1493005171.12] packet 0 a sent
packet0 timeout
[1493005171.12] packet 1 b sent
packet0 timeout
[1493005171.12] packet 2 c sent
packet0 timeout
[1493005171.12] packet 3 d sent
packet0 timeout
[1493005171.12] packet 4 e sent
packet0 timeout
[1493005171.12] packet 5 f sent
[1493005171.12] ACK0 received, window moves to 1
[1493005171.12] ACK1 received, window moves to 2


RECEIVER:

python2.7 gbnode.py  2222 1111 5 -d 3
>node [1493005171.12] Received Packet Num 0 a
[1493005171.12] ACK0 sent, expecting packet1
[1493005171.12] Received Packet Num 1 b
[1493005171.12] ACK1 sent, expecting packet2
[1493005171.12] Packet2 c discarded
[1493005171.12] ACK1 sent, expecting packet2
[1493005171.12] Received Packet Num 3 d
[1493005171.12] ACK1 sent, expecting packet2
[1493005171.12] Received Packet Num 4 e
[1493005171.12] ACK1 sent, expecting packet2
[1493005171.12] Packet5 f discarded
[1493005171.12] ACK1 sent, expecting packet2


IN PROBABILISTIC DROPPING MODE:
SENDER:

python2.7 gbnode.py  1111 2222 5 -p .3
>node send abcdefg
packet0 timeout
[1493005281.66] packet 0 a sent
packet0 timeout
[1493005281.66] packet 1 b sent
packet0 timeout
[1493005281.66] packet 2 c sent
packet0 timeout
[1493005281.66] packet 3 d sent
packet0 timeout
[1493005281.66] packet 4 e sent
packet0 timeout
[1493005281.66] packet 5 f sent
packet0 timeout
[1493005281.66] packet 6 g sent
[1493005281.66] ACK0 received, window moves to 1
[1493005281.66] ACK1 received, window moves to 2
[1493005281.66] ACK2 received, window moves to 3
[1493005281.66] ACK3 received, window moves to 4
[1493005281.66] ACK4 received, window moves to 5



RECEIVER: 
python2.7 gbnode.py  2222 1111 5 -p .3
>node [1493005281.66] Received Packet Num 0 a
[1493005281.66] ACK0 sent, expecting packet1
[1493005281.66] Received Packet Num 1 b
[1493005281.66] ACK1 sent, expecting packet2
[1493005281.66] Received Packet Num 2 c
[1493005281.66] ACK2 sent, expecting packet3
[1493005281.66] Received Packet Num 3 d
[1493005281.66] ACK3 sent, expecting packet4
[1493005281.66] Received Packet Num 4 e
[1493005281.66] ACK4 sent, expecting packet5
[1493005281.66] Received Packet Num 5 f
[1493005281.66] ACK5 sent, expecting packet6
[1493005281.66] Received Packet Num 6 g
[1493005281.66] ACK6 sent, expecting packet7


WHEN prob = 0:

SENDER:
python2.7 gbnode.py  1111 2222 5 -p 0
>node send abcdefg
packet0 timeout
[1493005352.83] packet 0 a sent
packet0 timeout
[1493005352.83] packet 1 b sent
packet0 timeout
[1493005352.83] packet 2 c sent
packet0 timeout
[1493005352.83] packet 3 d sent
packet0 timeout
[1493005352.83] packet 4 e sent
packet0 timeout
[1493005352.83] packet 5 f sent
packet0 timeout
[1493005352.83] packet 6 g sent
[1493005352.83] ACK0 received, window moves to 1
[1493005352.83] ACK1 received, window moves to 2
[1493005352.83] ACK2 received, window moves to 3
[1493005352.83] ACK3 received, window moves to 4
[1493005352.83] ACK4 received, window moves to 5


RECEIVER:

python2.7 gbnode.py  2222 1111 5 -p 0
>node [1493005352.83] Received Packet Num 0 a
[1493005352.83] ACK0 sent, expecting packet1
[1493005352.83] Received Packet Num 1 b
[1493005352.83] ACK1 sent, expecting packet2
[1493005352.83] Received Packet Num 2 c
[1493005352.83] ACK2 sent, expecting packet3
[1493005352.83] Received Packet Num 3 d
[1493005352.83] ACK3 sent, expecting packet4
[1493005352.83] Received Packet Num 4 e
[1493005352.83] ACK4 sent, expecting packet5
[1493005352.83] Received Packet Num 5 f
[1493005352.83] ACK5 sent, expecting packet6
[1493005352.83] Received Packet Num 6 g
[1493005352.83] ACK6 sent, expecting packet7









dvnode.py:
NODE 1: 

python2.7 dvnode.py  1111 2222 .1 3333 .5
[1493005551.91] Node 1111 Routing Table
(.1) -> Node 2222
(.5) -> Node 3333
[1493005553.98] Message received at Node 1111 from Node 2222
[1493005553.98] Message sent from Node 1111 to Node 2222
[1493005553.98] Message sent from Node 1111 to Node 3333
[1493005553.98] Message sent from Node 1111 to Node 1111
[1493005553.99] Node 1111 Routing Table
(.1.2) -> Node 2222
(.1.2) -> Node 2222; Next hop -> Node1111 
(.5) -> Node 3333
(.5) -> Node 3333; Next hop -> Node1111 


NODE 2: 

python2.7 dvnode.py  2222 1111 .1 3333 .2 4444 .8
[1493005548.86] Node 2222 Routing Table
(.1) -> Node 1111
(.2) -> Node 3333
(.8) -> Node 4444
[1493005553.98] Message received at Node 2222 from Node 4444
[1493005553.98] Message sent from Node 2222 to Node 1111
[1493005553.98] Message sent from Node 2222 to Node 3333
[1493005553.98] Message sent from Node 2222 to Node 4444
[1493005553.98] Message sent from Node 2222 to Node 2222
[1493005553.98] Node 2222 Routing Table
(.1) -> Node 1111
(.1) -> Node 1111; Next hop -> Node2222 
(.2) -> Node 3333
(.2) -> Node 3333; Next hop -> Node2222 
(.8) -> Node 4444
(.8) -> Node 4444; Next hop -> Node2222 



NODE 3:
python2.7 dvnode.py  3333 1111 .5 2222 .2 4444 .5
[1493005546.63] Node 3333 Routing Table
(.5) -> Node 1111
(.2) -> Node 2222
(.5) -> Node 4444
[1493005553.98] Message received at Node 3333 from Node 4444
[1493005553.98] Message sent from Node 3333 to Node 1111
[1493005553.98] Message sent from Node 3333 to Node 2222
[1493005553.98] Message sent from Node 3333 to Node 4444
[1493005553.98] Node 3333 Routing Table
(.5) -> Node 1111
(.2) -> Node 2222
(.5) -> Node 4444


NODE 4/LAST:

python2.7 dvnode.py  4444 2222 .8 3333 .5 last
[1493005553.98] Node 4444 Routing Table
(.8) -> Node 2222
(.5) -> Node 3333
[1493005553.98] Message sent from Node 4444 to Node 2222
[1493005553.98] Message sent from Node 4444 to Node 3333
[1493005553.98] Message received at Node 4444 from Node 2222
[1493005553.98] Message sent from Node 4444 to Node 2222
[1493005553.98] Message sent from Node 4444 to Node 3333
[1493005553.98] Node 4444 Routing Table
(.8) -> Node 2222
(.5) -> Node 3333






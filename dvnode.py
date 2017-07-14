import sys
import socket
import argparse
import time
from threading import *


#The data field of a packet should include 1) the sending node UDP listening port number (to identify the
#sending node to its neighbor) and 2) the most recent routing table.

def createNode(port):

	nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	nodeSocket.bind(("", int(port)))
	#nodeSocket.setblocking(0)

	return nodeSocket

#sol_socket socket.so_broadcast
#setsockopt

def listen(listenSocket, name, routing_list):
	message, senderAddress = listenSocket.recvfrom(2048) 
	new_routing_info = message.split("-")
	#[<timestamp>] Message received at Node <port-vvvv> from Node <port-xxxx>
	print "[{}] Message received at Node {} from Node {}".format(time.time(), name, new_routing_info[0])
	routing_dict = {}
	routing_dict[name] = routing_list
	n = 1
	t = 0
	while n<=len(routing_list):
		while t<len(routing_list):
			if routing_list[n] == new_routing_info[n+1]:
				if routing_list[t] > new_routing_info[t]+new_routing_info[t+2]:
					routing_list[n] = new_routing_info[t]+new_routing_info[t+2]
					#routing_list[t] = "(next hop)->"+"-"+routing_list[t][t+1]+"-"+new_routing_info[t+3]
			if new_routing_info[n] not in routing_list:
				routing_list.append(new_routing_info[n])
			t+=2
		n+=2
	routing_dict[name] = routing_list
	#doBellmanFord(new_routing_info, routing_list)
	exchange(routing_dict, listenSocket)
	printRoutingList(routing_dict)

def doBellmanFord(new_routing_info, old_routing_info):
	
	node_list.append
	updated_dict = []
	updated_list = []
	sourcenode = new_routing_info[0]
	n = 1
	t = 0
	while n < len(new_routing_info):
		while t <len(old_routing_info):
			if new_routing_info[n] == old_routing_info[t]:
				next_hop = new_routing_info[n]
				old_routing_info.append(next_hop)
				old_routing_info.append(new_routing_info[t])
				print new_routing_info[n]
				print old_routing_info
			t+=2
		n+=2
		#distance = routing_list[n+1]
		#print "({}) -> Node {}".format(distance, port)
		#n+=2
		return updated_dict


def exchange(routing_table, senderSocket):
	#[<timestamp>] Message sent from Node <port-xxxx> to Node <port-vvvv>
	host = socket.gethostname()
	
	for node in routing_table:
		routing_list = routing_table[node]
		node_list = [node]
		routing_two = node_list+routing_table[node]
		sentence_routing = '-'.join(routing_two)
		for neighbor in routing_list[0::2]:
			if neighbor!="last":
				#print neighbor
				print "[{}] Message sent from Node {} to Node {}".format(time.time(), node, neighbor)
				senderSocket.sendto(sentence_routing, (host, int(neighbor)))
def printInitialRoutingList(routing_dict):
	#Initial Routing Table
	#[<timestamp>] Node <port-xxxx> Routing Table
	for node in routing_dict:
		routing_list = routing_dict[node]
		print "[{}] Node {} Routing Table".format(time.time(), node)
		n = 0
		while n < len(routing_list) and routing_list[n]!= "last":
			port = routing_list[n] 
			distance = routing_list[n+1]
			print "({}) -> Node {}".format(distance, port)
			n+=2
def printRoutingList(routing_dict):
	for node in routing_dict:
		routing_list = routing_dict[node]
		print "[{}] Node {} Routing Table".format(time.time(), node)
		n = 0
		while n < len(routing_list) and routing_list[n]!= "last":
			port = routing_list[n] 
			distance = routing_list[n+1]
			print "({}) -> Node {}".format(distance, port)
			n+=2
			if len(routing_list)%2!=0:
				print "({}) -> Node {}; Next hop -> Node{} ".format(distance, port, routing_list[-1])


	# 	- (<distance>) -> Node <port-yyyy>
	# - (<distance>) -> Node <port-zzzz> ; Next hop -> Node <port-yyyy>
	# - (<distance>) -> Node <port-vvvv>
	# - (<distance>) -> Node <port-wwww> ; Next hop -> Node <port-vvvv>
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('inputs', nargs ='*')
	args = parser.parse_args()
	# print (args.inputs)
	localport = args.inputs[0]
	routing_list = []
	#routing_list.append(localport)
	for num in args.inputs:
		if num!=args.inputs[0]:
			routing_list.append(num)
	#python dvnode.py <local-port> <neighbor1-port> <loss-rate-1> <neighbor2-port> <loss-rate-2> ... [last]
	node = createNode(localport)
	node_dict = {}
	node_dict[localport] = (routing_list)
	listenThread = Thread(target = listen, args = (node,localport, routing_list))
	listenThread.start()
	printInitialRoutingList(node_dict)
	routing_info = {}
	if args.inputs[-1] == 'last':
		exchange(node_dict, node)

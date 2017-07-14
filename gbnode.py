#Breana Tate
#brt2109
#gbnode.py

import sys
import struct
import socket
from threading import *
import time
from random import randint

#Create sender socket, initialize window size, send messages
def sender(selfport, peerport, window):
	receiverName = socket.gethostname()
	senderPort = selfport
	receiverPort = peerport
	window_size = window
	senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	#senderSocket.setblocking(0)
	message = raw_input(">node ")
	window_count = 0
	packet_count = 0
	sendingBuffer = []
	if message.split(" ")[0]=="send":
		sendingBuffer = list(message.split(" ")[1])
	if window_count < window_size:
		for message in sendingBuffer:
			#creates packet and sends it
			modMessage = struct.pack('!Ic', packet_count, sendingBuffer[packet_count])
			senderSocket.sendto(modMessage, (receiverName, int(receiverPort)))
			#timer
			t = Timer(500.0 / 1000.0, timeout(window_count))
			t.start()
			print "[{}] packet {} {} sent".format(time.time(), packet_count, sendingBuffer[packet_count])
			packet_count+=1 
	while len(sendingBuffer)>0:
		modifiedMessage, receiverAddress = senderSocket.recvfrom(2048)
		if int(modifiedMessage) == window_count: 
			t.cancel()
			print "[{}] ACK{} received, window moves to {}".format(time.time(), window_count, window_count+1)
			if len(sendingBuffer)>1:
				sendingBuffer.pop(int(modifiedMessage)-1)
			#print sendingBuffer
			window_count+=1 
		elif int(modifiedMessage)!= window_count: 
			print "[{}] ACK{} received, window moves to {}".format(time.time(), window_count, window_count+1)
			senderSocket.sendto(modMessage, (receiverName, int(receiverPort)))
			print sendingBuffer
	if window_count== window_size:
		window_count = 0


		#modMessage = struct.pack('!Ic', window_count, sendingBuffer[window_count])
		#senderSocket.sendto(modMessage, (receiverName, int(receiverPort)))
def timeout(num):
	print "packet{} timeout".format(num)	
# def listenSender(sender):
# 	senderSocket = sender
# 	message, receiverAddress = senderSocket.recvfrom(2048)
# 	return message

# def listenReceiver(receiver):
# 	receiverSocket = receiver
# 	message, senderAddress = receiverSocket.recvfrom(2048) 
# 	return message

#receiver
def receiver(selfport, window, dropmode, prob):
	receiverPort = selfport
	receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiverSocket.bind(('', int(receiverPort)))
	#receiverSocket.setblocking(0)
	sendingBuffer = []
	windowsize = window
	window_expect = 0
	num_discarded = 0
	num = 1
	while 1:
		message, senderAddress = receiverSocket.recvfrom(2048) 
		ack, modMessage = struct.unpack('!Ic', message)
		sendingBuffer.append(ack)
		ack_message = ack
		if dropmode == "-d":
			if num%int(prob)!=0:
				if ack_message == window_expect:
					print "[{}] Received Packet Num {} {}".format(time.time(),str(ack),modMessage)
					receiverSocket.sendto(str(sendingBuffer[window_expect]), senderAddress)
					window_expect+=1
					print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect)
				elif ack_message!= window_expect:
					print "[{}] Received Packet Num {} {}".format(time.time(),str(ack),modMessage)
					print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(sendingBuffer[window_expect-1]),window_expect)
				num+=1
			elif num%int(prob)== 0:
				print "[{}] Packet{} {} discarded".format(time.time(),str(ack),modMessage)
				print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(window_expect-1),window_expect)
				num+=1
				num_discarded+=1
		elif dropmode == "-p":
			rand = (randint(0,9))
			mult = rand* prob

			# if ack_message == window_expect:
			# 	print "[{}] Received Packet Num {} {}".format(time.time(),str(ack),modMessage)
			# 	receiverSocket.sendto(str(sendingBuffer[window_expect]), senderAddress)
			# 	window_expect+=1
			# 	print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect+1)
			num+=1
			if prob ==1:
				print "[{}] Packet{} {} discarded".format(time.time(),str(ack),modMessage)
				print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect)
				num+=1 
				num_discarded+=1
			elif prob ==0:
				if ack_message == window_expect:
					print "[{}] Received Packet Num {} {}".format(time.time(),str(ack),modMessage)
					receiverSocket.sendto(str(sendingBuffer[window_expect]), senderAddress)
					window_expect+=1
					print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect)
				num+=1
			elif prob!=0 and prob!=1 and mult>1:
				if ack_message == window_expect:
					print "[{}] Received Packet Num {} {}".format(time.time(),str(ack),modMessage)
					receiverSocket.sendto(str(sendingBuffer[window_expect]), senderAddress)
					window_expect+=1
					print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect)
				num+=1
			elif prob!=0 and prob!=1 and mult<1:
				print "[{}] Packet{} {} discarded".format(time.time(),str(ack),modMessage)
				print "[{}] ACK{} sent, expecting packet{}".format(time.time(),str(ack),window_expect)
				num+=1 
				num_discarded+=1
		loss_rate = (num_discarded/len(sendingBuffer))
	print "[Summary] {} packets discarded, loss rate= {}".format(num_discarded, loss_rate)



if __name__ == "__main__":

	selfport = sys.argv[1]
	peerport = sys.argv[2]
	windowsize = sys.argv[3]
	choice =sys.argv[4]
	p = sys.argv[5]
	receiveThread = Thread(target = receiver, args = (selfport, windowsize, choice, p))
	receiveThread.start()
	#listenReceiverThread = Thread(target= listenReceiver, args =)
	sendThread = Thread(target = sender, args = (selfport, peerport, windowsize))
	sendThread.start()

	#listenSenderThread = Thread(target= listenSender, args =)

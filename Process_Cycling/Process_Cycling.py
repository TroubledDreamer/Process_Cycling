#!/bin/python3

import math
import os
import random
import re
import sys

#
# Please Paste all Fuctions from Part 1,2,3,4,5,6 & 7
# Complete the function below.
#
def makePacket(srcIP, dstIP, length, prt, sp, dp, sqn, pld):
    #takes in the SRC, DST, LEN, PRT, SP, DP, SQN, PLD and returns them in the packet format("PK", SRC, DST, [])
    return ("PK",srcIP,dstIP,[length,prt,[sp,dp],sqn,pld])
   
def getPacketSrc(pkt):
    #takes a packet as a input and returns the IP source
    return str(pkt[1])
   
def getPacketDst(pkt):
    return str(pkt[2])
    #takes a packet as a input and returns the IP Destination

   
def getPacketDetails(pkt):
    #takes a packet as a input and returns a list of packet details
    return pkt[3]

   
def isPacket(pkt):
    #takes a packet as a input and returns weather it meets the requirments of a packet
    return type(pkt) == tuple and pkt[0] == "PK" and len(pkt) == 4  and type(getPacketDetails(pkt)) == list

def isEmptyPkt(pkt):
    #takes a packet as a input and returns weather its contents in empty
    return getPacketDetails(pkt) == []

def getLength(pkt):
    #takes a packet as a input and returns the length attribute in the packet details
    return getPacketDetails(pkt)[0]

def getProtocol(pkt):
    #takes a packet as a input and returns the Protocole attribute in the packet details
    return str(getPacketDetails(pkt)[1])

def getPacketPorts(pkt):
    #takes a packet as a input and returns the port list in the packet details
    return getPacketDetails(pkt)[2]

def getSrcPort(pkt):
    #takes a packet as a input and returns the source port attribute in the portlist
    return getPacketPorts(pkt)[0]

def getDstPort(pkt):
    #takes a packet as a input and returns the destination port attribute in the portlist
    return getPacketPorts(pkt)[1]

def getSqn(pkt):
    #takes a packet as a input and returns the sequence number attribute in the packet details
    return getPacketDetails(pkt)[3]

def getPayloadSize(pkt):
    #takes a packet as a input and returns the Pay load Size attribute in the packet details
    return getPacketDetails(pkt)[4]

   
def flowAverage(pkt_list):
    #accept a list of packets and gets the average payload size of all the packets and returns a list of packets that are above the average of the list.
    
    #uses list comprhension to loop through pkt_list and sums every Payload Size in the element in the list the divides it by the number of pkts
    avg = sum(list(map(getPayloadSize,pkt_list))) / len(pkt_list)
    
    #loops through a list and checks it the packet Payload Size is above the average
    return [pkt for pkt in pkt_list if getPayloadSize(pkt) > avg]
       

def suspPort(pkt):
    #checks to see if the packet inputted is valid
    if isPacket(pkt):
        #checks to see if the packet inputted is empty
        if isEmptyPkt(pkt):
            return "Packet is Empty"
        else:
            # checks if the SrcPort and DstPort have a have over 500
            return getSrcPort(pkt) > 500 or getDstPort(pkt) > 500
               

def suspProto(pkt):
    #checks to see if the packet inputted is valid
    if isPacket(pkt):
        #checks to see if the packet inputted is empty
        if isEmptyPkt(pkt):
            return "Packet is Empty"
        else:
            #checks if the Protocol is in the given protocal list
            if getProtocol(pkt) in ProtocolList:
                return False
            else:
                return True

def ipBlacklist(pkt):
    #checks to see if the packet inputted is valid
    if isPacket(pkt):
        #checks to see if the packet inputted is empty
        if isEmptyPkt(pkt):
            return "Packet is Empty"
        else:
            #checks if the Protocol is in the given IP blacklist list
            return getPacketSrc(pkt) in IpBlackList
               
def calScore(pkt):
    total = 0
    #checks to see if the packet inputted is valid and the packet is not empty
    if isPacket(pkt)and not isEmptyPkt(pkt):
        #if the packet passes the flow average test it add 3.56 to the score
        if pkt in flowAverage(pkt_list): total += 3.56
            
        #if the packet passes the susp Protocol test it add 2.74 to the score
        if suspProto(pkt) == True: total += 2.74
            
        #if the packet passes the susp Port test it add 1.45 to the score
        if suspPort(pkt): total += 1.45
            
        #if the packet passes the ip Blacklist test it add 10 to the score
        if ipBlacklist(pkt): total += 10
            
        #returns the score to the second decimal
        return round(total,2)
    else:
        if not isPacket(pkt):
            return ("Packet: Is not a packet")
        else:
            return ("Packet: Is empty")
  # Write your code here
       
def makeScore(pkt_list):
    #takes a packet list a input and returns a score
    
    #loops through a list of packets and makes a list of tupes of each packet and their calculated score
    return ("Score",[(pkt,calScore(pkt)) for pkt in pkt_list])
   
def scoreDetails(ScoreList):
    #takes a score list as a input and returns its contents
    return ScoreList[1]  

def addPacket(ScoreList, pkt):
    #checks to see if the score inputted is valid
    
    if isScore(ScoreList):
    #checks to see if the packet inputted is valid and the packet is not empty
        if isPacket(pkt) and not isEmptyPkt(pkt):
            #caluclates the packet score
            a = calScore(pkt)
            
            #adds the a tuple of a packet and its score to the end on the score list
            scoreDetails(ScoreList).append((pkt,a))
        return ("Packet: Is not a packet")
    else:
        if not isScore(ScoreList):
            return ("Scorelist: Is not a scorelist")
   
           

def getSuspPkts(ScoreList):
    #checks to see if the score inputted is valid and the score is not empty
    if isScore(ScoreList) and not isEmptyScore(ScoreList):  
        #returns a list of the packets with the score over 5 in the score list
        return [pkt[0] for pkt in scoreDetails(ScoreList) if scoreDetails(pkt) > 5.00]
   

def getRegulPkts(ScoreList):
    #checks to see if the score inputted is valid and the score is not empty
    if isScore(ScoreList) and not isEmptyScore(ScoreList):
        #returns a list of the packets with the score under or equal to 5 in the score list
        return list(map(lambda pkt: pkt[0], my_filter(lambda pkt: scoreDetails(pkt) <= 5.00, scoreDetails(ScoreList))))

   
def my_filter(pred, lst):
    #filter bases on a predicate
    if lst == []:
        return []
    elif pred(lst[0]):
        return [lst[0]] + my_filter(pred, lst[1:])
    else:
        return my_filter(pred, lst[1:])


def isScore(ScoreList):
    #returns the score list is valid or not
    return type(ScoreList) == tuple and ScoreList[0] == "Score" and type(scoreDetails(ScoreList)) == list and len(ScoreList) == 2


def isEmptyScore(ScoreList):
    #returns weather the scorelists contents is empty or not
    #checks to see if the score inputted is valid
    if isScore(ScoreList):
        return scoreDetails(ScoreList) == []
  # Write your code here

def makePacketQueue():
    #creats a priority queue
    return ("PQ",[])

def contentsQ(q):
    #returns the contents on a queque
    return q[1]

def frontPacketQ(q):
    #checks to see if the queue inputted is valid
    if isPacketQ(q):
        #return the contents of the queque
        return contentsQ(q)[0]
    return ("PacketQ: Not a packet queue")


def addToPacketQ(pkt,q):
    #checks to see if the queue inputted is valid
    if isPacketQ(q):
        #checks the position and adds the packet to the queue
        contentsQ(q).insert(get_pos(pkt,contentsQ(q)),pkt)
    return ("PacketQ: Not a packet queue")
  # Write your code here

def get_pos(pkt,lst):
    if (lst == []):
        return 0
    elif getSqn(pkt) < getSqn(lst[0]):
        return 0 + get_pos(pkt,[])
    else:
        return 1 + get_pos(pkt,lst[1:])
           
def removeFromPacketQ(q):
    #checks to see if the queue inputted is valid and the queue is not empty
    if isPacketQ(q) and not isEmptPacketQ(q):
        #removes the first item on the queque
        contentsQ(q).pop(0)
    return ("PacketQ: Not a packet queue")

def isPacketQ(q):
    #returns the Queue is valid or not
    return type(q) == tuple and q[0] == "PQ" and len(q) == 2 and type(contentsQ(q)) == list
  # Write your code here

def isEmptPacketQ(q):
    #returns weather the scorelists contents is empty or not

    #checks to see if the queue inputted is valid
    if isPacketQ(q):
        return contentsQ(q) == []
    return ("PacketQ: Not a packet queue")


def makePacketStack():
    #Creates a stack 
    return ("PS",[])

    
def contentsStack(stk):
    #returns the contents on a stack
    return stk[1]

def topProjectStack (stk):
    #checks to see if the stack inputted is valid and the stack is not empty
    if isPKstack(stk) and not isEmptyPKStack(stk):
        #returns the item on the top of the stack
        return contentsStack(stk)[-1]
    return ("Error: Is not a Pkstack")


def pushProjectStack(pkt,stk):
    #checks to see if the stack inputted is valid 
    if isPKstack(stk):
        #addes a packet to the top of the stack
        contentsStack(stk).append(pkt)
    return ("Error: Is not a Pkstack")
  # Write your code here

def popPickupStack(stk):
    #checks to see if the stack inputted is valid and the stack is not empty
    if isPKstack(stk) and not isEmptyPKStack(stk):
        #removes the top item of the stack
        contentsStack(stk).pop(-1)
    return ("Error: Is not a Pkstack")
  # Write your code here

def isPKstack(stk):
    #returns the stack is valid or not
    return type(stk) == tuple and stk[0] == "PS" and type(contentsStack(stk)) == list and len(stk) == 2

def isEmptyPKStack(stk):
    #returns weather the stack contents is empty or not
    #checks the stack is valid or not
    if isPKstack(stk):
        return contentsStack(stk) == []
    return ("Packet Stack: Not a packet stack")
   

def sortPackets(scoreList,stack,queue):
    
    
    
    #checks to see if the score inputted is valid 
    if isScore(scoreList):
        #cecks which packet are Susp and adds all the Susp packet to the stack 
        x = [pushProjectStack(pkt,stack) for pkt in getSuspPkts(scoreList)]
        #cecks which packet are Susp and adds all the regular packet to the queue
        y = [addToPacketQ(pkt,queue) for pkt in getRegulPkts(scoreList)]
        
        #returns the contents of the stack and queque in a tuple
        return(contentsStack(stack),contentsQ(queue))

def analysePackets(packet_List):
    pkt_list = []
    #loops through the list of packets and assigns them to their assosiated verable
    for pkt in packet_List:
        src, dst, leng, pt, s, d, sq, pl = range(len(pkt))
        srcIP = pkt[src]
        dstIP = pkt[dst]
        length = pkt[leng]
        prt = pkt[pt]
        sp = pkt[s]
        dp = pkt[d]
        sqn = pkt[sq]
        pld = pkt[pl]
        #makes a packet and as it to the packet list
        pkt_list.append(makePacket(srcIP, dstIP, length, prt, sp, dp, sqn, pld))
    
    a = list(map(calScore,pkt_list))
    
    #makes a score using a the packet list created
    score = makeScore(pkt_list)
    
    #makes new stack
    stack = makePacketStack()
    #makes new queque
    queue = makePacketQueue()
    
    sortPackets(score,stack,queue)
    
    #returns the queque
    return queue
   

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()
    print(first_multiple_input)
    srcIP = str(first_multiple_input[0])
    dstIP = str(first_multiple_input[1])
    length = int(first_multiple_input[2])
    prt = str(first_multiple_input[3])
    sp = int(first_multiple_input[4])
    dp = int(first_multiple_input[5])
    sqn = int(first_multiple_input[6])
    pld = int(first_multiple_input[7])
   
    ProtocolList = ["HTTPS","SMTP","UDP","TCP","DHCP","IRC"]
    IpBlackList = []
    #makes a list of packets
    pkt = makePacket(srcIP, dstIP, length, prt, sp, dp, sqn, pld)
    pk1 = makePacket("111.202.230.44","62.82.29.190",31,"HTTP",80,20,1562436,338)
    pk2 = makePacket("222.57.155.164","50.168.160.19",22,"UDP",790,5431,1662435,812)
    pk3 = makePacket("333.230.18.207","213.217.236.184",56,"IMCP",501,5643,1762434,3138)
    pk4 = makePacket("444.221.232.94","50.168.160.19",1003,"TCP",4657,4875,1962433,428)
    pk5 = makePacket("555.221.232.94","50.168.160.19",236,"HTTP",7753,5724,2062432,48)
   
    pkt_list = [pkt,pk1,pk2,pk3,pk4,pk5]
    print(calScore(pk4))

    #makes a list of packet info
    packet_List = [(srcIP, dstIP, length, prt, sp, dp, sqn, pld), ("111.202.230.44","62.82.29.190",31,"HTTP",80,20,1562436,338), ("222.57.155.164","50.168.160.19",22,"UDP",790,5431,1662435,812), ("333.230.18.207","213.217.236.184",56,"IMCP",501,5643,1762434,3138), ("444.221.232.94","50.168.160.19",1003,"TCP",4657,4875,1962433,428), ("555.221.232.94","50.168.160.19",236,"HTTP",7753,5724,2062432,48)]

   
    fptr.write('Forward Packets => ' + str(analysePackets(packet_List)) + '\n')
   
    fptr.close()
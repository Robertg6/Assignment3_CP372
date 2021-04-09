from common import *
from pickle import FALSE, TRUE
from startA3.common import RTPacket

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[999 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]

        # you implement the rest of constructor
        for i in range(num):
            self.distanceTable[ID][i] = costs[i]
            
        for i in range(num):
            self.distanceTable[i][i] = 0
            
        #send initial configuration of this node to others
        self.toNeighbors()
            
        

    def recvUpdate(self, pkt):
        
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        
        # you implement the rest of it  

        for i in range(self.ns.NUM_NODES):
            if (pkt.mincosts[i] < self.distanceTable[pkt.sourceid][i]):
                self.distanceTable[pkt.sourceid][i] = pkt.mincosts[i]
                
        #update all nodes using bellman ford algorithm
        

        #int x; // temp variable used to detect changes in nodeID row
        changed = FALSE


        for r in range(self.ns.NUM_NODES):
            for c in range(self.ns.NUM_NODES):

                x = self.distanceTable[r][c]    #initial value in table

                self.bellmanford(r, c)   #try to update it with the bellman ford algorithm

                if (x != self.dataTable[r][c]):  #if this has changed, and we are in row of current node, update changed boolean
                    changed = TRUE
                    
                
        for r in range(self.ns.NUM_NODES):
            for c in range(self.ns.NUM_NODES):


                if (self.distanceTable[r][c] < self.distanceTable[c][r]):    #because bi-directional consider diagonal reflection
                    self.distanceTable[c][r] = self.distanceTable[r][c]
                    changed = TRUE
                    
                if (self.distanceTable[c][r] < self.distanceTable[r][c]):   #now reverse
                    self.distanceTable[r][c] = self.distanceTable[c][r]
                    changed = TRUE
                    
                if (r == c):                  #if we send to self, cost is 0
                    if (self.distanceTable[r][c] != 0):
                        changed = TRUE
                        
                    self.distanceTable[r][c] = 0
                    

                    
            


            #only need to send to neighbors if we have updated shortest path
        if (changed):
            self.toNeighbors()
            
              
            return;
        
        
    def toNeighbors(self):

        
        
        #source ID = node you send from = this node ID
        #newpkt.sourceid = self.myID;

        #initialize data to row of this node ID
        #for i in range(self.num):
            #newpkt.mincosts[i] = self.distanceTable[self.myID][i]
            


        #send state to reachable neighbors
        for i in range(self.ns.NUM_NODES):
            if (i != self.myID and self.routes[i] < 999):  #don't send to self or unreachable nodes
                #newpkt.destid = i
                newpkt = RTPacket(self.myID, i, self.distanceTable[self.myID])
                self.ns.tolayer2(newpkt)
                
                
    def bellmanford(self, source, dest):
        costs = []

        for i in range(self.ns.NUM_NODES):
            costs[i] = self.distanceTable[source][i] + self.distanceTable[i][dest]
            
        calcMin = min(costs)

        if (calcMin < self.distanceTable[source][dest]):
            self.distanceTable[source][dest] = calcMin
            


        

    
    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print()
        

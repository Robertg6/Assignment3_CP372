from common import *
from pickle import FALSE, TRUE
from common import RTPacket

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[999 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]
        self.routes[self.myID] = self.myID

        # you implement the rest of constructor
        for i in range(num):
            self.distanceTable[ID][i] = costs[i]
            
        for i in range(num):
            for ii in range(num):
                if i != ii and self.distanceTable[i][ii] == 0:
                    self.distanceTable[i][ii] = 999
                elif i == ii:
                    self.distanceTable[i][ii] = 0
            
            
        self.toAdjacentNodes()
            
        

    def recvUpdate(self, pkt):
        
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        
        # you implement the rest of it  

        for i in range(self.ns.NUM_NODES):
            if (pkt.mincosts[i] < self.distanceTable[pkt.sourceid][i]):
                self.distanceTable[pkt.sourceid][i] = pkt.mincosts[i]

        changed = FALSE


        for r in range(self.ns.NUM_NODES):
            for c in range(self.ns.NUM_NODES):

                x = self.distanceTable[r][c]  

                self.bellmanford(r, c) 

                if (x != self.distanceTable[r][c]): 
                    changed = TRUE
                    
        
        for r in range(self.ns.NUM_NODES):
            for c in range(self.ns.NUM_NODES):


                if (self.distanceTable[r][c] < self.distanceTable[c][r]): 
                    self.distanceTable[c][r] = self.distanceTable[r][c]
                    changed = TRUE
                    
                elif (self.distanceTable[c][r] < self.distanceTable[r][c]): 
                    self.distanceTable[r][c] = self.distanceTable[c][r]
                    changed = TRUE
                    
                if (r == c):           
                    if (self.distanceTable[r][c] != 0):
                        changed = TRUE
                        
                    self.distanceTable[r][c] = 0
            
        if (changed == TRUE):
            
            for c in range(self.ns.NUM_NODES):
                dists = [0] * self.ns.NUM_NODES
                
                for r in range(self.ns.NUM_NODES):
                    if(c == r):
                        dists[r] = 999 
                    else:
                        dists[r] = self.distanceTable[r][c] 

                self.routes[c] = dists.index(min(dists)) 
                        
            self.routes[self.myID] = self.myID
            
            self.toAdjacentNodes()
        
    
        return;
        
        
    def toAdjacentNodes(self):

        for i in range(self.ns.NUM_NODES):
            if (i != self.myID and self.routes[i] < 999):
                newpkt = RTPacket(self.myID, i, self.distanceTable[self.myID])
                self.ns.tolayer2(newpkt)
                
                
    def bellmanford(self, source, dest):
        costs = []

        for i in range(self.ns.NUM_NODES):
            costs.append(self.distanceTable[source][i] + self.distanceTable[i][dest])
            
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

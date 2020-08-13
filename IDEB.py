#--------------------------------------------------------------------------------------------------------------------
                           #An improved dissipated energy based transmission protocol for wireless body area networks
                                                                  #IDEB
#--------------------------------------------------------------------------------------------------------------------
#A list of all the libraries used:
import math as ma
from csv import writer
#import numpy as np
#********************************************************************************************************************
#first i shall declare some universal variable values that are integral to thecalculation of dissipated energies etc.
dummy=pow(10,-9)
ETX=16.7*dummy#this is the energy dissipated on transmission of bit package
ERX=36.1*dummy#this is the energy consumed at the time of recieving of the bit package
EDA=5.0*dummy
Emp=1.97*dummy#this is the energy cnsumed at the time of bit amplification
lamb=0.125
c=299792458
d0=0.1
packets_to_CH=0
r=8000#the total  number of transmission cycles or rounds
node=8
flag=0
dead_node=0
packtosink=0
packtoforwarder=0
failed=0
primelist=[]
#*********************************************************************************************************************
#we shall first begin by creating a class for the wireless transmitting nodes
class node:
#constructor to each node to initialize with standard values
     def __init__(self,id,x,y,type):
         self.id=id
         self.E=0.5
         self.type=type
         self.statusflag=0
         self.x=x
         self.y=y
#now i shal define a function that updates the energy of each node after transmission is over in case the node is a a normal node
     def updating_in_case_normal(self):
        d=euclidean_distance(self,sinky)
        self.E=self.E-((ETX)*(4000) + Emp*3.38*4000*(ma.pow(d,3.38)))

     def updating_in_case_forwarder(self):
         d=euclidean_distance(self,sinky)
         self.E=self.E - ( (ETX+ERX+EDA)*(4000) + Emp*3.38*4000*(ma.pow(d,3.38)))
#now i shall create a class for the sink nodes
class sink:
    #constructor to initialize the sink
    def __init__(self):
        self.x=0.25
        self.y=0.1

#now i shall create a function to calculate the cost function in case of the simple protocol:
def calcffsimple(nody,sinky):
    distance=euclidean_distance(nody,sinky)
    ff=distance/nody.E
    return ff
#now i shall create a function to calculate the cost function in case of the E2 protocol:
def calcffE2(nody,sinky):
    distance=euclidean_distance(nody,sinky)
    if nody.E==0.5:
        ff=1/(distance*nody.E*nody.E)
    else:
        de=0.5-nody.E #dissipated energy
        ff=1/(distance*de*de)
    return ff
#now is shall create a function to calculate the forwarding function in case of IDEB protocol:
def calcffIDEB(nody,sinky):
    distance=ma.pow(euclidean_distance(nody,sinky),5)
    if nody.E==0.5:
        ff=1/(distance*ma.pow(nody.E,2))
    else:
        de=0.5-nody.E
        ff=1/(distance*ma.pow(de,2))
    return ff
#the function to calculate euclidian distance is given as follow:
def euclidean_distance(node1,node2):
    x1=node1.x
    x2=node2.x
    y1=node1.y
    y2=node2.y
    dist=ma.sqrt(ma.pow(x1+x2,2)+ma.pow(y1+y2,2))
    return dist

#now i shall define a function that finds the forwarder node
def find_forwarder(normal_node_list,sinky):
    ff_list=[]
    #fin=[]
    l=len(normal_node_list)
    for i in range(0,l):
        ff_list.append(calcffIDEB(normal_node_list[i],sinky))
    #req=sum(ff_list)
    #avg=req/l
    #for i in range(0,l):
        #fin.append(avg-ff_list[i])
    reqn=min(ff_list)
    for i in range(0,l):
        if reqn==ff_list[i]:
            index=i
    return normal_node_list[index]

#function to create and write onto a csv failed
def appendrow(list_of_elem):
    # Open file in append mode
    with open('idebforIDEB.csv','a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
#***************************************************************************************************************************
#now the main body of the code begins, I shall start by declaring and initializing all the nodes and thus establish the network
#the following is a loop to generate prime numbers in the specified range to generate failed delivery of packets simulation.
for num in range(2,5000):
    if all(num%i!=0 for i in range(2,num)):
        primelist.append(num)
x_list=[0.3,0.5,0.3,0.5,0.37,0.45,0.7,0.1]
y_list=[0.1,0.3,0.55,0.55,0.75,0.9,0.8,0.8]
type_list=[1,1,1,1,2,2,1,1]
id_list=[1,2,3,4,7,8,5,6]
node_list=[]
normal_node_list=[]
adv_node_list=[]
for i in range(0,8):
    new_node=node(id_list[i],x_list[i],y_list[i],type_list[i])
    node_list.append(new_node)
    if new_node.type==2:
        adv_node_list.append(new_node)
    else:
        normal_node_list.append(new_node)
#initialize the sink node:
sinky=sink()
for r in range(0,8000):
    writable_contents=[]
    total_residue=0
    len1=len(normal_node_list)
    len2=len(adv_node_list)
    for i in range(0,len1):
        try:
            if normal_node_list[i].E<=0:
                normal_node_list.remove(normal_node_list[i])
                dead_node=dead_node+1
        except:
            flg=0
        try:
            if adv_node_list[i].E<=0:
                adv_node_list.remove(adv_node_list[i])
                dead_node=dead_node+1
        except:
            continue
    for_norm=find_forwarder(normal_node_list,sinky)
    numnode=len(normal_node_list)
    for i in range(0,numnode):
        if for_norm.id!=normal_node_list[i].id:
            if flag in primelist:
                normal_node_list[i].updating_in_case_normal()
                failed=failed+1
                total_residue=total_residue+normal_node_list[i].E
                flag=flag+1
            else:
                normal_node_list[i].updating_in_case_normal()
                packtoforwarder=packtoforwarder+1
                total_residue=total_residue+normal_node_list[i].E
    for_norm.updating_in_case_forwarder()
    total_residue=total_residue+for_norm.E
    packtosink=packtosink+1
    try:
        num=len(adv_node_list)
        for i in range(0,num):
            adv_node_list[i].updating_in_case_normal()
            packtosink=packtosink+1
            total_residue=total_residue+adv_node_list[i].E
    except:
        continue
    writable_contents=[r,total_residue,dead_node,packtosink]
    appendrow(writable_contents)

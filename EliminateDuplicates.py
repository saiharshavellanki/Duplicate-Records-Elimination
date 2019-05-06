import math
import copy
import sys
import time

class Node:
	def __init__(self):
		self.Parent_index=-1
		self.Children={}
		self.Values=[]
   
root=Node()
Nodes=[]
count=0
Nodes.append(root)
Root_pos=0
t=2

def pos_search_left_value(val,lis):
	pos=-1
	for i in range(0,len(lis)):
		if val>lis[i]:
			pos=i
	return pos

def split(Current_node,Parent_index):
	global Root_pos
	global count
	if Current_node==Root_pos and len(Nodes[Current_node].Values)==2*t-1:
		Root=Nodes[Current_node]
		Left_Child=Node()
		Right_Child=Node()
		New_Root=Node()
		New_Root.Parent_index=-1
		Central_Value=Root.Values[t-1]
		Left_Child.Values=Root.Values[:t-1]
		Right_Child.Values=Root.Values[t:]
		New_Root.Values=Root.Values[t-1:t]

		for i in range(0,len(Left_Child.Values)):
			if Left_Child.Values[i] in Root.Children:
				Left_Child.Children[Left_Child.Values[i]]=Root.Children[Left_Child.Values[i]]

		if -1 in Root.Children:
			Left_Child.Children[-1]=Root.Children[-1]

		for i in range(0,len(Right_Child.Values)):
			if Right_Child.Values[i] in Root.Children:
				Right_Child.Children[Right_Child.Values[i]]=Root.Children[Right_Child.Values[i]]
		if Root.Values[t-1] in Root.Children:
			Right_Child.Children[-1]=Root.Children[Root.Values[t-1]]

		count+=2
		Left_Child.Parent_index=count
		Nodes[Root_pos]=copy.deepcopy(Left_Child)
		Nodes.append(Right_Child)
		Right_Child_pos=len(Nodes)-1
		Right_Child.Parent_index=count
		New_Root.Children[-1]=Root_pos
		New_Root.Children[Central_Value]=count-1
		Root_pos=count
		Nodes.append(New_Root)

		Current_node=Right_Child_pos
		for i in Nodes[Current_node].Children:
			Nodes[Nodes[Current_node].Children[i]].Parent_index=Right_Child_pos

	elif len(Nodes[Current_node].Values)==2*t-1:
		Root=Nodes[Current_node]
		Left_Child=Node()
		Right_Child=Node()
		Central_Value=Root.Values[t-1]
		Left_Child.Values=Root.Values[:t-1]
		Right_Child.Values=Root.Values[t:]
	
		for i in range(0,len(Left_Child.Values)):
			if Left_Child.Values[i] in Root.Children:
				Left_Child.Children[Left_Child.Values[i]]=Root.Children[Left_Child.Values[i]]

		if -1 in Root.Children:
			Left_Child.Children[-1]=Root.Children[-1]

		for i in range(0,len(Right_Child.Values)):
			if Right_Child.Values[i] in Root.Children:
				Right_Child.Children[Right_Child.Values[i]]=Root.Children[Right_Child.Values[i]]
		if Root.Values[t-1] in Root.Children:
			Right_Child.Children[-1]=Root.Children[Root.Values[t-1]]

		Left_Child.Parent_index=Nodes[Current_node].Parent_index
		Right_Child.Parent_index=Nodes[Current_node].Parent_index

		Nodes[Current_node]=Left_Child
		Nodes.append(Right_Child)
		Right_Child_pos=len(Nodes)-1
		count+=1
		prev_index=Current_node
		Current_node=Nodes[Current_node].Parent_index
		Position=pos_search_left_value(Central_Value,Nodes[Current_node].Values)
		lis=Nodes[Current_node].Values
		Nodes[Current_node].Values=lis[:Position+1]+[Central_Value]+lis[Position+1:]
		if Position==-1:
			Nodes[Current_node].Children[-1]=prev_index
		else:
			Nodes[Current_node].Children[Nodes[Current_node].Values[Position]]=prev_index
	
		Nodes[Current_node].Children[Nodes[Current_node].Values[Position+1]]=count
		Nodes[prev_index]=Left_Child
		for i in Nodes[Right_Child_pos].Children:
			Nodes[Nodes[Right_Child_pos].Children[i]].Parent_index=Right_Child_pos

		split(Current_node,Nodes[Current_node].Parent_index)

def insert(val):
	global Root_pos
	Current_node=search(val)
	if Current_node==-1:
		print "duplicate",val
		return
	f=0
	Position=pos_search_left_value(val,Nodes[Current_node].Values)
	lis=Nodes[Current_node].Values
	Nodes[Current_node].Values=lis[:Position+1]+[val]+lis[Position+1:]
	if len(Nodes[Current_node].Values)==2*t-1:
		f=1
	if f==1:
		split(Current_node,Nodes[Current_node].Parent_index)


def print_btree():
	for i in range(0,len(Nodes)):
		print i,"Parent is ",Nodes[i].Parent_index,Nodes[i].Values,Nodes[i].Children

def search(val):
	global Root_pos
	Current_node=Root_pos
	found_pos=-1
	while(len(Nodes[Current_node].Children))!=0:
		Position=pos_search_left_value(val,Nodes[Current_node].Values)
		if Position!=-1:
			Value=Nodes[Current_node].Values[Position]
		else:
			Value=-1
		if Position+1<len(Nodes[Current_node].Values) and  val == Nodes[Current_node].Values[Position+1]:
			found_pos=Current_node
			break
		Current_node=Nodes[Current_node].Children[Value]

	Position=pos_search_left_value(val,Nodes[Current_node].Values)
	if Position+1<len(Nodes[Current_node].Values) and  val == Nodes[Current_node].Values[Position+1]:
			found_pos=Current_node

	if found_pos!=-1:
		return -1
	else:
		return Current_node

hash_tree=set()

arguments=sys.argv
input_file=arguments[1]
no_of_records=int(arguments[2])
M=int(arguments[3])
n=int(arguments[4])
flag=int(arguments[5])

# print arguments

def search_hash(val):
	global hash_tree
	if val not in hash_tree:
		return 0
	else:
		return -1
def insert_hash(val):
	hash_tree.add(val)


def insert_ds(val):
	global flag
	if flag==0:
		insert(val)
	else:
		insert_hash(val)

def search_ds(val):
	global flag
	if flag==0:
		l=search(val)
		return l
	else:
		l=search_hash(val)
		return l

inp=[]
out=[]
start_time=time.time()
try:
	f = open(input_file, 'r')
except IOError:
	sys.stderr.write("No File for the Relation " + input_file+ " exists\n")
	sys.exit(-1)
for line in f:
	inp.append(line)
	if len(inp)==(M-1)*no_of_records:
		for i in range(0,len(inp)):
			fl=search_ds(inp[i])
			if fl!=-1:
				out.append(inp[i])
				insert_ds(inp[i])
			if len(out)==no_of_records:
				print out
				f1=open('output.txt','a+')
				for j in range(0,len(out)):
					f1.write(out[j])
				f1.close()
				out=[]
		inp=[]
f.close()
for i in range(0,len(inp)):
	fl=search_ds(inp[i])
	if fl!=-1:
		out.append(inp[i])
		insert_ds(inp[i])
	if len(out)==no_of_records:
		print out
		f1=open('output.txt','a+')
		for j in range(0,len(out)):
			f1.write(out[j])
		f1.close()
		out=[]
print out
for i in range(0,len(out)):
	f1=open('output.txt','a+')
	for j in range(0,len(out)):
		f1.write(out[j])
	f1.close()
# print time.time()-start_time

import random
import sys
import os
import math

#Netlist of Dr. Kalla's publication
top = [0,1,4,5,1,6,7,0,4,9,10,10]
bottom = [2,3,0,3,5,2,6,8,9,8,7,0] #[4, 2, 3, 4, 3, 6, 5, 8, 5, 9] are common
a = len(top)
b = len(bottom)
if a >= b:
   n=a
else:
   n=b

#mergedlist contains unique elements , combination of top and bottom
mergedlist = top + bottom
d = []
for i in mergedlist:
   if i != 0 and i not in d:
  	 d.append(i)
mergedlist = d
#number of unique cells
uc = len(mergedlist)
print 'number of cells to route',uc

#print 'mergedlist is', mergedlist
	 
###
common = [i for i in top if i in bottom]

#class of list to store left and right of a particular cell and stores what is above and below
class position:
   l=0
   r=0
   above=[]
   below=[]
   track=[]
cell = []    		 #empty list
for i in range (0,13):
   cell.append(position())
#finding leftmost occurance among common elements

for j in range (0,len(common)):
   for i in range (0,len(top)):
  	 if common[j] == top[i]:
  		 #print 'left of', common[j],'in top is',i
  		 p=i
  		 cell[common[j]].l = i
  		 break
   for i in range (0,len(bottom)):
  	 if common[j] == bottom[i]:
  		 #print 'left of', common[j],'in bottom is',i
  		 q=i
  		 cell[common[j]].l = i
  		 break
   if p<q:
  	 cell[common[j]].l = p

#finding leftmost occurance of onlytop and onlybottom elements
onlytop = [i for i in top if i not in bottom]
#print onlytop
onlybottom = [i for i in bottom if i not in top]
#print onlybottom

for j in range (0,len(onlytop)):
   for i in range (0,len(top)):
  	 if onlytop[j] == top[i]:
  		 #print 'left of', onlytop[j],'is',i
  		 cell[onlytop[j]].l = i
  		 break
for j in range (0,len(onlybottom)):
   for i in range (0,len(bottom)):
  	 if onlybottom[j] == bottom[i]:
  		 #print 'left of', onlybottom[j],'is',i
  		 cell[onlybottom[j]].l = i
  		 break

#finding rightmost occurance in common elements
for j in range (0,len(common)):
   for i in range (0,len(top)):
  	 if common[j] == top[-i-1]:
  		 #print 'right of', common[j],'in top is',len(top)-i-1
  		 p= len(top)-i-1
  		 break
   for i in range (0,len(bottom)):
  	 if common[j] == bottom[-i-1]:
  		 #print 'right of', common[j],'in bottom is',len(bottom)-i-1
  		 q=len(bottom)-i-1
  		 break
   if p<q or p==q:
  	 cell[common[j]].r = q
   else:
  	 cell[common[j]].r = p    
for j in range (0,len(onlytop)):
   for i in range (0,len(top)):
  	 if onlytop[j] == top[-i-1]:
  		 #print 'right of', onlytop[j],'is',len(top)-i-1
  		 cell[onlytop[j]].r = len(top)-i-1    
  		 break
for j in range (0,len(onlybottom)):
   for i in range (0,len(bottom)):
  	 if onlybottom[j] == bottom[-i-1]:
  		 #print 'right of', onlybottom[j],'is',len(bottom)-i-1
  		 cell[onlybottom[j]].r = len(bottom)-i-1
  		 break
cell[0].l = cell[0].r = -1

# finding left and right of all cells is completed before this step

column = []
for i in range (0,n):
   column.append([])
for i in range(0,n):
   for j in range (0,uc+1):
  	 if i >= cell[j].l and i <=  cell[j].r:
  		 column[i].append(j)  #j is cell number and i is column number

#removing duplicates
s = []
for i in column:
   if i not in s:
  	 s.append(i)
column = s
print 'S(col):',column
# function for maximum compatibles for
def subset(a,b):
   counter = 0
   for i in a:
  	 for j in b:
  		 if i == j:
  			 counter += 1
  			 break
   if counter == len(a):
  	 return True
   else:
  	 return False

zone = []
nozone = []
for i in range(0,len(column)) :
	for j in range(0,len(column)) :
		if i != j:
			if subset(column[i],column[j]) :
				nozone.append(column[i])
				break;

for i in column:
	if i not in nozone:
		zone.append(i)

print 'zone is ',zone   		
print 'number of zones:',len(zone)
# zone representation is done above this step
#finding set of zones in which a particular cell lies in

for i in range (0,n):  	#test range (1,n)
   cell[i].above = []
   cell[i].below = []
   cell[i].track = []
   cell[i].zone = []
for i in range (1,uc+1):
   for j in range (0,len(zone)):
  	 if i in zone[j]:
  		 cell[i].zone.append(j+1)
#for i in range (1,uc+1):
 #  print 'cell',i,'in zones',cell[i].zone
  	
# VCG generation starts here

for i in range (0,len(top)):
   if bottom[i] != 0:
  	 cell[top[i]].above.append(bottom[i])
for i in range (0,len(bottom)):
   if top[i] != 0:
  	 cell[bottom[i]].below.append(top[i])

# To start assignment from leftedge, store the appropriate order in this list named leftEdge.
leftEdge = [1,7,4,8,5,9,6,2,3,10]
'''
for i in range (0,n):
	if top[i] !=0 :
		leftEdge.append(top[i])
	if bottom[i] !=0:
		leftEdge.append(bottom[i])
#print leftEdge
#removing duplicates
s = []
for i in leftEdge:
   if i not in s:
  	 s.append(i)
leftEdge = s
#print 'leftedge order:',leftEdge
'''
#elements are stored in appropriate order to start routing from left edge.

# Track Assignment
t = 1
full = leftEdge[:]
assigned = []
for counter in range (0,uc):
	parentless = []
	for i in range (0,uc):    
  	 z = full[i]
  	 #leftEdge.remove(z)
  	 if cell[z].below == [] and z not in assigned:
  		 #add z to parentless
		 parentless.append(z)
		 #print 'parentless pins',parentless
	if len(parentless) == 0 :
		if(len(assigned) == len(full)) :
			break
		else :
			print 'Reached a deadlock'
#			print 'assigned is ', assigned
#			print 'full is ', full
			break
	selected = []
	selected.append(parentless[0])
	# selected[0]=parentless[0]
	
	#b= through 1 to length of parentless
	for j in range (1,len(parentless)):
		#if all elements of selected and b can be in same track = no same zone shared
		q = parentless[j]
		flag = 0
		for k in range(0,len(zone)):
			if q in zone[k]:
				for l in range(0,len(selected)):
					if selected[l] in zone[k]:
						flag = 1
					if flag == 1:
						break 
		if flag == 0:
				selected.append(q)			
			#add b to selected
	#add all ements of selected to assigned. remove
  	for i in range(0,len(selected)):
		assigned.append(selected[i])
	print 'track ', t, 'has nets', selected
#	print 'parentless is',parentless
	t+=1
	for i in range(0,len(selected)):
		p = cell[selected[i]].above
		for j in range(0,len(p)):
			if selected[i] in cell[p[j]].below :
				cell[p[j]].below.remove(selected[i])
print 'selecting pins from top left and bottom right, total tracks used',t-1


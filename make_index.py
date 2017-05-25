import os

fold = 'Reports/'

next = 'next.txt'

links = os.listdir(fold)

links.remove(next)
links.sort()
links.reverse()

head = open('Header/header.html', 'r')

f = open('index.md', 'w')

for line in head:
   f.write(line.replace('__ACTIVE_ADOP__', 'active'))

head.close()

f.write("[The next (unofficial) report](" + fold +  next + ") \n\n")
f.write("[The latest report](" + fold + links.pop(0) + ") \n\n")
f.write("The rest: \n\n")
for string in links:
   f.write("[" + string + "](" + fold + string + ") \n\n")
f.close()

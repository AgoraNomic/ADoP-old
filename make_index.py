import os

fold = 'Reports/'

next = 'next.txt'

links = os.listdir(fold)

links.remove(next)
links.sort()
links.reverse()

f = open('index.md', 'w')

f.write("[The next (unofficial) report](" + fold +  next + ") \n\n")
f.write("[The latest report](" + fold + links.pop(0) + ") \n\n")
f.write("The rest: \n\n")
for string in links:
   f.write("[" + string + "](" + fold + string + ") \n\n")

f.close()

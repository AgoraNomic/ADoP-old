import os

fold = 'Reports/'

next = 'next.txt'

links = os.listdir(fold)

links.remove(next)
links.sort()
links.reverse()

f = open('index.md', 'w')

f.write("#Office of the ADoP\n\n")
f.write("##Current\n\n")
f.write("[The next (unofficial) report](" + fold +  next + ") \n\n")
n = links.pop(0)
f.write("[The Latest](" + fold + n + ") (" + n + ")\n\n")
f.write("##Past\n\n")
for string in links:
   f.write("[" + string + "](" + fold + string + ") \n\n")

f.close()

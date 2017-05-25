import os

fold = 'Reports/'

next = 'next.txt'

links = os.listdir(fold)

links.remove(next)
links.sort()
links.reverse()

head = open('Header/header.html', 'r')

f = open('index.md', 'w')

f.write('<html> <body> \n')

f.write ('  <script src=\"https://code.jquery.com/jquery-3.2.1.min.js\" integrity=\"sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=\" crossorigin=\"anonymous\"></script> \n <!-- Latest compiled and minified CSS --> \n <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" crossorigin=\"anonymous\"> \n  <!-- Latest compiled and minified JavaScript --> \n <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\" integrity=\"sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa\" crossorigin=\"anonymous\"></script>')

for line in head:
   f.write(line.replace('__ACTIVE_ADOP__', 'active'))

head.close()

f.write("[The next (unofficial) report](" + fold +  next + ") \n\n")
f.write("[The latest report](" + fold + links.pop(0) + ") \n\n")
f.write("The rest: \n\n")
for string in links:
   f.write("[" + string + "](" + fold + string + ") \n\n")

f.write('</body> </html>')

f.close()

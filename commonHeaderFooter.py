"""
This is a script to make the head, header, and footer of every HTML file in this website the same, so that I don't have to do it manually.
I apologize for the messy code, I wrote it and tested it in about an hour, and it seems to work.
It does not run in the browser at all, it is just a tool to make working on the website less tedious on my end.

Run with: python3 commonHeaderFooter.py

"""
import os

files = os.popen("find . -type f").read().split("\n") # get a list of files with their paths. This is a Bash command, so you need at least WSL to make it work

f = open("index.html", "r") # open index.html, read its contents into a variable, close the file
indexStr = f.read()
f.close()

head = indexStr[(indexStr.find('<head>')+len('<head>')):indexStr.find('</head>')] # get the head of the index.html file
header = indexStr[(indexStr.find('<header>')+len('<header>')):indexStr.find('</header>')] # get the header section of the index.html file
footer = indexStr[(indexStr.find('<footer>')+len('<footer>')):indexStr.find('</footer>')] # get the footer section of the index.html file

for fs in files: # iterate through the files
	if fs[2:] != "index.html" and ".html" in fs: # check to make sure that the current file is an HTML file and that it is not index.html
		isInSubDir = '/' in fs[2:] # checks if the current file is in a sub directory
		f = open(fs[2:], "r") # opens the file, reads its contents into a variable, closes the file
		currFileStr = f.read()
		f.close()
		
		if isInSubDir == False: # the next few lines patch together the new HTML file from the headers and the old HTML file. If you don't like long lines of code, please avert your eyes
			newFileStr = currFileStr[:currFileStr.find('<head>')] + "<head>" + head + currFileStr[currFileStr.find('</head>'):currFileStr.find('<header>')] + "<header>" + header + currFileStr[currFileStr.find('</header>'):currFileStr.find('<footer>')] + "<footer>" + footer + currFileStr[currFileStr.find('</footer>'):]
		else: # add "../" to every file path in the header if it's in a subdirectory
			newFileStr = currFileStr[:currFileStr.find('<head>')] + "<head>" + head + currFileStr[currFileStr.find('</head>'):currFileStr.find('<header>')] + "<header>" + header.replace('href="', 'href="../') + currFileStr[currFileStr.find('</header>'):currFileStr.find('<footer>')] + "<footer>" + footer + currFileStr[currFileStr.find('</footer>'):]
		 
		f = open(fs[2:], "w") # can add .replace('.', '1.') to fs[2:] to make new files instead of overwriting the existing ones
		f.write(newFileStr) # open the old file, write the new HTML file to the old file, close the file
		f.close()
		
"""
Guides I referenced:
https://stackoverflow.com/questions/1767384/ls-command-how-can-i-get-a-recursive-full-path-listing-one-line-per-file
https://www.kite.com/python/answers/how-to-get-the-substring-between-two-markers-in-python
https://www.w3schools.com/python/python_file_write.asp
"""

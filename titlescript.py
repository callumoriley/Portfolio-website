import os

files = os.popen("find . -type f").read().split("\n")

for fs in files:
    if fs[2:] != "index.html" and ".html" in fs: # if the file is not the index file and the file is an HTML file
        f = open(fs[2:], "r") # get the page title
        htmlStr = f.read()
        pageTitle = htmlStr[htmlStr.find('<h3>')+4:htmlStr.find('</h3>')]
        f.close()

        htmlStr = htmlStr.replace("<title>Callum O'Riley</title>", "<title>Callum O'Riley | " + pageTitle + "</title>")

        f = open(fs[2:], "w")
        f.write(htmlStr)
        f.close()

"""
Mainly referenced commonHeaderFooter.py, but also referenced this site: https://www.w3schools.com/python/ref_string_replace.asp
"""
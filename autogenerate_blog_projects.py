import os
import re

directory = "posts/"
files = os.listdir(directory)
paths = [os.path.join(directory, file) for file in files]
print(paths)

page_titles = []
dates = []
for path in paths:
    with open(path, "r") as f:
        html_str = f.read()
    page_titles.append(html_str[html_str.find('<h3>')+4:html_str.find('</h3>')].replace("\n    ",""))
    if "<time>" in html_str:
        dates.append(html_str[html_str.find('<time>')+6:html_str.find('</time>')].replace("\n    ","")[1:])

print(page_titles)
print(dates)

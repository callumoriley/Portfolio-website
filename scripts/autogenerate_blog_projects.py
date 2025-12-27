import os
import re
from datetime import datetime

def parse_date_string(date_str):
    # Remove ordinal suffixes: st, nd, rd, th
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    dt = datetime.strptime(cleaned, "%B %d, %Y")

    return dt

def get_entry_str(date, title, path):
    path = path.replace("../","")
    
    string = f"""<a class=\"list-group-item list-group-item-action\" href=\"{path}\">
      {title}
      <div class=\"date\">
       {date}
      </div>
     </a>
     """

    return string

def get_entries(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files]
    #print(paths)

    page_titles = []
    dates = []
    for path in paths:
        with open(path, "r") as f:
            html_str = f.read()

        match = re.search(r"<h3>\s*(.*?)\s*</h3>", html_str, re.DOTALL)
        if match:
            page_titles.append(match.group(1).strip())

        if "<time>" in html_str:        
            match = re.search(r"<time>\s*(.*?)\s*</time>", html_str, re.DOTALL)
            if match:
                dates.append(match.group(1).strip())

    #print(page_titles)
    #print(dates)
    combined = zip([parse_date_string(date) for date in dates], dates, page_titles, paths)
    sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

    return sorted_combined

header = """<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport"/>
  <title>
   Callum O'Riley | Blog posts
  </title>
  <!-- Bootstrap core CSS -->
  <link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <style>
   .img-fluid {


                width: 500px;


                height: auto;


            }


            .jumbotron { /* Also like #16298a */


                background-color: #2a40b0!important;


            }


            .icon {


                width: 16px;


                height: 16px;


            }
  </style>
  <!-- Global site tag (gtag.js) - Google Analytics (for seeing how many people view the website) -->
  <script async="" src="https://www.googletagmanager.com/gtag/js?id=G-GLWJR8MLT4">
  </script>
  <script>
   window.dataLayer = window.dataLayer || [];


            function gtag(){dataLayer.push(arguments);}


            gtag('js', new Date());





            gtag('config', 'G-GLWJR8MLT4');
  </script>
  <script>
   if (document.title === "Callum O'Riley | Holy Land Pilgrimage") {


                window.location.href = "https://www.notion.so/callums-holy-land-odyssey/Callum-s-Holy-Land-Pilgrimage-ba5b4b66c2fb497f94b6a505e7ae05ab?pvs=4";


            }
  </script>
 </head>
 <body>
  <header>
   <div class="container">
    <div class="jumbotron text-white">
     <!-- Don't know if these colours will stay the same -->
     <h1 class="text-center">
      <b>
       Callum O'Riley
      </b>
     </h1>
    </div>
    <div class="btn-group d-flex" role="group">
     <a class="btn btn-dark w-100" href="index.html">
      Home
     </a>
     <a class="btn btn-dark w-100" href="projects.html">
      Projects
     </a>
     <a class="btn btn-dark w-100" href="blog.html">
      Blog
     </a>
     <!-- <a href="holy_land_pilgrimage.html" class="btn btn-dark w-100">Holy Land Pilgrimage</a> -->
    </div>
    <hr/>
   </div>
  </header>
  <main>
   <div class="container text-left">
    <h3>
     Blog posts
    </h3>
    <p>
     This is where I write about smaller projects that are in less of a polished or finished state than the projects in the "Projects" page. I also might write on some non-technical topics.
    </p>
    <br/>
    <div class="list-group">"""
footer = """</div>
   </div>
  </main>
  <footer>
   <div class="container text-left text-muted">
    <hr/>
    <p>
     © Callum O'Riley, 2025
    </p>
    <p>
     All images belong to their respective owners.
    </p>
    <img class="icon" src="https://github.githubassets.com/favicons/favicon.png"/>
    <a href="https://github.com/callumoriley">
     GitHub
    </a>
    <br/>
    <img class="icon" src="https://static.licdn.com/sc/h/413gphjmquu9edbn2negq413a"/>
    <a href="https://www.linkedin.com/in/callum-o-riley-35316320b/">
     LinkedIn
    </a>
    <p>
     📧 callumchristopheroriley (at) gmail (dot) com
    </p>
   </div>
  </footer>
 </body>
</html>"""



if __name__ == "__main__":
    directory = "../posts/"
    sorted_combined = get_entries(directory)
    for c in sorted_combined:
            print(c)

    output_string = ""
    for c in sorted_combined:
        output_string += get_entry_str(c[1], c[2], c[3])

    full_html = f"{header}\n{output_string}\n{footer}"

    with open("../blog.html", 'w', encoding='utf-8') as file:
        file.write(full_html)

    print("Done!")
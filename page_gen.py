import markdown
import argparse

def convert_markdown_to_html(md_file, html_file, header, footer):
    """
    Converts a markdown file to an HTML file with a given header and footer.
    
    :param md_file: Path to the input markdown file
    :param html_file: Path to the output HTML file
    :param header: HTML content to be added as a header
    :param footer: HTML content to be added as a footer
    """
    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            md_content = file.read()

        html_content = markdown.markdown(md_content)
        full_html = f"{header}\n{html_content}\n{footer}"
        
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(full_html)
        
        print(f"Conversion successful! HTML saved to {html_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
header_html = """<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<title>Callum O'Riley | Template</title>

		<!-- Bootstrap core CSS -->
		<link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet">
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
		<script async src="https://www.googletagmanager.com/gtag/js?id=G-GLWJR8MLT4"></script>
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
				<div class="jumbotron text-white"> <!-- Don't know if these colours will stay the same -->
					<h1 class="text-center"><b>Callum O'Riley</b></h1>	
				</div>
				<div class="btn-group d-flex" role="group">
					<a href="../index.html" class="btn btn-dark w-100">Home</a>	
					<a href="../projects.html" class="btn btn-dark w-100">Projects</a>
					<a href="../blog.html" class="btn btn-dark w-100">Blog</a>
					<!-- <a href="../holy_land_pilgrimage.html" class="btn btn-dark w-100">Holy Land Pilgrimage</a> -->
				</div>
				<hr>
			</div>
		</header>
		<main>
            <div class="container text-left">
				<h3>Insert Title Here</h3>
				<time>January 1st, 2025</time>
				<br><br>
			</div>
			<div class="container text-left">"""
footer_html = """</main>
		<footer>
			<div class="container text-left text-muted">
				<hr>
				<p>© Callum O'Riley, 2025</p>
				<p>All images belong to their respective owners.</p>
				<img src="https://github.githubassets.com/favicons/favicon.png" class="icon">&nbsp;&nbsp;<a href="https://github.com/callumoriley">GitHub</a><br>
				<img src="https://static.licdn.com/sc/h/413gphjmquu9edbn2negq413a" class="icon">&nbsp;&nbsp;<a href="https://www.linkedin.com/in/callum-o-riley-35316320b/">LinkedIn</a>
				<p>📧&nbsp;callumchristopheroriley (at) gmail (dot) com</p>
			</div>
		</footer>
	</body>

</html>"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Markdown file to an HTML file with a header and footer.")
    parser.add_argument("input", help="Path to the input markdown file")
    parser.add_argument("output", help="Path to the output HTML file")
    args = parser.parse_args()

    convert_markdown_to_html(args.input, args.output, header_html, footer_html)

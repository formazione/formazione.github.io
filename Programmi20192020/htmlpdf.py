# from txt to html
# install wkthtml
import os
import pdfkit

with open("text.txt") as file:
	with open ("text.html", "w") as output:
		file = file.read()
		file = file.replace("\n", "<br>")
		output.write(file)

#os.startfile("text.txt")
#os.startfile("text.html")
pdfkit.from_file("text.html", "output.pdf")

os.startfile("output.pdf")
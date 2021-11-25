import os

classe = [
        "Breglia",
        "Cammarano_D",
        "Cammarano_N",
        "Costantini",
        "Del Verme",
        "Esposito",
        "Fontana",
        "Garofalo",
        "Giordano",
        "Grimaldi",
        "Lista",
        "Malzone",
        "Mandia",
        "Musto",
        "Ruocco",
        "Santoro",
        "Scola_M",
        "SCOLA_V",

]

path = "collegamenti.html"
html = ""
for n in classe:
       html += f"<h2><a href='https://formazione.github.io/quiz5ae/{n}.html'>{n}</a></h2>"
with open(path, "w") as file:
       file.write(html)

os.system(path)


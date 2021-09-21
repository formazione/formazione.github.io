import os
from punti import *
 

def html():

       tot = {}
       for k in a:
              tot[k] = 0
       print(tot)
       print("creato diz tot")

       data = ""
       for k in a:
              print(k, a[k])
              for day in a[k]:
                     tot[k] += a[k][day]
              data += f"<td><b style=\"font-size:12\">{tot[k]}</b><td> {k}</td>"
              print("totale", tot[k])
              # this sorted makes the days in order
              for d in sorted(a[k]):
                     if a[k][d] > 0:
                          data += "<td><b style=\"font-size:8\">" + d + "</b><br><center>" + str(a[k][d]) + "</center></td>"
                     else:
                          data += "<td></td>"
                     # data += "<td>" + d + " : " + str(a[k][d]) + "</td>"
              data += "<tr>"
       data = "<style>body{background:gray;color:white}</style><table border=1>" + data + "<table>"
       return data, tot
# print(data)

#===================================
count_lesson = 0
def add_data(frase):
       global data, count_lesson

       count_lesson += 1
       data += "<p>" + str(count_lesson) + ". " + frase + "</p>"



def h3(text):
       """Usa per create un titolo h3"""
       global data
       data += "<p><h3>" + text + "</h3></p>"



data, tot = html()

count_lesson = 0
h3("Lezioni")
# ====== ADD LESSONS HERE ===================
add_data("18.9 Correzione test d'ingresso ")


# ============ CREATE HTML FILE FOR INTERNET =====
def create_file():
       with open("5ae.html", "w") as file:
              file.write(data)
       os.startfile("5ae.html")

create_file()
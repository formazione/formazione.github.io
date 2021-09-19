import os
 
# a = {

# "Mandia" : ["18.9 : 7",
#             "20.9 : 0"],

# "Malzone" : ["18.9 : 2",
#              "20.9 : 0"],

# "Musto" : ["18.9 : 1",
#            "20.9 : 0"]
# }

a = {
"Breglia" : {"18.9" : 0,
       "20.9" :  0},
"Brunone" : {"18.9" : 0,
       "20.9" :  0},
"Cammarano D" : {"18.9" : 0,
       "20.9" :  0},
"Cammarano N" : {"18.9" : 0,
       "20.9" :  0},
"Costantini" : {"18.9" : 0,
       "20.9" :  0},
"Del Verme" : {"18.9" : 0,
       "20.9" :  0},
"Esposito" : {"18.9" : 0,
       "20.9" :  0},
"Fontana" : {"18.9" : 0,
       "20.9" :  0},
"Garofalo" : {"18.9" : 0,
       "20.9" :  0},
"Giordano" : {"18.9" : 0,
       "20.9" :  0},
"Grimaldi" : {"18.9" : 0,
       "20.9" :  0},
"Lista" : {"18.9" : 0,
       "20.9" :  0},
"Malzone" : {"18.9" : 2,
             "20.9" : 0},
"Mandia" : {"18.9" : 7,
            "20.9" :  0},
"Marchesani" : {"18.9" : 0,
            "20.9" :  0},
"Musto" : {"18.9" : 1,
           "20.9" : 0},
"Ruocco" : {"18.9" : 0,
            "20.9" :  0},
"Santoro" : {"18.9" : 0,
"20.9" :  0},
"Scola M" : {"18.9" : 0,
"20.9" :  0},
"Scola V" : {"18.9" : 0,
"20.9" :  0},
}


def day(dd):
       for k in a:
              a[k][dd] = 0
# ===================== 20.9
day("20.9")
# a["Mandia"]["20.9"] = 5
 



data = ""
tot = {}
for k in a:
       tot[k] = 0
print(tot)
print("creato diz tot")
for k in a:
       data += "<td>" + k + "</td>"
       print(k, a[k])
       for day in a[k]:
              tot[k] += a[k][day]
       print("totale", tot[k])
       for d in a[k]:
              if a[k][d] > 0:
                   data += "<td><b style=\"font-size:8\">" + d + "</b><br><center>" + str(a[k][d]) + "</center></td>"
              else:
                   data += "<td style=\"color:red;background:black\"><i style=\"font-size:8\">" + d + "</i><br><center></center></b></td>"
              # data += "<td>" + d + " : " + str(a[k][d]) + "</td>"
       data += "<tr>"
data = "<table border=1>" + data + "<table>"
# print(data)

count_lesson = 0
def add_data(frase):
       global data, count_lesson

       count_lesson += 1
       data += "<p>" + str(count_lesson) + ". " + frase + "</p>"


add_data("18.9 Correzione test d'ingresso ")

def create_file():
       with open("5ae.html", "w") as file:
              file.write(data)
       os.startfile("5ae.html")

# create_file()
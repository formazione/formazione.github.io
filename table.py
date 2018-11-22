from random import randrange
from creafile import creafile


def wrap(x, tag):
    "Wraps in <td> tag the x"
    tag1 = tag
    if tag == "table":
        tag1 = "table border=1"
    return f"<{tag1}>{x}</{tag}>"


def p(x):
    return randrange(x, x + 1000, 100)


def split(tab):
    for n, row in enumerate(tab):
        tab[n] = row.split(",")
    return tab


def table(tab):
    html = ''  # contain html
    for n, x in enumerate(tab):
        for a in x:
            html += wrap(a, "td")
        html += "<tr>"
    html = wrap(html, "table")
    return html


t1 = p(20000000)  # presenze ita
t2 = p(20000000)  # pres. stra
t3 = p(5000000)     # arrivi ita
t4 = p(6000000)     # arrivi stra
t5 = p(500000)  # posti
t6 = p(22000)   # km
t7 = 3750511    # abitanti

e1 = p(20000000)  # presenze ita
e2 = p(9000000)  # pres. stra
e3 = p(6000000)     # arrivi ita
e4 = p(2000000)     # arrivi stra
e5 = p(400000)  # posti
e6 = p(22000)   # km
e7 = 4446354    # abitanti

tab = split(f""",Toscana, Emilia Romagna
Presenze di turisti italiani,{t1}, {e1}
Presenze di turisti stranieri,{t2}, {e2}
Arrivi di turisti italiani,{t3}, {e3}
Arrivi di turisti stranieri,{t4}, {e4}
Posti letto, {t5}, {e5}
Sup. in Km quadrati, {t6}, {e6}
Popolazione, {t7}, {e7}
""".splitlines())

tab2 = split(f"""
Risultati, Toscana, Emilia Romagna
Permanenza media,{round((t1 + t2) / (t3 + t4),2)}, {round((e1 + e2) / (e3 + e4),2)}
""".splitlines())


print(table(tab))
creafile("prova_table.html", table(tab) + table(tab2))

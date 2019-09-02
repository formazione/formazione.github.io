let tabella1 = `
  Servizio	bassa	media	alta	prezzo	bassa	media	alta	Totale
menu	12480	9360	14040	50	624000	468000	702000	1794000
Banchetti	1320	1320	1980	120	158400	158400	237600	554400`.split("\n")
  
  document.write("<table>");
  for (row in tabella1){
    document.write("<tr>");
    for cell in row.split(" ") document.write("<td>" + cell + "</td>");
    document.write("</tr>");
   // ogni row ha una serie di dati separati da uno spazio
  };
  document.write("<table>");
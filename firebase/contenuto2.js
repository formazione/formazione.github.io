/// inserisci alla fine ###" + s per immagini, feedback e client diversi (pagine con schemi diversi)

let s = "https://quinta.glitch.me/firebase/client_standard.html";

// ......................... FUNZIONI PER FORMATTARE IL TESTO ....................

function img(im){ return "<br><img src=" + im + " width=200px /><br>";}
function ul(testo){
 // unordered list wrapper for string divided by '.'
  testo = "<ul><li>" + testo.replace(/\./g,"<li>") + "</ul>";
  return testo;
}

// ogni chiave è il titolo di una pagina web, il valore è il testo (body/slide) che
// viene inviata al client (dal file server.html)
// si può utilizzare per creare un ebook sul programma di 5a
let contenuto = {
  
    "Costituzione dell’impresa" : 
  
  "Le imprese ristorative sono imprese commerciali che per costituirsi devono iscriversi nel Registro delle imprese presso la Camera di Commercio Industria Artigianato e Agricoltura inviando in via telematica la Comunicazione Unica d'impresa (ComUnica)."+ 
    // comunica - Per aggiungere un immagine, passsa l'indirizzo alla funzione img
  img("https://www.emsm.it/s/cc_images/cache_2467890977.jpg") +
  "Questa verrà inoltrata all'INAIL per la posizione assicurativa, all'INPS per i contributi e all'Agenzia delle entrate per avere il numero di Partita IVA."+
  "Con la ComUnica si invia anche la SCIA (Segnalazione certificata di inizio attività) al SUAP (Servizio unico delle attività produttive) in cui si devono autocertificare<li> requisiti personali (maggiore età e assolvimento obblighi scolastici),<ul><li> morali (non avere condanne penali e non esser falliti) e<li> professionali (diploma alberghiero o 2 anni di esperienza nell'esercizio della somministrazione di alimenti e bevande)</ul>. Se il Comune non comunica nulla entro 60 giorni, per la regola del silenzio - assenso, la nuova attività si intende in regola." +
  // Immagine comUnica
  "#http://downloadcomunica.infocamere.it/comunica_webinstaller/comunica/LogoComunicaImpresa.png"+
  "##" +s,
  /*
  "Le imprese ristorative sono imprese commerciali. Per costituirle bisogna inviare per via telematica al Registro delle imprese, presso la CCIAA, Camera di Commercio Industria Artigianato e Agricoltura, della provincia di appartenenza la Comunicazione Unica d'impresa per l'iscrizione della nuova azienda. La Camera di Commercio la invia all'Agenzia delle Entrate (numero di partita IVA), all'INAIL (posizione assicurativa), INPS (contributi sociali). Bisogna trasmettere la SCIA (Segnalazione certificata di inizio attività) al SUAP (Servizio unico per le attività produttive) con l'autocertificazione dei requisiti personali (maggiore età, assolvimento obblighi scolastici) e morali (non aver riportato condanne penali o esser stato dichiarato fallito). Per la somministrazione di alimenti e bevande occorrono anche i requisiti professionali (diploma di istituto alberghiero o equivalente, frequenza  di corsi professionali regionali o almeno 2 anni di esperienze lavorative nel quinquennio precedente). Il fabbricato dove si eroga il servizio deve essere conforme alle norme di pubblica sicurezza e prevenzione incendi (CPI, certificato di prevenzione incendi). Il Comune, entro 60 giorni dal ricevimento della SCIA, deve accertare la veridicità dei requisiti dichiarati. Vale il principio del silenzio-assenso se entro 60 giorni non viene ricevuta alcuna comunicazione, la nuova attività è in regola.###" + s,
*/

"Sicurezza 1" : "Per sicurezza sul lavoro si intende il poter lavorare in un ambiente e in condizioni con rischi ridotti al minimo di infortunio e di malattie professionali. Devono essere resi sicuri il luogo di lavoro, l'attrezzatura e il corpo del lavoratore. Il Testo unico, d.lgs. 81/2008, si applica a tutti i settori di attività pubblici e privati, e a tutti i lavoratori. Vengono esclusi solo i lavori domestici e familiari." +
  "###" + s,
  
  "Sicurezza 3 - Responsabilità del datore di lavoro":
  "Il datore di lavoro è il principale responsabile della sicurezza del luogo di lavoro, deve monitorare i rischi presenti in azienda###" + s,
  
  "Document di valutazione dei rischi":
  "Il datore di lavoro redige il documento di valutazione dei rischi che indica le misure di prevenzione e protezione attuate, dei dispositivi di protezione adottati e il programma dei provvedimenti ritenuti opportuni. Le imprese con meno di 10 dipendenti possono redigere un documento semplificato.###"+s,
  
  "Servizio di protezione":
  "Dopo aver valutato i rischi deve organizzare un servizio di prevenzione e protezione, nominare un responsabile del servizio (datore di lavoro, dipendente o altri con le competenze necessarie) e un medico competente che collabori alla stesura del documento di valutazione dei rischi." +
  "###" +
  s,
  
  "Sicurezza 5 - Responsabilità dei lavoratori":
  "I lavoratori osservano le disposizioni del datore di lavoro, partecipano a corsi di formazione sulla sicurezza e nominano il proprio rappresentante per la sicurezza." +
  "###" +
  s,
  
  
  "Sicurezza 6 - Conformità dei luoghi di lavoro":
  ul("I luoghi di lavoro devono essere conformi alla normativa in materia di sicurezza. Gli edifici devono essere stabili e sottoposti a manutenzione periodica. Devono essere presenti vie e uscite di emergenza. I luoghi di lavoro devono essere sufficientemente illuminati e areati. Le temperature devono essere adeguate all'organismo umano, i pavimenti devono essere antiscivolo, non presentare buche o piani inclinati. Le porte devono consentire alle persone un'uscita rapida e devono essere facilmente apribili dall'interno. Le scale devono avere un parapetto e devono resistere alle massime condizioni di affollamento in situazioni di emergenza. I locali devono essere puliti e con superfici facilmente pulibili. Nelle immediate vicinanze dei locali di lavoro non possono essere presenti immondizie o rifiuti che possano produrre emanazioni insalubri. I lavoratori devono disporre di gabinetti e lavabi con acqua corrente. La pulizia è a carico del datore di lavoro. Le attrezzature devono essere dotate di marcatura CE") + 
     "###" + s,
  
  "Normativa antincendio": "La normativa antincendio si occupa di prevenire gli incendi e di tutelare l'incolumità delle persone in caso di incendio. Il datore di lavoro deve redigere un piano di emergenza nel quale siano descritte le misure da applicare in caso di incendio, valutando i rischi in azienda. In base a questi il datore di lavoro adotta le misure ritenute necessarie, come la messa a terra degli impianti elettrici, la ventilazione degli ambienti, informazione e formazione dei lavoratori. Il decreto ministeriale 9 aprile 1994 detta le regole tecniche per prevenire gli incendi nelle strutture ricettive. I fabbricati devono essere resistenti al fuoco, le strutture ricettive con più di 25 posti letto devono richiedere ai Vigili del fuoco il Certificato di prevenzione incendi (CPI). Tutte le strutture devono esporre la planimetria dell'albergo nei corridoi e nelle camere, indicando la posizione di chi legge e la via di fuga da seguire per accedere all'uscita di emergenza, segnalate anche da frecce direzionali e indicazioni luminose. Tutte le attività ricettive devono essere dotate di sistemi d'allarme, estintori, idranti, rilevatori di fumo, di fiamma e di gas.###" + s,
  
  "Norme di igiene alimentare":
 "La normativa alimentare e disciplina la produzione, il confezionamento, trasporto, conservazione, vendita e somministrazione degli alimenti. La disposizione legislativa di riferimento è il decreto legislativo 193 del 2007 con il quale sono entrati in vigore i regolamenti comunitari del cosiddetto 'pacchetto igiene'. Si basa sui seguenti principi: responsabilità diretta del soggetto che opera nella catena agro-alimentare, dalla produzione, alla conservazione e distribuzione; controlli lungo tutta la filiera agro-alimentare da parte di soggetti esterni autorizzati, ma anche da parte dello stesso operatore con l'adozione di sistemi di analisi del rischio per ridurre o eliminare i pericoli di contaminazione degli alimenti (sistemi HACCP); rintracciabilità e tracciabilità dei prodotti alimentari, cioè l'adozione di un sistema di raccolta e gestione delle informazioni che permetta in ogni momento di individuare il percorso degli alimenti, dalla produzione alla distribuzione, in modo che il sistema sia in grado di localizzare e ritirare dal mercato in modo rapidissimo i prodotti che risultino pericolosi per la salute dei consumatori.###" + s,
  
  "Sistema Haccp":
  "Hazard analysis an critical control point: protocollo per individuare e prevenire eventuali criticità nella produzione, trasformazione, confezionamento, distribuzione, conservazione, vendita e somministrazione degli alimenti, che potrebbero alterzare la loro salubrità. Si basa sull'attento monitoraggio dei punti critici della lavorazione degli alimenti, potenzialmente idonei a provocare la contaminazione degli stessi.###" + s, 
  
  "Informazioni garantite dall'etichettatura": "L'etichettatura fornisce al consumatore le informazioni adeguate sul prodotto per garantirne la sicurezza e facilitarne l'utilizzo. Le etichette, in base alla normativa italiana che ha recepito il Regolamento UE 1169/2001, devono  contenere una dichiarazione nutrizionale riferita a 100 g /100 ml dell'alimento con il valore energetico e il contenuto in grassi, carboidrati, proteine e sali, lo stato fisico del prodotto (congelato o decongelati), l'elenco degli ingredienti che compongono il prodotto in ordine decrescente di peso, gli allergeni (sostanze che possono risultare allergiche per alcuni consumatori, ad es. il glutine), la data di scadenza, le condizioni di conservazione, le modalità di utilizzo dell'alimento e il Pese di origine e il luogo di provenienza dell'alimento.###" + s,
  
 "Definizione delle Norme volontarie ISo 9000":
"Sono un sistema di qualità totale (total quality management o TQM) che le imprese possono adottare, in cui in tutti i processi ricerca la completa soddisfazione degli stakeholders aziendali (soci, dipendenti, finanziatori, fornitori e clienti)###" + s,
  
  "Trattamento dei dati personali":
  "Le imprese ristorative vengono in possesso di dati a###" + s,
  
  "contratti": "Il contratto è l'accordo di due o più parti per costituire, regolare o estinguere tra loro un rapporto giuridico di natura patrimoniale (art. 1321 c.c.)###" + s,
  
  "Gli elementi essenziali del contratto":
  "Accordo (volontà di due o più parti di dar vita a un rapporto patrimoniale), oggetto (il bene o la prestazione), causa (il motivo che giustifica il contratto, ad es. la causa di un mutuo è quella di ottenere un finanziamento) e forma (verbale, scritta o per fatti concludenti)###" + s,
  
  "contratto di ristorazione": "Con il contratto di ristorazione una parte, il ristoratore, si impegna a fornire la somministrazione di pasti e bevande dietro pagamento di un prezzo. È un contratto bilaterale, consensuale, a titolo oneroso, a prestazioni corrispettive.###" + s,
  
  "Il codice del consumo":
  "È una legge, decreto legislativo 206/2005, finalizzata a proteggere i consumatori, fornendo loro una serie di garanzie a tutela dei loro diritti. Tutela i consumatori anche nei confronti dei ristoratori, che hanno l'obbligo di consegnare agli stessi beni conformi a quanto stabilito dal contratto.###" + s,
  
  "contratto di catering": "Con il contratto di catering, il caterer si impegna a fornire la somministrazione di pasti e bevande all'altra parte, cliente, in modo continuativo o occasionale dietro pagamento di un prezzo.###" + s,
  
  "contratto di banqueting": "Con il contratto di banqueting una parte si impegna a fornire a un'altra parte un servizio di ristorazione effettuato tramite l'organizzazione di banchetti di qualità dietro pagamento di un prezzo.###" + s,
  
  
  //                        IL   MARCHIO    - ULTIMO MODULO
  
  "Il marchio": "Il marchio è ciò che distingue l'impresa dai suoi concorrenti (simbolo grafico, testo, suono). Giuridicamente è un segno che identifica impresa e prodotti in modo univoco. È un segno distintivo come la ditta e l'insegna.###" + s,
  
  "Registrazione del marchio":
  "Il marchio è protetto se viene registrato all'UIBM (Ufficio Italiano Brevetti e Marchi) per la tutela a livello nazionale o presso l'UAMI (Ufficio per l'Armonizzazione del Mercato Interno) per la tutela a livello comunitario.###"+s,
  
  "Marchi individuali e collettivi":
  "I marchi individuali  distinguono i prodotti di una singola impresa, i marchi collettivi sono utilizzati da più imprese che rispettano gli standard qualitativi stabiliti da un organismo di controllo che concede l'utilizzo del marchio, garantendo l'origine e la qualità dei prodotti ed effettuando i relativi controlli.###"+s,
  
  "Marchi di qualità alimentare":
  "Sono una particolare categoria di marchi collettivi. I requisiti del prodotto su cui si appone il marchio sono stabiliti dalla normativa nazionale o comunitaria e i controlli sono effettuati da organi pubblici. Vi rientrano i marchi DOP, IGP ecc. disciplinati dal Regolamento CE 510/2006###"+s,
  
  "Procedura per l'attribuzione: presentazione della domanda":
  "Le associazioni dei produttori presentano una domanda di attribuzione del marchio all'autorità compentente del proprio Stato.###"+s,
  
  "Parere dello Stato":
  "Se lo Stato esprime un parere favorevole, trasmette la domanda alla Commissione europea, allegando un disciplinare di produzione in cui sono indicate: caratteristiche, legame col territorio, materie prime e meto di lavorazione del prodotto.###"+s,
  
  "La Commissione":
"Quando la Commissione attribuiscec il marchio, lo Stato individua gli organismi di controllo.###"+s,
  
  "Elemento territoriale":
  "È l'elemento fondamentale e si riferisce all'insieme di elementi ambientali e umani che sono esclusivi di una zona ben delimitata, Il territorio è il luogo di produzione (Regione###"+s,
  
  "Dop":
  "Denominazione di Origine Protetta. si attribuisce ai prodotti alimentari e agricoli originari di un territorio la cui qualità dipende da elementi ambientali e umani legati al territorio in cui si eseguono tutte le fasi di lavorazione.###"+s,
  
  "Esempi di marchi DOP":
  "Asiago, Parmigiano Reggiano, Taleggio, Ricotta di Bufala campana, Pecorino romano.###"+s,
  
  "IGP":
  "Indicazione geografica protetta si attribuisce a quei prodotti alimentari e agricoli originari di un territorio la cui qualità dipende da elementi ambientali ed umani legati al territorio nel quale si esegue almeno una parte della lavorazione. A differenza del DOP, quindi, non si eseguono tutte le fasi nel territorio di origine.###"+s,
  
  "Esempi di marchi IGP":
  "Speck dell'Alto Adige, Lardo di colonnata, Arancia Rossa di Sicilia.###"+s,
  
  "STG":
  "Specialità tradizionale garantita: si attribuisce a prodotti alimentari e agricoli collegati a un territorio nel quale si esegue almeno una fase di lavorazione, ma che vengono prodotti anche in altri territori. In questo caso, quindi, non c'è una esclusività del prodotto come nell'IGP.###"+s,
  
  "Esempi di STG":
  "Pizza napoletana###"+s,
  
  "BIO":
  "Produzione biologica: attribuita a prodotti realizzati con un sistema di produzione sostenibile per l'agricoltura.###"+s,
  
  "I vini":
  "In Italia esistono altri tipi di certificazione che riguardano i vini. I vini da tavola non seguono un disciplinare, cosa che invece fanno i vini DOC, DOCG e IGT.###"+s,
  
  "DOC":
  "Denominazione di origine controllata: vini di qualità pordotti in zone delimitate di piccole e medie dimensioni.###"+s,
  
  "DOCG":
  "Denominazione di Origine Controllata e Garantita: vini di particolare pregio di qualità riconosciuta sottoposti a rigidi controlli. Sono vini DOCG il Brunello di Montalcino, e il Chianti classico."+
  "###"+s,

  "IGT":
  "Indicazione geografica tipica: attribuito a quei vini di qualità prodotti in ambiti territoriali meno ristretti e sottoposti a disciplinari meno rigidi.###"+s,
  
}





/*

Ufficio brevetti italiano:
UIBM
AIMA


*/


// alt + 0146 ’
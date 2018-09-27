# 0

Quella che sto per presentarvi è una descrizione *estremamente sintetica* del mio lavoro di analisi che ha avuto come oggetto dei dati relativi ad *alcuni aspetti* del CdL triennale in informatica.

Una parte principale di questa analisi è stata, come vedremo, l'attività di *data mining*.

# 1

Come suggerisce la metafora implicita nel nome, fare data mining significa estrarre delle informazioni preziose - quindi, utili - da una grande mole di dati grezzi.

Il procedimento seguito è, banalmente, quello illustrato dalla slide: si è data una *struttura* ai dati iniziali, rendendoli adatti ad essere dati in input a un *software* che implementa vari algorimi di data mining, per poi disporne l'output in modo da favorirne l'interpretazione.

Per realizzare tutto questo, c'è stato bisogno *principalmente* di tre strumenti software:

- *data base* per manipolare agilmente i dati e dargli la forma che serve;
- libreria di implementazioni degli algoritmi di data mining;
- strumenti per la *visualizzazione* di dati;

# 2

Per le operazioni di *pre processing* ho scelto MongoDB, un data base *non* relazionale che modella i dati in documenti strutturati secondo la Java Script Object Notation. Si tratta di una tecnologia *relativamente nuova* ma *sufficientemente matura*, ed ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

Per l'utilizzo degli algoritmi di data mining la scelta è ricaduta su Weka, uno strumento che ho già usato nel corso di Data Mining and Orgnaization e che, nonostante alcuni difetti, è risultato adeguato a questo scopo.

Infine, per realizzare il *post processing* ho impiegato vari strumenti, privilegiando però l'immediatezza d'uso dei semplici fogli di calcolo rispetto a uno strumento complesso come il linguaggio R.

# 3

Andiamo ora a vedere il materiale grezzo a disposizione. Abbiamo a che fare con due gruppi di dati: uno relativo agli *studenti*, l'altro agli *insegnamenti*.

Riguardo agli *studenti*, per coloro immatricolati dal 2010 al 2013, abbiamo dei record *anonimi* riguardo alla loro carriera accademica lungo *quattro anni* - ovvero, per ogni esame, la data in cui è stato superato e il voto conseguito, oltre ad altri attributi generici come ad esempio il punteggio raggiunto al test di ingresso.

Come si vede dal grafico, i dati degli studenti coprono *non uniformemente* il periodo che va dal 2010 al 2017. Quindi, relativamente a questo lasso di tempo, sono state prese in considerazione le risposte date dagli studenti ai *questionari di valutazione degli insegnamenti*, ovviamente in forma aggregata rispetto ai quesiti per preservare l'anonimato di chi ha espresso le valutazioni.

# 4, 5

Che abbiamo fatto con questi dati? Innanzitutto, li abbiamo studiati nella loro forma iniziale usando varie tecniche di visualizzazione, per capire quali informazioni possono esserne estratte.

Ad esempio, producendo dei grafici di dispersione riguardo al dataset della *carriera degli studenti*, si potrebbe *speculare* che ci sia una correlazione diretta fra il *punteggio del test di ingresso* - sulle ascisse - e il *voto medio* ottenuto negli esami - sulle ordinate.

Un altro esempio, sempre riguardante i dati degli studenti, può essere questo: una matrice che mostra l'andamento dello *scarto quadratico medio* dei voti ottenuti dagli studenti - le righe - negli *esami del primo anno* - le colonne. Si può notare, ad esempio, come alcuni gruppi di studenti abbiano preso un voto inferiore alla media in ogni esame, così come si può vedere che in alcuni esami i voti tendono a discostarsi meno dalla loro media.

# 6

Vediamo subito l'utilizzo di una tecnica di data mining sui soli dati degli studenti.  (seq)
...

# prepr

Per entrare nel vivo dell'analisi e utilizzare finalmente delle tecniche di data mining, occorre preparare i dati adeguatamente.

Visto che i due dataset a mia disposizione hanno un elemento in comune - il corso di insegnamento - un'idea ovvia è stata quella di effettuare un'operazione di *join* fra di essi. Il procedimento per realizzare il join è stato quello che ho brevemente riassunto nella slide: ho scartato qualche *outlier* e ho aggregato le istanze degli studenti rispetto ai *corsi d'esame* di ogni anno - condensando quelle informazioni in attributi come ad esempio la media dei voti, o il ritardo con cui è stato superato quell'esame. Fatto questo, le chiavi primarie hanno combaciato, e ho potuto ricavare...

...questo dataset facendo semplicemente un *inner join* fra i due che avevo a disposizione. Da questa struttura, poi, tramite altre operazioni di *preprocessing*, ho reso i dati adatti ad essere usati come input per gli algoritmi di data mining che adesso, finalmente, vedremo.

# 8


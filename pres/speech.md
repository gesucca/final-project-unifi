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

Riguardo agli *studenti*, per coloro immatricolati dal 2010 al 2013, abbiamo dei record anonimi riguardanti la carriera accademica lungo *quattro anni* - ovvero, per ogni esame, la data in cui è stato superato e il voto conseguito, oltre ad altri attributi generici come ad esempio il punteggio raggiunto al test di ingresso.

...
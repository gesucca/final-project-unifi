# 0 - Introduzione

> Quella che vi sto per presentare è una descrizione dell'analisi che ho fatto su alcuni dati dati relativi a *qualche aspetto* del Corso di Laurea triennale in informatica.

> Una parte principale di questa analisi è stata, come vedremo, l'attività di **data mining**.

# 1 - Data Mining

> Come suggerisce la metafora nel nome

**data mining** = estrarre informazioni *preziose* (**utili**) - da una grande mole di dati grezzi.

Procedimento:

- **pre processing** - rendere i dati adatti...
- > ...ad essere usati come input per gli **algorimi di data mining** che si desidera utilizzare
- **post processing** infine si dispone l'output in modo da favorirne l'interpretazione.

Ho avuto bisogno *principalmente* di *tre* strumenti software:

- **data base**
- libreria di **implementazioni di algoritmi per il data mining**
- software per tecniche di **visualizzazione**

> Andiamo a vedere brevemente le scelte che ho fatto per soddisfare questi tre requisiti.

# 2 - Technology Stack

**MongoDB**: paradigma *noSQL*, *non* relazionale ma modella i dati in documenti.

> I dati con cui ho lavorato si potevano gestire efficacemente anche restando nel classico modello relazionale...

...ma meglio MongoDB perché è una tecnologia *relativamente nuova* ma *sufficientemente matura*.

Saperlo utilizzare è abilità *utile* e *spendibile* in molti ambiti.

> Ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

Algoritmi di data mining: **Weka**. Già usato nel corso *Data Mining and Organization*, qualche difetto ma adeguato.

**Visualizzazione**: fogli di calcolo per operazioni semplici...
> mentre per quelle più complesse sono andato a scomodare uno strumento più potente, cioè il **linguaggio R**.

# 3 - Dati grezzi

2 famiglie di dati:*studenti* e *insegnamenti*.

**Studenti**: record *anonimi* riguardo alla carriera accademica

- *attributi generici* (e.g. il voto ottenuto al test di ingresso)
- *per ogni esame*, la **data** in cui è stato superato e il **voto** conseguito

Riguardano gli studenti *immatricolati dal 2010 al 2013*, coprono i *quattro Anni Accademici* successivi all’immatricolazione.

> Relativamente al lasso di tempo *totale* coperto dai dati degli studenti - dal 2010 al 2017 - mi sono state fornite le risposte ai **questionari di valutazione degli insegnamenti**, ovviamente in *forma aggregata rispetto ai quesiti* per preservare l'anonimato di chi ha espresso le valutazioni.

# 4 - Scatter Plot

> La prima cosa che ho fatto dopo aver ricevuto i dati, è stata *studiarli nella loro forma iniziale* usando varie tecniche di visualizzazione, cercando di intuire qualcosa di utile per direzionare le analisi successive.

Vediamo alcuni utilizzi di qualche tecnica di visualizzazione.

Ad esempio, **grafico di dispersione** fra la *media dei voti* (ascisse) degli studenti e il loro *punteggio al test di ingresso* (ordinate).

Cosa si nota?

- non ci sono particolari differenze di prestazioni fra le varie coorti di immatricolazione, a parte qualche outlier.
- *speculare* che ci sia una **correlazione diretta** fra i due attributi

# 5 - Matrice std. dev.

Altro esempio, sempre riguardo ai **dati degli studenti**

Matrice che mostra l'andamento della **deviazione standard** dei voti ottenuti dagli studenti negli **esami del primo anno**.

- *gruppi di studenti* hanno preso un *voto inferiore alla media* in ogni esame (fasce orizzontali blu)
- in alcuni esami i voti tendono a *discostarsi meno dalla loro media*, (colori meno accesi di determinate fasce).

<div style="page-break-after: always;"></div>

# 6 - Preprocessing

Dopo lo studio sui dati iniziali, ho preparato i dati per il data mining.

**Studenti**: aggregato le istanze *rispetto ai corsi d'esame* di ogni anno, distillando quelle informazioni in pochi attributi più sintetici, ad esempio:

- *media dei voti*
- *ritardo medio* accusato dagli studenti nel superare l'esame rispetto al primo appello disponibile

**Insegnamenti**: aggregato ulteriormente le risposte ai quesiti per ridurre il numero di attributi.

Ricavato dataset unico facendo un **inner join** e a partire da quello...

> ...tramite altre operazioni di **preprocessing**, ho reso i dati adatti ad essere usati come input per gli algoritmi di data mining che adesso, finalmente, vedremo.

# 7 - Clustering

> Vi mostro, ovviamente, soltanto il risultato più significativo di quella che è stata una lunga serie di tentativi fatti per valutare le prestazioni varie configurazioni possibili.

> Questo miglior risultato, è stato ottenuto utilizzando l'agorotimo **K-Means**...

> ...e la **distanza euclidea** come metrica di prossimità fra i vari punti del dataset - è una scelta piuttosto standard, forse banale, ma è risultata la più adeguata.

K-Means richiede come parametro iniziale il *numero di cluster* in cui partizionare il dataset. **2**, perché:

- miglior scelta in termini di valutazione del risultato
- > intuitivamente, si può sperare che i due cluster trovati rappresentino uno i corsi **buoni** e l'altro i corsi **meno buoni**, almeno per quanto riguarda gli *attributi* considerati...

> ...che sono **questi tre**: *voto medio* all'esame, *ritardo medio* nel superarlo e *valutazione complessiva media* data al corso. Sembrano pochi, ma in realtà sono abbastanza rappresentativi di tutti gli aspetti fondamentali dei dati a nostra disposizione.

<div style="page-break-after: always;"></div>

# 8 - Risultati Clustering

Sezione dei dati lungo il piano *ritardo medio* (ascisse) e *voto medio* (ordinate); i punti ovviamnte sono i corsi di un determinato Anno Accademico.

I due cluster trovati sono abbastanza *polarizzati verso gli estremi buoni* dei due attributi visualizzati:

- cluster blu, voto alto e ritardo basso
- cluster rosso il contrario

> Le altre sezioni mostrano un comportamento simile, quindi *ad una prima analisi visiva* questo clustering sembra buono.

# 9 - Valutazione Clustering

**Matrice delle distanze euclidee** e **matrice di incidenza** del clustering.

Ispezione visiva: *distanza bassa* fra punti appartenenti allo *stesso cluster*, e viceversa.

Aspetto confermato dalla **correlazione negativa** fra le due matrici.

K-Means ha raggruppato in questi due cluster dei punti che sono effettivamente vicini fra di loro: *il clustering è buono*.

# 10 - Interpretazione Clustering

Cluster dei corsi *meno buoni* (rispetto ai tre attributi considerati):

- materie *più ostiche* per la maggioranza degli studenti
  - prestazioni peggiori (ritardo alto e voto basso)
  - valutati più severamente

Specularmente, nell'altro cluster:

- materie *assimilate più agilmente*
  - prestazioni migliori
  - valutati più generosamente.

> Questa lettura lascia intuire che ci sia una correlazione fra le prestazioni degli studenti in un certo e la loro valutazione data sul rispettivo corso.

[//]: # (Printed 'till here!)

# 11 - Regole Associative

*Ricerca di regole associative*, cioè di implicazioni fra i valori di alcuni attributi.

Anche in questo caso metodo *trial-and-error*, quindi risultato migliore ottenuto alla fine di un percorso di vari tentativi.

- Implementazione di **Apriori** di Weka
- Metrica di confidenza: **lift**

Lift molto efficace: se regola *A implica B*, lift è rapporto fra *probabilità di B dato A* e *probabilità di B indipendentemente da A*.

- **Discretizzazione** degli attributi continui in *range* discreti (BASSO, MEDIO e ALTO)
- Focus sui soliti **tre attributi** rappresentativi


# 12 - Regole Associative: ritultati

Selezionato le **10 regole migliori** secondo la metrica del lift.

> Queste dieci regole combaciano perfettamente in *cinque implicazioni doppie*, e il loro significato va sempre in una direzione: delle *buone prestazioni in un esame* - ritardo basso e voto alto - implicano una *buona valutazione del rispettivo corso*, e viceversa. Perciò, come si sospettava, esiste una correlazione diretta fra questi due aspetti.

# 13 - Pattern Sequenziali Frequenti

> Guardiamo ora l'ultima analisi che ho fatto - forse la più interessante.

Ricerca di *pattern frequenti* fra le *sequenze di esami* superati dagli studenti.

- Preprocessing *ad hoc* su dati degli studenti, costruire le **sequenze ordinate** degli esami superati da ogni studente.

Si sarebbe potuto molto altro, ad esempio:

- raggruppare esami superati nello stesso appello
- considerare solo sequenze che rispettano un certo **gap** temporale massimo

> Purtroppo,l'implementazione di **GSP** che offre Weka non offre nessuna di queste possibilità, quindi ho creato le sequenze *rispettando solo l'ordine in cui ogni studente ha superato i vari esami*, senza considerare altro.

> Infine, è stata di fondamentale importanza l'interpretazione data ai pattern frequenti ottenuti. L'output di GSP è stato fin troppo generoso: fra tutti quelli frequenti, quali sono i pattern interessanti? Chiaramente, quelli non **ordinati**.


# 14 - Pattner Sequenziali Frequenti: pattern interessanti

> Cosa significa che un pattern è *ordinato*?

Lista di tutti i corsi d'esame del CdL, ordinati nella *giusta* sequenza.

Questa è una *relazione d'ordine parziale* sull'insieme degli esami.

> Vediamo un esempio di pattern non ordinato.

# 15 - Pattner Sequenziali Frequenti - pattern non ordinati

*[descrivi il concetto di **esame fuori posto**]*

# 16 - Pattern Sequenziali Frequenti - post processing

> Come ho riassunto le informazioni contenute nei pattern frequenti non ordinati?

> Ho contato quante volte un esame è stato *fuori posto* nei pattern frequenti, e ho creato un **diagramma a torta**.

Che osservazioni si possono fare?

> Innegabile che, se un'esame si trova frequentemente fuori posto, presenta delle *difficoltà di qualche tipo* agli studenti.

Significato esame fuori posto:

- bocciato e superato *solo dopo aver ripetuto il corso*
- *saltato* in favore di esami più facili, anche se teoricamente successivi

**Fisica** è l'esame più presente nei pattern non ordianti (spesso è proprio *l'ultimo esame* che gli studenti superano).

> Curiosamente, non sblocca alcun vincolo di propedeuticità: che molti studenti siano *portati ad ignorarlo* fino ad aver completato il resto del corso di laurea?

# 0 - Introduzione

> Quella che sto per presentare, è una descrizione dell'analisi di alcuni dati relativi a *qualche aspetto* del Corso di Laurea triennale in informatica.

> Una parte principale di questa analisi è stata, come vedremo, l'attività di **data mining**.

# 1 - Data Mining

> Come suggerisce la metafora nel nome

**Data mining** = *estrarre* informazioni *preziose* da una grande mole di dati grezzi.

Procedimento:

- > Si effettua innanzitutto una fase di **pre processing**...
- > ...per rendere i dati iniziali *adatti* ad essere usati come input per gli **algorimi di data mining** che si desidera utilizzare.
- > Infine, in quella che è una fase di **post processing**, si dispone l'output in modo da favorirne l'interpretazione.

C'è quindi bisogno *principalmente* di **tre** strumenti software:

- **data base** per strutturare agilmente i dati
- libreria di **implementazioni di algoritmi per il data mining**
- software per tecniche di **visualizzazione**

> Andiamo a vedere brevemente le scelte che ho fatto per soddisfare questi tre requisiti.

# 2 - Technology Stack

**MongoDB** adotta il paradigma *noSQL*: *non* segue il modello relazionale ma *memorizza i dati in documenti*.

I dati con cui ho lavorato si sarebbero potuti *gestire efficacemente anche restando nel classico modello relazionale*.

Ho scelto cmq MongoDB, perché è una tecnologia **relativamente nuova** ma **sufficientemente matura**, e saperlo utilizzare è abilità *utile* e *spendibile* in molti ambiti. Ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

Algoritmi di data mining: **Weka**. Già usato nel corso *Data Mining and Organization*, qualche difetto ma adeguato.

**Visualizzazione**: fogli di calcolo per operazioni semplici, linguaggio R per quelle più complesse.

# 3 - Dati grezzi

**Studenti**: record *anonimi* riguardo alla carriera accademica.

- *Attributi generici* (e.g. il voto ottenuto al test di ingresso);
- *Per ogni esame*, la **data** in cui è stato superato e il **voto** conseguito.

Riguardano gli studenti *immatricolati dal 2010 al 2013*, coprono i *quattro Anni Accademici* successivi all’immatricolazione.

> Relativamente al lasso di tempo *totale* coperto da questi dati - dal 2010 al 2017 - mi sono state fornite le risposte degli stidenti ai **questionari di valutazione degli insegnamenti**, ovviamente in *forma aggregata rispetto ai quesiti* per preservare l'anonimato di chi ha espresso le valutazioni.

Ho avuto a che fare con queste due famiglie di dati. Come li ho impiegati?

# 4 - Scatter Plot

> La prima cosa da fare è stata *studiarli nella loro forma iniziale* usando varie **tecniche di visualizzazione**, per cercare di intuire qualcosa di utile per direzionare le analisi successive.

Vediamo un paio di esempi di utilizzo di questo genere di tecniche.

**Grafico di dispersione** fra la *media dei voti* (ascisse) degli studenti e il loro *punteggio al test di ingresso* (ordinate).

Cosa può dirci questo grafico?

- Non ci sono particolari differenze di prestazioni fra le varie coorti di immatricolazione, a parte qualche outlier;
- *Speculare* che ci sia una **correlazione diretta** fra i due attributi.

# 5 - Matrice deviazione standard

Altro esempio, sempre riguardo ai **dati degli studenti**

Matrice che mostra l'andamento della **deviazione standard** dei voti ottenuti dagli studenti negli **esami del primo anno**.

Cosa possiamo intuire?

- *Gruppi di studenti* hanno preso *voti inferiori alla media* in ogni esame (fasce orizzontali blu);
- In alcuni esami i voti tendono a *discostarsi meno dalla loro media* (colori di alcune colonne meno accesi).

<div style="page-break-after: always;"></div>

# 6 - Preprocessing

Dopo lo studio sui dati iniziali, li ho preparati per il data mining.

**Studenti**: aggregato le istanze *rispetto ai corsi d'esame* di ogni anno, distillando tutte quelle informazioni in pochi attributi più sintetici:

- *Media dei voti*;
- *Ritardo medio* accusato dagli studenti nel superare l'esame rispetto al primo appello disponibile.

**Insegnamenti**: aggregato ulteriormente le risposte ai quesiti per ridurre il numero di attributi.

> I due dataset aggregati avevano le stesse chiavi, perciò facendo un **inner join**, ho ricavato questo *dataset unico* che ho poi usato come base per creare di volta in volta l'input necessario ai vari algoritmi di data mining - che adesso vedremo.

# 7 - Clustering

Mostro soltanto il risultato più significativo - lunga serie di tentativi per *valutare le prestazioni* dei vari *algoritmi* e delle loro *configurazioni*.

- Miglior risultato ottenuto con **K-Means**
- Metrica di prossimità: **distanza euclidea**
  > è una scelta piuttosto standard, forse banale, ma è risultata la più adeguata.

K-Means richiede come parametro iniziale il *numero di cluster* in cui partizionare il dataset. Scelto **2**, perché:

- miglior scelta in termini di valutazione del risultato
- > intuitivamente, si può sperare che i due cluster trovati rappresentino uno i corsi **buoni** e l'altro i corsi **meno buoni**, almeno per quanto riguarda gli *attributi* considerati...

> ...che sono **questi tre**: *voto medio* all'esame, *ritardo medio* nel superarlo e *valutazione complessiva media* data al corso. Sembrano pochi, ma in realtà sono abbastanza rappresentativi di tutti gli aspetti fondamentali dei dati a nostra disposizione.

<div style="page-break-after: always;"></div>

# 8 - Risultati Clustering

Sezione dei dati lungo il piano *ritardo medio* (ascisse) e *voto medio* (ordinate); i punti ovviamente sono i corsi di un determinato Anno Accademico.

I due cluster trovati sono abbastanza **polarizzati verso gli estremi buoni** dei due attributi visualizzati:

- cluster blu, voto alto e ritardo basso
- cluster rosso il contrario

Le altre sezioni mostrano un comportamento simile: si può dire che il *cluster 0* (blu) includa i corsi buoni, mentre l'altro i corsi *meno buoni*.

> Ad una prima *analisi visiva* questo clustering sembra buono.

# 9 - Valutazione Clustering

Approccio più analitico: **matrice delle distanze euclidee** e **matrice di incidenza** del clustering.

> Si nota subito che i punti appartenenti allo *stesso cluster* sono *meno distanti* fra loro di quelli che appartengono a due cluster diversi, e questo aspetto è confermato dalla **correlazione** fra le due matrici, che è **negativa**.

K-Means ha raggruppato in questi due cluster dei punti che sono effettivamente vicini fra di loro: *il clustering è buono*.

# 10 - Interpretazione Clustering

Nel *cluster 1*  corsi *meno buoni* (rispetto ai tre attributi considerati):

Nel *cluster 1* (rosso) sono finite tutte le istanze delle materie *più ostiche*:

- studenti hanno avuto prestazioni peggiori
- li hanno valutati più severamente

Specularmente, nel *cluster 0* (blu), sono andate principalmente le materie *assimilate più agilmente*:

- studenti con prestazioni migliori
- valutati più generosamente.

> Questa lettura lascia intuire che ci sia una correlazione fra le prestazioni degli studenti e la valutazione data al rispettivo corso.

<div style="page-break-after: always;"></div>

# 11 - Regole Associative

*Ricerca di regole associative*, cioè di implicazioni fra i valori di alcuni attributi.

Anche in questo caso metodo *trial-and-error*, quindi risultato migliore ottenuto alla fine di un percorso di vari tentativi.

- Implementazione di **Apriori** di Weka
- Metrica di confidenza: **lift**

Lift molto efficace: se esiste una regola del tipo *A implica B*, lift è rapporto fra *probabilità di B dato A* e *probabilità di B indipendentemente da A*.

- **Discretizzazione** degli attributi continui in *range* discreti (BASSO, MEDIO e ALTO)
- Focus sui soliti *tre attributi rappresentativi*

# 12 - Regole Associative: risultati

Selezionato le **10 regole migliori** secondo la metrica del lift.

> Queste dieci regole combaciano perfettamente in *cinque implicazioni doppie*, e il loro significato va sempre in una direzione: delle *buone prestazioni in un esame* - ritardo basso e voto alto - implicano una *buona valutazione del rispettivo corso*, e viceversa.

> Perciò, come si sospettava, esiste una correlazione diretta fra questi due aspetti.

# 13 - Pattern Seq. Frequenti

> Guardiamo ora l'ultima analisi che ho fatto - forse la più interessante.

Ricerca di *pattern frequenti* fra le *sequenze di esami* superati dagli studenti.

- Preprocessing *ad hoc* su dati degli studenti, costruire le **sequenze ordinate** degli esami superati da ogni studente.

Si sarebbe potuto molto altro, ad esempio:

- raggruppare esami superati nello stesso appello
- considerare solo sequenze che rispettano un certo **gap** temporale massimo

> Purtroppo,l'implementazione di **GSP** che offre Weka non offre nessuna di queste possibilità, quindi ho creato le sequenze *rispettando solo l'ordine in cui ogni studente ha superato i vari esami*, senza considerare altro.

> Infine, è stata di fondamentale importanza l'interpretazione data ai pattern frequenti ottenuti. L'output di GSP è stato fin troppo generoso: fra tutti quelli frequenti, quali sono i pattern interessanti? Chiaramente, quelli non **ordinati**.

# 14 - Pattner Seq. Frequenti - pattern non ordinati

> Prendiamo ad esempio questo pattern sequenziale frequente.

[Calcolo Numerico], [Informatica Teorica], [Fisica Generale]

> La particolarità in questo pattern è il fatto che *Fisica Generale*, un esame del *secondo anno*, è stato superato successivamente a due esami del *terzo anno*.

Pattern di questo tipo sono molto interessanti, contengono informazioni preziose.

Perché un esame può essere frequentemente "fuori posto":

- bocciato e superato *solo dopo aver ripetuto il corso*
- *saltato* in favore di esami più facili, anche se teoricamente successivi

> In ogni caso, è innegabile che, se un'esame si trova frequentemente fuori posto, presenta delle *difficoltà di qualche tipo* per la maggioranza degli studenti.

# 15 - Pattern Seq. Frequenti - post processing

> Come ho riassunto le informazioni contenute nei pattern frequenti non ordinati?

> Ho contato quante volte un esame è stato *fuori posto* nei pattern frequenti, e ho creato un **diagramma a torta**.

**Fisica** è l'esame più presente nei pattern non ordianti (spesso è proprio *l'ultimo esame* che gli studenti superano).

Le interpretazioni possono essere molte, una può essere questa: non sblocca vincoli di propedeuticità: forse molti studenti sono *portati ad ignorarlo* fino ad aver completato il resto del corso di laurea.

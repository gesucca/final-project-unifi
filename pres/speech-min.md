# 0 - introduzione

> Quella che vi sto per presentare è una descrizione dell'analisi che ho fatto su alcuni dati dati relativi a *qualche aspetto* del Corso di Laurea triennale in informatica.

> Una parte principale di questa analisi è stata, come vedremo, l'attività di **data mining**.

# 1 - data mining

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

# 2 - technology stack

**MongoDB**: paradigma *noSQL*, *non* relazionale ma modella i dati in documenti.

> I dati con cui ho lavorato si potevano gestire efficacemente anche restando nel classico modello relazionale...

...ma meglio MongoDB perché è una tecnologia *relativamente nuova* ma *sufficientemente matura*.

Saperlo utilizzare è abilità *utile* e *spendibile* in molti ambiti.

> Ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

___

Algoritmi di data mining: **Weka**. Già usato nel corso *Data Mining and Organization*, qualche difetto ma adeguato.

___

**Visualizzazione**: fogli di calcolo per operazioni semplici...
> mentre per quelle più complesse sono andato a scomodare uno strumento più potente, cioè il **linguaggio R**.

# 3 - dati grezzi

2 famiglie di dati:*studenti* e *insegnamenti*.

**Studenti**: record *anonimi* riguardo alla carriera accademica

- *attributi generici* (e.g. il voto ottenuto al test di ingresso)
- *per ogni esame*, la **data** in cui è stato superato e il **voto** conseguito

Riguardano gli studenti *immatricolati dal 2010 al 2013*, coprono i *quattro Anni Accademici* successivi all’immatricolazione.

___

> Relativamente al lasso di tempo *totale* coperto dai dati degli studenti - dal 2010 al 2017 - mi sono state fornite le risposte ai **questionari di valutazione degli insegnamenti**, ovviamente in *forma aggregata rispetto ai quesiti* per preservare l'anonimato di chi ha espresso le valutazioni.

# 4 - scatter plot

> La prima cosa che ho fatto dopo aver ricevuto i dati, è stata *studiarli nella loro forma iniziale* usando varie tecniche di visualizzazione, cercando di intuire qualcosa di utile per direzionare le analisi successive.

Vediamo alcuni utilizzi di qualche tecnica di visualizzazione.

Ad esempio, **grafico di dispersione** fra la *media dei voti* (ascisse) degli studenti e il loro *punteggio al test di ingresso* (ordinate).

Cosa si nota?

- non ci sono particolari differenze di prestazioni fra le varie coorti di immatricolazione, a parte qualche outlier.
- *speculare* che ci sia una **correlazione diretta** fra i due attributi

# 5 - matrice std dev

Altro esempio, sempre riguardo ai **dati degli studenti**

Matrice che mostra l'andamento della **deviazione standard** dei voti ottenuti dagli studenti negli **esami del primo anno**.

- *gruppi di studenti* hanno preso un *voto inferiore alla media* in ogni esame (fasce orizzontali blu)
- in alcuni esami i voti tendono a *discostarsi meno dalla loro media*, (colori meno accesi di determinate fasce).

# 6 - preprocessing

Dopo lo studio sui dati iniziali, ho preparato i dati per il data mining.

**Studenti**: aggregato le istanze *rispetto ai corsi d'esame* di ogni anno, distillando quelle informazioni in pochi attributi più sintetici, ad esempio:

- *media dei voti*
- *ritardo medio* accusato dagli studenti nel superare l'esame rispetto al primo appello disponibile

**Insegnamenti**: aggregato ulteriormente le risposte ai quesiti per ridurre il numero di attributi.

Ricavato dataset unico facendo un **inner join** e a partire da quello...

> ...tramite altre operazioni di **preprocessing**, ho reso i dati adatti ad essere usati come input per gli algoritmi di data mining che adesso, finalmente, vedremo.

# 7 - clustering

> Vi mostro, ovviamente, soltanto il risultato più significativo di quella che è stata una lunga serie di tentativi fatti per valutare le prestazioni varie configurazioni possibili.

> Questo miglior risultato, è stato ottenuto utilizzando l'agorotimo **K-Means**...

___

> ...e la **distanza euclidea** come metrica di prossimità fra i vari punti del dataset - è una scelta piuttosto standard, forse banale, ma è risultata la più adeguata.

___

K-Means richiede come parametro iniziale il *numero di cluster* in cui partizionare il dataset. **2**, perché:

- miglior scelta in termini di valutazione del risultato
- > intuitivamente, si può sperare che i due cluster trovati rappresentino uno i corsi **buoni** e l'altro i corsi **meno buoni**, almeno per quanto riguarda gli *attributi* considerati...

___

> ...che sono **questi tre**: *voto medio* all'esame, *ritardo medio* nel superarlo e *valutazione complessiva media* data al corso. Sembrano pochi, ma in realtà sono abbastanza rappresentativi di tutti gli aspetti fondamentali dei dati a nostra disposizione.
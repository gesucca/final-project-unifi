# 0

Quella che vi sto per presentare è una descrizione *estremamente sintetica* dell'analisi che ho fatto su alcuni dati dati relativi a *qualche aspetto* del Corso di Laurea triennale in informatica.

Una parte principale di questa analisi è stata, come vedremo, l'attività di *data mining*.


# 1

Come suggerisce la metafora nel nome, fare *data mining* significa estrarre delle informazioni preziose - quindi, utili - da una grande mole di dati grezzi.

Il procedimento che solitamente si segue è questo [address the slide]: si da innanzitutta una *struttura* ai dati iniziali, rendendoli adatti ad essere forniti come input al *software* che implementa l'algorimo di data mining che si desidera utilizzare, per poi disporne l'output in modo da favorirne l'interpretazione.

Per realizzare tutto questo, ho avuto bisogno *principalmente* di tre strumenti software:

- un *data base* per manipolare agilmente i dati e dargli la forma che serve;
- una libreria di implementazioni degli algoritmi per il data mining;
- qualche strumento per la *visualizzazione* di dati;

Andiamo a vedere brevemente le scelte che ho fatto per soddisfare questi tre requisiti.


# 2

Come base di dati ho scelto MongoDB, un data base *non* relazionale che modella i dati in documenti strutturati secondo la Java Script Object Notation.

Come sarà chiaro a breve, i dati con cui ho lavorato si potevano gestire efficacemente anche restando nel classico modello relazionale, ma ho preferito comunque utilizzare MongoDB. Si tratta di una tecnologia *relativamente nuova* ma *sufficientemente matura*, ed ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

[nuova slide]

Per quanto riguarda gli algoritmi di data mining, la scelta è ricaduta sul software Weka: uno strumento che ho già usato nel corso di Data Mining and Orgnaization e che, nonostante abbia alcuni difetti, è comunque uno strumento abbastanza completo ed è risultato adeguato al mio scopo.

[nuova slide]

Infine, per le tecniche di visualizzazione ho scelto di usare dei banali fogli di calcolo per le operazioni più semplici, mentre per quelle più complesse sono andato a scomodare uno strumento più potente, cioè il linguaggio R.


# 3

Andiamo ora a vedere il materiale grezzo a disposizione. Abbiamo a che fare con due gruppi di dati: uno relativo agli *studenti*, l'altro agli *insegnamenti*.

Riguardo agli *studenti*, per coloro immatricolati dal 2010 al 2013, abbiamo dei record *anonimi* riguardo alla loro carriera accademica lungo *quattro anni* - ovvero, per ogni esame, la data in cui è stato superato e il voto conseguito, oltre ad altri attributi generici come ad esempio il punteggio raggiunto al test di ingresso.

Come si vede dal grafico, i dati degli studenti coprono tutto il periodo che va dal 2010 al 2017, anche se in modo *non uniforme*. Quindi, relativamente a questo lasso di tempo, sono state prese in considerazione le risposte date dagli studenti ai *questionari di valutazione degli insegnamenti*, ovviamente in forma aggregata rispetto ai quesiti per preservare l'anonimato di chi ha espresso le valutazioni.


# 4

Che cosa ho fatto con questi dati? Innanzitutto, li ho studiati nella loro forma iniziale usando varie tecniche di visualizzazione, cercando di intuire qualcosa di utile per direzionare le analisi successive.

Ad esempio, producendo dei grafici di dispersione riguardo al dataset della *carriera degli studenti*, si può notare che non ci sono particolari differenze di prestazioni fra le varie coorti di immatricolazione --- a parte qualche outlier --- e si potrebbe *speculare* che ci sia una correlazione diretta fra il *punteggio del test di ingresso* - sulle ascisse - e il *voto medio* ottenuto negli esami - sulle ordinate.


# 5

Un altro esempio, sempre riguardante i *dati degli studenti*, può essere questo: una matrice che mostra l'andamento dello *scarto quadratico medio* dei voti ottenuti dagli studenti - le righe - negli *esami del primo anno* - le colonne.

Si può notare, fra le altre cose, come dei gruppi di studenti abbiano preso un voto inferiore alla media in ogni esame - mi riferisco alle fasce orizzontali blu, così come si può vedere che in alcuni esami i voti tendono a discostarsi meno dalla loro media, come si può vedere dai colori meno accesi di determinate fasce.


# 6

Per entrare nel vivo dell'analisi e utilizzare finalmente delle tecniche di data mining, occorre preparare i dati adeguatamente.

Visto che i due dataset a mia disposizione hanno un elemento in comune - il corso di insegnamento - un'idea ovvia è stata quella di effettuare un'operazione di *join* fra di essi. Per realizzarlo, ho aggregato le istanze degli studenti rispetto ai *corsi d'esame* di ogni anno - condensando quelle informazioni in attributi come ad esempio la media dei voti, o il ritardo con cui è stato superato quell'esame. Fatto questo, le chiavi primarie hanno combaciato, e ho potuto ricavare questo dataset facendo semplicemente un *inner join* fra i due che avevo a disposizione.

Da questa struttura, poi, tramite altre operazioni di *preprocessing*, ho reso i dati adatti ad essere usati come input per gli algoritmi di data mining che adesso, finalmente, vedremo.


# 7

Cominciamo dal *clustering*: vi mostro, ovviamente, soltanto il risultato più significativo di quella che è stata una lunga serie di tentativi fatti per testare e valutare le varie configurazioni dei vari algoritmi, come suggerisce il buon vecchio metodo *trial-and-error*.

Questo miglior risultato, è stato ottenuto utilizzando l'agorotimo *K-Means*...

...e la *distanza euclidea* come metrica di prossimità fra i vari punti del dataset - è una scelta piuttosto standard, forse banale, ma è risultata la più adeguata.

L'algoritmo K-Means richiede di scegliere a prescindere il numero di cluster in cui partizionare il dataset. Ho scelto una suddivisione in *due cluster*, sia perché è risultata la migliore in termini di valutazione del risultato, sia perché intuitivamente si può sperare che i due cluster trovati rappresentino uno i corsi *migliori* e l'altro i corsi *peggiori*, almeno per quanto riguarda gli attributi considerati.

Riguardo proprio agli attributi, ho scelto di considerarne tre: *voto medio* conseguito dagli studenti, *valutazione complessiva media* data ai corsi e *ritardo medio* degli studenti nel superare quell'esame rispetto al primo appello disponibile.


# 8

Vediamo che cosa ha trovato l'algoritmo K-Means.

Questa è una sezione dei dati lungo il piano formato dal ritardo medio (sulle ascisse) e il voto medio (sulle ordinate); i punti ovviamnte sono i corsi di un determinato Anno Accademico. Si può vedere che i due cluster trovati sono *abbastanza polarizzati* verso gli estremi "buoni" dei due attributi visualizzati: cluster blu, voto alto e ritardo basso; cluster rosso il contrario.

Le altre sezioni mostrano *visivamente* un comportamento simile, quindi *a occhio* questo clustering sembra buono.


# 9

Impiegando un appoccio un po' più analitico, sono andato a calcolare la correlazione fra la *matrice delle distanze euclidee* e la *matrice di incidenza* di questo clustering, che viene *negativa*.

Che significa? Che la distanza euclidea fra due punti del dataset tende ad essere *bassa* quando essi appartengono allo stesso cluster, e viceversa. Quindi, l'algoritmo K-Means ha raggruppato in questi due cluster dei punti che sono effettivamente vicini fra di loro.


# 10

Visto che il clustering è buono, si può andare a vedere quali corsi siano finiti nel cluster dei corsi buoni e quali in quello dei corsi meno buoni.

Volendo spendere due parole sulle possibile lettura di questi risultati, sembrerebbe naturale che nel *cluster dei corsi peggiori* - intesi tali rispetto ai nostri tre attributi - siano finite molte istanze delle *materie più difficili* per la maggioranza degli studenti, i cui esami vengono superati con voti bassi e dopo vari appelli, e - come vi mostrerò adesso - le prestazioni basse in un certo esame implicano generalmente una bassa valutazione del suo corso.

Specularmente, è naturale che nel *cluster dei corsi migliori* siano andate la maggioranza delle *materie assimilate più agilmente*, quelle in cui gli studenti hanno avuto prestazioni migliori e che quindi hanno valutato più generosamente.

Non mi sono azzardato a trarre nessuna conclusione, ma posso dire che, per quella che è la mia esperienza, alcuni di questi risultati un po' mi sorprendono, mentre altri decisamente no.


# 11

Passiamo a vedere la *ricerca di regole associative*, cioè di implicazioni fra i valori di alcuni attributi. Anche in questo caso, ho seguito il metodo *trial-and-error*, quindi vi mostro solamente quello che ho giudicato essere il miglior risultato fra i tanti tentativi fatti.

Ho usato ovviamente l'implementazione di Weka dell'algoritmo *Apriori*...

...impostato per usare il *lift* come metrica di confidenza delle regole associative.

C'è stato bisogno di *discretizzare* i valori continui degli attributi considerati, facendoli rientrare in dei *range* sufficientemente ampi per non generare confusione, ma abbastanza definiti come significato - la classica divisione in "BASSO", "MEDIO" e "ALTO" è andata più che bene.

Il focus è stato messo sugli stessi attributi considerati per il clustering, visto che questa scelta in quella sede aveva funzionato.


# 12

Fra tutte quelle ottenute, ho selezionato le *dieci regole associative migliori*, tutte con ottimi valori di lift e quasi tutte con un valore di confidenza accettabile.

Curiosamente, queste dieci regole combaciano perfettamente in cinque implicazioni doppie, il cui significato va sempre in una direzione: *buone prestazioni agli esami* - cioè ritardo basso e voto alto - *implicano una buona valutazione del corso*, e *viceversa*.


# 13

Guardiamo ora l'ultima analisi che ho fatto - forse la più interessante. Si tratta della ricerca di *pattern frequenti* fra le sequenze di esami superati dagli studenti.

Cosa ho fatto? [leggi]

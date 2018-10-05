# 0

Quella che vi sto per presentare è una descrizione **estremamente sintetica** dell'analisi che ho fatto su alcuni dati dati relativi a **qualche aspetto** del Corso di Laurea triennale in informatica.

Una parte principale di questa analisi è stata, come vedremo, l'attività di **data mining**.


# 1

Come suggerisce la metafora nel nome, fare **data mining** significa estrarre delle informazioni *preziose* - quindi, *utili* - da una grande mole di dati grezzi.

Il procedimento che si segue è questo: si **trasformano i dati inziali** in modo appropriati, ai dati iniziali, si danno in input al **software** che implementa *l'algorimo di data mining* che si desidera utilizzare, infine si dispone l'output in modo da favorirne l'interpretazione.

Per realizzare tutto questo, ho avuto bisogno **principalmente** di tre strumenti software:

- un **data base**
- una libreria di algoritmi per il data mining;
- qualche strumento per la **visualizzazione** di dati;

Andiamo a vedere brevemente le scelte che ho fatto per soddisfare questi tre requisiti.


# 2

Come base di dati ho scelto MongoDB, un data base **non** relazionale che modella i dati in documenti. I dati con cui ho lavorato si potevano gestire efficacemente anche restando nel classico modello relazionale, ma ho preferito comunque utilizzare MongoDB, perché si tratta di una tecnologia **relativamente nuova** ma **sufficientemente matura**, e ho ritenuto importante sfruttare questo lavoro come occasione per prenderci confidenza.

Per quanto riguarda gli algoritmi di data mining, la scelta è ricaduta sul software Weka. È uno strumento che ho già usato nel corso di Data Mining and Orgnaization, ha qualche difetto ma è comunque uno strumento adeguato.

Infine, per le tecniche di visualizzazione ho scelto di usare dei banali **fogli di calcolo** per le operazioni più semplici, mentre per quelle più complesse sono andato a scomodare uno strumento più potente, cioè il **linguaggio R**.


# 3

Andiamo ora a vedere il materiale grezzo a disposizione. Abbiamo a che fare con due gruppi di dati: uno relativo agli **studenti**, l'altro agli **insegnamenti**.

Riguardo agli **studenti**, abbiamo dei record **anonimi** riguardo alla carriera accademica – ovvero: qualche attributo generico (ad esempio, il voto ottenuto al test di ingresso), ma soprattutto, **per ogni esame**, la *data* in cui è stato superato e il *voto* conseguito. Come si vede dal grafico, questi dati erano a disposizione per coloro immatricolati dal 2010 al 2013, e coprivano i quattro Anni Accademici successivi all’immatricolazione. 

Quindi, relativamente al lasso di tempo totale coperto dai dati degli studenti, mi sono state fornite le risposte ai **questionari di valutazione degli insegnamenti**,  ovviamente in forma aggregata rispetto ai quesiti per preservare l'anonimato di chi ha espresso le valutazioni.

Che cosa ho fatto con questi dati? Innanzitutto, li ho studiati nella loro forma iniziale usando varie tecniche di visualizzazione, cercando di intuire qualcosa di utile per direzionare le analisi successive.

# 4

Ad esempio, osservando questo grafico di dispersione fra la *media dei voti* degli studenti e il loro *punteggio al test di ingresso*, si può notare che non ci sono particolari differenze di prestazioni fra le varie coorti di immatricolazione - a parte qualche outlier. Inoltre, si potrebbe **speculare** che ci sia una **correlazione diretta** fra il *punteggio del test di ingresso* - sulle ascisse - e il *voto medio* ottenuto negli esami - sulle ordinate.


# 5

Un altro esempio, sempre riguardante i **dati degli studenti**, può essere questo: una matrice che mostra l'andamento della **deviazione standard** dei voti ottenuti dagli studenti negli **esami del primo anno**. Si può notare, fra le altre cose, come dei *gruppi di studenti* abbiano preso un *voto inferiore alla media* in ogni esame - mi riferisco alle fasce orizzontali blu, così come si può vedere che in alcuni esami i voti tendono a *discostarsi meno dalla loro media*, come si può vedere dai colori meno accesi di determinate fasce.


# 6

Una volta studiata bene la natura dei dati iniziali, sono entrato nel vivo dell'analisi e ho utilizzato finalmente qualche tecnica di data mining. Prima, però, ho dovuto preparare i dati adeguatamente.

Ho aggregato le istanze degli studenti **rispetto ai corsi d'esame** di ogni anno, condensando quelle informazioni in pochi attributi più sintetici - come ad esempio la **media dei voti**, o il **ritardo medio** accusato dagli studenti nel superare quell'esame rispetto al primo appello disponibile per la loro coorte di immatricolazione. 

Fatto questo, ho potuto ricavare un dataset unico facendo semplicemente un **inner join** fra i due che avevo a disposizione.

Da questa struttura poi, tramite altre operazioni di **preprocessing**, ho reso i dati adatti ad essere usati come input per gli algoritmi di data mining che adesso, finalmente, vedremo.


# 7

Cominciamo dal **clustering**: vi mostro, ovviamente, soltanto il risultato più significativo di quella che è stata una lunga serie di tentativi fatti per testare e valutare le varie configurazioni dei vari algoritmi.

Questo miglior risultato,è stato ottenuto utilizzando l'agorotimo **K-Means**...

...e la **distanza euclidea** come metrica di prossimità fra i vari punti del dataset - è una scelta piuttosto standard, forse banale, ma è risultata la più adeguata.

L'algoritmo K-Means richiede di scegliere a prescindere il numero di cluster in cui partizionare il dataset. Ho scelto una suddivisione in **due cluster**, sia perché è risultata la migliore in termini di valutazione del risultato, sia perché intuitivamente si può sperare che i due cluster trovati rappresentino uno i corsi **buoni** e l'altro i corsi **meno buoni**, almeno per quanto riguarda gli attributi considerati...

...che sono questi tre: *voto medio* all'esame, *ritardo medio* nel superarlo e *valutazione complessiva media* data al corso. Sembrano pochi, ma in realtà sono abbastanza rappresentativi degli aspetti fondamentali di tutti i dati a nostra disposizione.


# 8

Vediamo che cosa ha trovato l'algoritmo K-Means.

Questa è una sezione dei dati lungo il piano formato dal ritardo medio (sulle ascisse) e il voto medio (sulle ordinate); i punti ovviamnte sono i corsi di un determinato Anno Accademico. Si può vedere che i due cluster trovati sono **abbastanza polarizzati** verso gli estremi "buoni" dei due attributi visualizzati: cluster blu, voto alto e ritardo basso; cluster rosso il contrario.

Le altre sezioni mostrano **visivamente** un comportamento simile, quindi **a occhio** questo clustering sembra buono.


# 9

Impiegando un appoccio un po' più analitico, sono andato a calcolare la correlazione fra la **matrice delle distanze euclidee** e la **matrice di incidenza** di questo clustering, che viene **negativa**.

Che significa? Che la distanza euclidea fra due punti del dataset tende ad essere **bassa** quando essi appartengono allo stesso cluster, e viceversa. Quindi, l'algoritmo K-Means ha raggruppato in questi due cluster dei punti che sono effettivamente vicini fra di loro.

Visto che il clustering è buono, si può andare a vedere quali corsi siano finiti nei due cluster.


# 10

Volendo spendere due parole sulle possibile lettura di questi risultati, sembrerebbe naturale che nel **cluster dei corsi meno buoni** - sempre intesi tali rispetto ai nostri tre attributi - siano finite molte istanze delle **materie più difficili** per la maggioranza degli studenti, che hanno avuto prestazioni peggiori e li hanno valutati più severamente. Specularmente, è naturale che nel **cluster dei corsi più buoni** siano andate la maggioranza delle **materie assimilate più agilmente**, quelle in cui gli studenti hanno avuto prestazioni migliori e che quindi hanno valutato più generosamente.

Posso dire che, per quella che è la mia esperienza, alcuni di questi risultati un po' mi sorprendono, mentre altri un po' me li aspettavo.


# 11

Passiamo a vedere la **ricerca di regole associative**, cioè di implicazioni fra i valori di alcuni attributi. Anche in questo caso, ho seguito il metodo **trial-and-error**, quindi vi mostro solamente quello che ho giudicato essere il miglior risultato fra i tanti tentativi fatti.

Ho usato ovviamente l'implementazione di Weka dell'algoritmo **Apriori**...

...impostato per usare il **lift** come metrica di confidenza. Si tratta di una metrica molto efficace nel valutare le regole associative.

C'è stato bisogno di **discretizzare** i valori continui degli attributi considerati, facendoli rientrare in dei **range** discreti - la classica divisione in "BASSO", "MEDIO" e "ALTO" è andata più che bene.

Il focus è stato messo sugli stessi attributi considerati per il clustering, visto che questa scelta in quella sede aveva funzionato.


# 12

Fra tutte quelle ottenute, ho selezionato le **dieci regole associative migliori**, tutte con ottimi valori di lift e quasi tutte con un valore di confidenza accettabile.

Curiosamente, queste dieci regole combaciano perfettamente in cinque implicazioni doppie, il cui significato va sempre in una direzione: **buone prestazioni agli esami** - cioè ritardo basso e voto alto - **implicano una buona valutazione del corso**, e **viceversa**.

# 13

Guardiamo ora l'ultima analisi che ho fatto - forse la più interessante. Si tratta della ricerca di **pattern frequenti** fra le sequenze di esami superati dagli studenti.

C'è stato bisogno innanzitutto di una ulteriore fase di preprocessing sui dati degli studenti, dai quali ho dovuto distillare le informazioni necessarie a ricostruire le **sequenze ordinate** di esami superati da ogni studente. In questa fase si sarebbe potuto fare molte cose diverse, ad esempio raggruppare esami superati nello stesso appello, o considerare solo sequenze che rispettano un certo **gap** temporale massimo; purtroppo...

... l'implementazione di **GSP** che offre Weka non consente di analizzare nulla più delle basiche transazioni composte da singoli item, quindi ho creato le sequenze rispettando solo l'ordine grezzo in cui ogni studente ha superato ogni esame.

Infine, è stata di fondamentale importanza l'interpretazione data ai pattern frequenti ottenuti. L'output di GSP è fin troppo generoso: fra tutti quelli frequenti, quali sono i pattern interessanti? Chiaramente, quelli non **sordinati**.


# 14

Cosa significa che un pattern è *ordinato*?

Quella che vedete qui è la lista di tutti i corsi di esame, ordinati in quella che dovrebbe essere la sequenza *giusta* per superarli: prima gli esami del primo anno - in qualunque ordine fra loro, ovviamente - poi gli esami del primo semestre del secondo anno, poi quelli del secondo semestre del secondo anno e così via.

Quindi, come ho accennato prima, per ogni studente ho creato dai dati a disposizione delle sequenze ordinate come queste, riportanti l'ordine in cui sono stati passati gli esami che lo studente ha passato. Su di questi, ho lanciato l'algoritmo **GSP** e analizzato il suo output, andando a vere quali esami erano stati superati solo dopo di altri teoricamente ad esso successivi


# 15

Vediamo un esempio di pattern non ordinato.

[leggi]

Il fatto che un esame sia fuori posto, , può significare varie cose: che sia stato bocciato e **superato solo dopo aver ripetuto il corso**, oppure che sia stato per qualche ragione **saltato** in favore di esami più facili, anche se teoricamente successivi. Indipendentemente da questo, posso affermare che un'esame che si trova frequentemente fuori posto presenti delle **difficoltà di qualche tipo** agli studenti.

Vediamo come ho riassunto le informazioni ottenute.


# 16

Ho contato quante volte un esame è stato fuori posto in qualche pattern, e ho creato un diagramma a torta.

Anche in questo caso, mi astengo dall'azzardare speculazioni, ma non posso evitare di notare che l'esame più rimandato in assoluto - Fisica - è uno che non sblocca alcun vincolo di propedeuticità, e che quindi molti studenti sono portati ad ignorare tranquillamente fino ad aver completato il resto del corso di laurea.

# FINE
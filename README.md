# SpottedSapienza
Il sito che abbiamo realizzato è una versione web della famosa pagina instagram "Spotted Sapienza", in cui è possibile caricare degli spot/annunci per la comunità universitaria. 
Abbiamo inoltre aggiunto ulteriori funzionalità come la possibilità di spottare eventi, di rispondere a spot inviando messaggi all'autore dello spot. E' stato implementato anche un gioco a quiz tra facoltà a cui è possibile giocare una volta al giorno per far guadagnare punti alla propria facoltà. Sono inoltre presenti la pagina per la registrazione, quella per il login e quella del profilo dove leggere le risposte ai propri spot.

## I LINGUAGGI DI PROGRAMMAZIONE UTILIZZATI SONO PRINCIPALMENTE HTML/CSS/JS/FLASK

# Descrizione dei singoli files
## Home
- home.html:
    Pagina principale del sito. All'interno c'è il codice per le seguenti implementazioni:
    + Navbar per cambiare pagina
    + Hamburger per permettere la visualizzazione della navbar su mobile
    + Sezione filtro facoltà per visualizzare solo gli spot che appartengono ad una determinata facoltà
    + Sezione creazione spot, un form per inserire nel database gli spot
    + Sezione risposta a spot, un form per rispondere privatamente all'utente autore dello spot
    + Sezione bacheca in cui sono visualizzati gli spot presenti sul database
    + Event Handler per:
        -- Aprire le card di registrazione/login
        -- Selezionare lo spot a cui si intende rispondere
        -- Inviare i vari form al modulo Flask per la registrazione su database
        -- Aprire l'hamburger su mobile con un animazione a scorrimento
        -- Aprire come popup le sezioni filtro, creazione spot e risposta spot

- stile homepage.css:
    + Foglio di stile per migliorare l'estetica del sito
    + media query per rendere responsive la pagina, adatta quindi anche a dispositivi mobile

- loginpage.html:
    Schermata di accesso al server:
    + form name=log per effettuare il login caratterizzato da un metodo post e costituito da 2 classi field, una per l'email e una per la password. All'interno dei dield sono presenti delle icone denominate da classi "input-icon". Presente anche un bottone di Login collegato a una funzione Javascript: validateLogin();

    + Funzioni Javascript:
        -- validateLogin(): recupera le informazioni trascritte dall'utente sul form e ne crea un oggetto dati che invia tramite Json al server Flask e che in caso di successo del collegamento chiuderà la schermata di login visualizzata come card attraverso la funzione closeCard();
        
        -- closeCard(): la funzione recupera varie informazioni sullo stile del file home.html della loginpage.html contenute nel file stile homepage.css e esegue vari controlli tramite if per aggiornare la visualizzazione del home.html, non rendendo più visibile la card contenente loginpage.html e la div class sign contenente i bottoni di registrazione e accesso e rende visibile il bottone de il mio profilo e rende visibili gli elementi di .creaspot e .rispondi e disattiva l'overlay di home.html

    - reg_page.html:
        Schermata di registrazione al server:
        + form name= "registr", costituito da 6 campi field e un bottone. Sesto campo field, riferito alla facoltà, è caratterizzato da un menù a tendina con le varie opzioni delle facoltà presenti nel server e da una opzione non selezionabile. Le facoltà vengono direttamente caricate dal server e di cui sono visibili all'utente i nomi delle facoltà ma che a livello di valore sono indicate dal loro codice.
        I campi field email, password e conferma password sono accompagnati da alcune icone definite da "input-icon". Il bottone di registrazione invece è collegato alla funzione Javascript: validateSign();

        + validateSign(): recupera dal form i campi compilati dall'utente, specifica una variabile passwordPattern per eseguire controlli sulla sicurezza della password. Successivamente esegue dei controlli per verificare che tuetti i campi siano stati compilati correttamente e vi è un ulteriore controllo sulla mail per verificare se rispetti il formato delle email e un controllo che verifica se password e conferma password siano uguali. Dopo i controlli costruisce un oggetto data da inviare al server contennete tutte le info. Viene fatta una richiesta GET tramite Json per verificare se l'email è già presente nel server e se così fosse invia un alert all'utente e impedisce la registrazione; altrimenti esegue una richiesta POST tramite Json per caricare i dati nel server e in caso di successo chiude la Card di reg_page.html tramite la funzione Javascript closeCard();

        + closeCard(): chiude la card contenente la schermata reg_page.html e disattiva l'overlay del file home.html

## Spot Eventi

- mappa.html
    Pagina per lo spot di eventi
    + connessione all'API di leaflet per visualizzare una mappa della zona universitaria di Roma
    + Navbar per muoversi all'interno del sito
    + Hamburger per rendere la navbar più agibile agli utenti da mobile
    + Form per il caricamento degli eventi da database mostrando dei pin sulla mappa
      con le informazione relative all'orario e al tipo di evento
    + script javascript per:
        -- muovere il pin sulla mappa al click per inserire all'interno del form per lo spot
           latitudine e longitudine della posizione selezionata
        -- visualizzare sulla mappa gli eventi presenti sul database
        -- permettere una selezione della data/ora dell'evento con widget apposito, effettuando
           controlli sulla data dell'evento
        -- gestione pressione dell'hamburger da mobile da visualizzare con una animazione a scorrimento

- stile mappa.css
    + Foglio di stile per migliorare l'estetica del sito
    + media query per rendere responsive la pagina, adatta quindi anche a dispositivi mobile

## Quiz tra Facoltà

- classifica.html
    Pagina per il gioco a quiz tra facoltà
    + Navbar per muoversi all'interno del sito
    + Hamburger per rendere la navbar più agibile agli utenti da mobile
    + Sezione per la visualizzazione della classifica. Lista di facoltà in ordine di punteggio
    + Classifica alternativa per mobile: lista di facoltà in ordine di punteggio che scorrono su una
      banda orizzontale da sinistra verso destra
    + Sezione per la spiegazione delle regole e per avviare il quiz
    + Sezione per utenti che hanno già giocato con pulsante che "scappa" dal cursore del mouse
    + Timer per indicare il tempo rimanente alla prossima giocata disponibile (quanto manca alla mezzanotte)
    + Sezione che appare una volta premuto il pulsante gioca, quiz con immagine di sfondo a tema, domanda,
      4 alternative disponibili
    + EvenListener Javascript per:
        -- Animazione risposta corretta/sbagliata con l'apparizione di una gif e colorazione dell'alternativa corretta
        -- Gestione visibilità delle div per giocare/timer in base all'ultima partita giocata
        -- Gestione/Aggiornamento real time del timer
        -- Visualizzazione carosello orizzontale per classifica su mobile
    
- stileDashboard.css
    + Foglio di stile per migliorare l'estetica del sito
    + media query per rendere responsive la pagina, adatta quindi anche a dispositivi mobile


## Profilo

⁠- ⁠profilo.html
    Pagina riguardante il profilo personale dell'utente
    + Navbar per muoversi all'interno del sito
    + Hamburger per rendere la navbar più agibile agli utenti da mobile
    + Sezione per visualizzare gli spot pubblicati e le risposte inerenti ad essi
    + Sezione per visualizzare alcune informazioni dell'utente

-profilo.css
    + Foglio di stile per migliorare l'estetica del sito
    + media query per rendere responsive la pagina, adatta quindi anche a dispositivi mobile

## Backend

- app.py
    Codice che gestisce qualsiasi attività relativa al backend del sito
    + Connessione al database
    + Definizione dei modelli delle tabelle presenti nel database
    + Controlli di autenticazione per il login
    + Recupero spot per la homepage
    + Inserimento spot
    + Inserimento risposte a spot
    + Scelta domanda random dalla tabella delle domande
    + Incremento punti a facoltà
    + Recupero eventi da tabella
    + Registrazione evento
    + Registrazione utente
    + Logout


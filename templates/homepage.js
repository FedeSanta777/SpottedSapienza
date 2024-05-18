document.addEventListener("DOMContentLoaded", function() {
    let hamburger = document.querySelector('.hamburger');
    let header = document.querySelector('.header');

    hamburger.addEventListener("click", function() {
        header.classList.toggle('open');
    });
});


// script.js
document.addEventListener('DOMContentLoaded', function() {
    const icons = document.querySelectorAll('.icon');
    const popups = document.querySelectorAll('.popup');

    icons.forEach(icon => {
        icon.addEventListener('click', function() {
            const popupId = this.getAttribute('data-popup');
            const popup = document.getElementById(popupId);

            // Chiudi tutti i popup aperti
            popups.forEach(p => p.style.display = 'none');
            icons.forEach(i => i.classList.remove('active'));

            // Mostra il popup corrente
            popup.style.display = 'block';
            this.classList.add('active');

            // Aggiungi l'overlay
            const overlay = document.createElement('div');
            overlay.classList.add('overlay');
            document.body.appendChild(overlay);

            // Chiudi il popup quando si clicca fuori
            overlay.addEventListener('click', function() {
                popup.style.display = 'none';
                icon.classList.remove('active');
                overlay.remove();
            });
        });
    });
});



document.addEventListener("DOMContentLoaded", function() {
    var isLoggedIn = false; // Imposta lo stato di accesso dell'utente

    // Verifica se l'utente è già autenticato (ad esempio, tramite cookie o sessione)
    // Imposta isLoggedIn a true o false di conseguenza

    if (isLoggedIn) {
        // L'utente è autenticato, mostra il pulsante per la pagina dell'utente
        document.getElementById("utentelog").style.display = "inline-block";
    } else {
        // L'utente non è autenticato, mostra i pulsanti di accesso e registrazione
        document.getElementById("sign").style.display = "inline-block";
    }

    // Aggiungi un gestore di eventi per il clic sul pulsante di accesso
    document.getElementById("sign").addEventListener("click", function() {
        // Simula l'accesso dell'utente (nel tuo caso, potresti implementare la logica di autenticazione)
        isLoggedIn = true;
        // Nascondi i pulsanti di accesso e registrazione
        document.getElementById("sign").style.display = "none";
        // Mostra il pulsante per la pagina dell'utente
        document.getElementById("utentelog").style.display = "inline-block";
    });

    // Aggiungi un gestore di eventi per il clic sul pulsante della pagina dell'utente
    document.getElementById("userpage").addEventListener("click", function() {
        // Reindirizza l'utente alla pagina dell'utente
        window.location.href = "paginautente";
    });
});
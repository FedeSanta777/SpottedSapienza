<script>
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
</script>
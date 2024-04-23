<?php
$servername = "localhost"; // o l'indirizzo IP del server del database
$username = "root";
$password = "";
$database = "spottedsapienza";

// Connessione al database
$connessione = new mysqli($servername, $username, $password, $database);

// Verifica connessione
if ($connessione->connect_error) {
    die("Connessione fallita: " . $connessione->connect_error);
}
echo "Connessione al database riuscita";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizza Messaggi</title>
</head>
<body>
    <h1>Messaggi sulla Bacheca</h1>
    <?php 
        
        
    // Query per recuperare i messaggi dalla tabella "bacheca"
    $sql = "SELECT * FROM bacheca";
    $result = $connessione->query($sql);

    if ($result->num_rows > 0) {
        // Output dei dati di ogni riga
        while($row = $result->fetch_assoc()) {
            // Creazione di una div per ogni messaggio
            echo "<div>";
            echo "<h2>" . $row["nome"] . "</h2>";
            echo "<p>" . $row["messaggio"] . "</p>";
            echo "</div>";
        }
    } else {
        echo "Nessun messaggio trovato nella bacheca.";
    }

    // Chiusura connessione
    $connessione->close();
    ?>
</body>
</html>
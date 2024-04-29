<?php
$conn=new mysqli("localhost", "root", "spottedsapienza"); //Crea connessione al database
if($conn->connect_error){
    die("Connessione fallita: ".$conn->connect_error);
}
//Prepara i parametri
$stmt=$conn->prepare("INSERT INTO utenti (nome, cognome, email, password, facolta) VALUES (?, ?, ?, ?, ?)");
$stmt->bind_param("sssss", $nome, $cognome, $email, $password, $facolta);

//Imposta i parametri e esegui
$nome=$_POST['nome'];
$cognome=$_POST['cognome'];
$email=$_POST['email'];
$password=$_POST['password'];
$facolta=$_POST['facolta'];

if($stmt->execute()){
    echo "Nuovo record creato con successo";
}else{
    echo "Errore: ", $stmt->error;
}
$stmt->close();
$conn->close();
?>
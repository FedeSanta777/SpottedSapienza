document.addEventListener("DOMContentLoaded", function() {
    let hamburger = document.querySelector('.hamburger');
    let header = document.querySelector('.header');

    hamburger.addEventListener("click", function() {
        header.classList.toggle('open');
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const icons = document.querySelectorAll('.icon');
    const popups = document.querySelectorAll('.popup');
    let overlay1;

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
            overlay1.classList.add('overlay1');
            document.body.appendChild(overlay1);

            // Chiudi il popup quando si clicca fuori
            overlay1.addEventListener('click', closePopup);
        });
    });

    document.querySelectorAll('.closebtn').forEach(btn => {
        btn.addEventListener('click', function() {
            closePopup();
        });
    });

    function closePopup() {
        popups.forEach(p => p.style.display = 'none');
        icons.forEach(i => i.classList.remove('active'));
        if (overlay1) {
            overlay1.remove();
        }
    }
});





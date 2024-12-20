$(document).ready(function() {
    $('#form-favoris').on('submit', function(e) {
        e.preventDefault(); // Empêche la soumission classique du formulaire

        // Récupération des données du formulaire
        let formData = {
            user: $('#user').val(),
            repas: $('#repas').val()
        };

        // Envoi de la requête AJAX
        $.ajax({
            url: '/favoris', // URL de la route Flask
            type: 'POST', // Méthode HTTP
            data: formData, // Données envoyées au serveur
            success: function(response) {
                // Affichage du message de succès
                $('#message').html(
                    `<p style="color: green;">${response.message} (Utilisateur: ${response.user}, Repas: ${response.repas})</p>`
                );
            },
            error: function(xhr) {
                // Affichage du message d'erreur
                let errorResponse = JSON.parse(xhr.responseText);
                $('#message').html(
                    `<p style="color: red;">Erreur: ${errorResponse.message}</p>`
                );
            }
        });
    });
});

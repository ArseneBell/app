$(document).ready(function() {
        $('#add').on('input', function() {
            $.ajax({
                url: '/api/ingredients', // URL de la route Flask
                type: 'GET', // Type de la requête
                dataType: 'json', // On attend un JSON en réponse
                success: function(data) {
                    console.log('Données reçues:', data);
                    $('#propositions').empty()
                    data.forEach(function(data) {
                        const ecrit = $('#add').val().toLowerCase(); 
                        if (data.nom.toLowerCase().startsWith(ecrit) && ecrit != ''){
                            $('#propositions').append(`<li class="proposition" onclick="document.getElementById('add').value=this.textContent">${data.nom}</li>`);
                        }
                        console.log(data.nom)
                    });
                    
                    
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Erreur:', textStatus, errorThrown);

                    $('#resultat').append('<p style="color:red;">Erreur de récupération des données</p>');

                }
            });
        });
});

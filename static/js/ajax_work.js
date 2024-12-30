$(document).ready(function() {



    // Empêche le rechargement de la page lors de la soumission du formulaire
    $('.form-add').on('submit', function(event) {
        event.preventDefault(); // Empêche le comportement par défaut du bouton de soumission

        // Récupère les données du formulaire
        let formData = $(this).serialize(); // Transforme les inputs en format URL-encoded (ex : "nom=John&email=john%40doe.com")
        
        
        // Affichage direct des valeurs des inputs
        $(this).find('input').each(function() {
            let nomChamp = $(this).attr('name');  // Récupère le nom du champ
            let valeurChamp = $(this).val();  // Récupère la valeur saisie par l'utilisateur
            console.log(valeurChamp)

            // Affiche la valeur dans la div #resultat
            let tab= `<tr class="row-ingredient" id = "${valeurChamp}"><th>
            <input type="checkbox" class="ingredient" name="ingredients" value="${valeurChamp}" checked>${valeurChamp}
            <button id="supprimer" style="background: transparent; border: none;" onclick="document.getElementById('${valeurChamp}').remove()"><i class="fa fa-trash me-3 text-primary"></i></button>
            </th></tr>`
            $('#liste-ingredients').append(tab);
            input = document.getElementById('add');
            input.value = '';

            var seen = {};
            $('#liste-ingredients').each(function() {
                var text = $(this).text();
                if(seen[text]){
                    $(this).remove();
                }else{
                    seen[text] = true;
                }
            })

        });


    });

});


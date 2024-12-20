

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    # Récupérer les informations de l'utilisateur
    user = User().get_by_id(id)  # Implémentez une méthode pour obtenir un utilisateur par ID
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        updated_user = User(
            id=id,
            nom=request.form.get('nom', ''),
            anneeNaiss=int(request.form.get('anneeNaiss', 0)),
            email=request.form.get('email', ''),
            sexe=request.form.get('sexe', ''),
            password=request.form.get('password', ''),
            tel=request.form.get('tel', ''),
            statut=request.form.get('statut', 'user'),
            preferences=request.form.get('preferences', '')
        )
        
        # Mettre à jour l'utilisateur
        if updated_user.Update(id):
            return redirect(url_for('user_profile', id=id))
        else:
            return "Erreur lors de la mise à jour", 400
    
    return render_template('user_profile.html', user=user)

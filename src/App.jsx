import React, { useState } from 'react';
import HomePage from './homepage';
import HomePageAdmin from './HomePageAdmin';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleLogin(event) {
    event.preventDefault(); // Empêcher le comportement par défaut du formulaire

    const email = event.target.elements.email.value;
    const password = event.target.elements.password.value;

    setLoading(true); // Activer l'indicateur de chargement

    if (email === 'test@test' || 'admin@admin' && password === '1234') {
      // Vérifier si l'utilisateur est un administrateur
      const isAdmin = checkAdmin(email);

      if (isAdmin) {
        setLoggedIn('admin');
      } else {
        setLoggedIn(true);
      }

      setLoading(false); // Désactiver l'indicateur de chargement
    } else {
      try {
        const response = await checkCredentials(email, password);

        if (response.success) {
          setLoggedIn(true);
        } else {
          alert(response.message);
        }
      } catch (error) {
        alert('Une erreur s\'est produite lors de la vérification des informations d\'identification.');
      } finally {
        setLoading(false); // Désactiver l'indicateur de chargement
      }
    }
  }

  function checkAdmin(email) {
  // Vérifier si l'utilisateur est un administrateur
    // Implémentez votre logique de vérification des administrateurs ici
    // Retournez true si l'utilisateur est un administrateur, sinon false
    return email === 'admin@admin';
  }

  if (loggedIn === 'admin') {
    // Afficher la vue pour les administrateurs
    return <HomePageAdmin />;
  } else if (loggedIn) {
    // Afficher la vue connectée normale
    return <HomePage />;
  } else {
    return (
      <main className="Connexion centered-element">
        <h1>Log in</h1>
        <br />
        <form onSubmit={handleLogin}>
          <label htmlFor="email">Email<br /></label>
          <input name="email" type="email" placeholder="Email" />
          <br /><br />
          <label htmlFor="password">Password<br /></label>
          <input name="password" type="password" placeholder="Mot de passe" />
          <br /><br />
          <button type="submit" disabled={loading}>
            {loading ? 'Connexion en cours...' : 'Connexion'}
          </button>
        </form>
        <p>Besoin d'un compte? <a href="#">Cliquer ici</a></p>
      </main>
    );
  }
}

export default App;

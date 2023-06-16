import React, { useState } from 'react';
import HomePage from './homepage';
import HomePageAdmin from './HomePageAdmin';
import { checkCredentials } from './api';

function checkAdmin(Email) {
  return Email === 'admin@admin';
}


function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  async function handleLogin(event) {
    event.preventDefault(); // Empêcher le comportement par défaut du formulaire

    const Email = event.target.elements.Email.value;
    const Password = event.target.elements.Password.value;

    if ((Email === 'test@test' || Email === 'admin@admin') && Password === '1234') {
      // Connection de base pour test acces page User vs Admin
      if ( checkAdmin(Email)) {
        setLoggedIn('admin');
      } else {
        setLoggedIn(true);
      }
    } else {
      // Connexion via SGBD
      try {
        const data = await checkCredentials(Email, Password);
        if (response.success) {
          if (data.isAdmin = true) {
            setLoggedIn('admin')
            ;
          } else {
            setLoggedIn(true);
          };
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert('Une erreur s\'est produite lors de la vérification des informations d\'identification.');
      } finally {
      }
    }
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
          <label htmlFor="Email">Email<br /></label>
          <input name="Email" type="Email" placeholder="Email" />
          <br /><br />
          <label htmlFor="Password">Password<br /></label>
          <input name="Password" type="Password" placeholder="Mot de passe" />
          <br /><br />
          <button type="submit"> Connexion
          </button>
        </form>
        <p>Besoin d'un compte? <a href="#">Cliquer ici</a></p>
      </main>
    );
  }
}

export default App;

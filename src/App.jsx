import React, { useState } from 'react';
import { checkCredentials, checkUser, createUser } from './Composant/API/api';
import HomePage from './Composant/Page/HomePage';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);

  // Fonction de connexion
  const handleLogin = async (event) => {
    event.preventDefault();

    const Email = event.target.elements.Email.value;
    const Password = event.target.elements.Password.value;

    try {
      const data = await checkCredentials(Email, Password);
      // Si l'utilisateur est un administrateur => loggedIn à 'admin'
      if (data.isAdmin === true) {
        setLoggedIn('admin');
      } else {
        setLoggedIn(true);
      }
    } catch (error) {
      alert('Utilisateur ou mot de passe incorrect');
    }
  };

  // Fonction d'inscription
  const handleInscription = async (event) => {
    event.preventDefault();

    const Email = event.target.elements.Email.value;
    const Password = event.target.elements.Password.value;
    const ConfirmPassword = event.target.elements.ConfirmPassword.value;

    // Vérification de l'email
    if (Email.endsWith('@goldenline.fr'))  {
        try {
          // Vérification de l'existence de l'utilisateur
        const response = await checkUser(Email);
          if (response.status === 200) {
            alert('Utilisateur déjà existant merci de vous connecter ou de demander un nouveau mot de passe par mail au sevice informatique');
          }
      } catch (error) {
        // Si l'utilisateur n'existe pas =>
        if (error.response && error.response.status === 404) {
          console.log('404 = Utilisateur inexistant => création');
          // Vérification de la correspondance des mots de passe
          if (Password !== ConfirmPassword) {
            alert('Les mots de passe ne correspondent pas');
          }
          else {
          await createUser(Email, Password);
          alert('Utilisateur créé')
          }
          
        } else {
          // Gérer les autres erreurs de requête ou de réseau
          alert('Une erreur est survenue');
        }
      }
    }
    else {
      alert('Vous devez utiliser un email @goldenline.fr');
    }
  };

    

// Fonction de changement de page vers la page d'inscription
  const handleRegisterClick = () => {
    setIsRegistering(true);
  };

  // Rendu conditionnel en fonction de l'état isRegistering = Page d'inscription
  if (isRegistering) {
    return (
      <main className="Connexion centered-element">
      <h1>Inscription</h1>
        <p style={{color: '#D4AF37'}}> Apres inscription votre compte doit etre activé par un administrateur</p>
      <form onSubmit={handleInscription}>
        <label htmlFor="Email">Email<br /></label>
        <input name="Email" type="email" placeholder="Email" />
        <br /><br />
        <label htmlFor="Password">Password<br /></label>
        <input name="Password" type="password" placeholder="Mot de passe" />
        <br />
        <label htmlFor="ConfirmPassword">Confirmation password<br /></label>
        <input name="ConfirmPassword" type="password" placeholder="Mot de passe" />
        <br />
        <button type="submit"> Valider </button>
        <br /><br />
        <button id="reset" type="reset" onClick={() => window.location.reload()}> Retour </button>
      </form>
      </main>
    );
  }

  // Rendu conditionnel en fonction de l'état loggedIn
  if (loggedIn === 'admin') {
    return <HomePage isAdmin={true} />;
  } else if (loggedIn === true) {
    return <HomePage isAdmin={false} />;
  } else {
    return (
      <main className="Connexion centered-element">
        <h1>Log in</h1>
        <br />
        <form onSubmit={handleLogin}>
          <label htmlFor="Email">Email<br /></label>
          <input name="Email" type="email" placeholder="Email" />
          <br /><br />
          <label htmlFor="Password">Password<br /></label>
          <input name="Password" type="password" placeholder="Mot de passe" />
          <br /><br />
          <button type="submit"> Connexion </button>
        </form>
        <br /><br />
          <p style={{color: '#D4AF37', margin:0 }}>Besoin d'un compte? 
          <br />
          <button style={{width: '25%' }}  onClick={handleRegisterClick}>Cliquer ici</button></p>
      </main>
    );
  }
}

export default App;
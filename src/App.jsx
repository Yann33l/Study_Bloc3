import React, { useState } from 'react';
import HomePage from './HomePage';
import { checkCredentials } from './Composant/API/api';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

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
        <p>Besoin d'un compte? <a href="#">Cliquer ici</a></p>
      </main>
    );
  }
}

export default App;
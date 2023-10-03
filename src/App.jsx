import React, { useState } from 'react';
import HomePage from './homepage';
import HomePageAdmin from './HomePageAdmin';
import { checkCredentials } from './api';

/*function checkAdmin(Email) {
  return Email === 'admin@admin';
}*/

  function App() {
    const [loggedIn, setLoggedIn] = useState(false);
  
    async function handleLogin(event) {
      event.preventDefault(); 

      const Email = event.target.elements.Email.value;
      const Password = event.target.elements.Password.value;

// Connection via API
      try { 
        const data = await checkCredentials(Email, Password);
        console.log(data)
        console.log(data.isAdmin)
        // Si l'utilisateur est un administrateur on passe LoggedIn à 'admin'
        if (data.isAdmin === true) 
        {
          setLoggedIn('admin');} 
        else {
          setLoggedIn(true);}} 
        // gestion des erreurs de authentification
        catch (error) {
        alert('Utilisateur ou mot de passe incorrect');
        }
      }
      
      
  
if (loggedIn === 'admin') {
    // Afficher la vue pour les administrateurs
  return <HomePageAdmin />;}
else if (loggedIn) {
    // Afficher la vue connectée normale
  return <HomePage />;}
else {
  // formulaire de connexion si utilisateur non connecté
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
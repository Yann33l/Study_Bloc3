function App() {
  return (
    <main class="Connexion centered-element" >
      <h1>Log in</h1>
      <br />
        <form>
          <label htmlfor="Email">Email<br /></label >
          <input type="text" placeholder="Login" />
          <br /><br />
          <label htmlfor="Password">Password<br /></label >
          <input type="password" placeholder="Mot de passe" />
          <br /><br />
          <button>Connexion</button>  
        </form>
        <p >Besoin d'un compte? <a href=""> Cliquer içi</a></p>
    </main>
  )
}

export default App;
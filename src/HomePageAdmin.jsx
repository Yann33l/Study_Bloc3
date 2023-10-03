function HomePage() {
    return(
    <body id="page" > 
      <header>
        <div id="logoheader">
            <img id="logo" alt="logo" src="/public/Image/logo/png/logo-no-background.png" height="120" />
        </div>
        <nav className="menu-nav">
            <ul>
                <li className="bouton">
                    <a href="/main.html">Acceuil</a>
                </li>
                <li className="bouton">
                    <a href="/Graphiques.html">Graphiques</a>
                </li>
                <li className="bouton">
                    <a href="/Exporter.html">Exporter</a>
                </li>
                <li className="bouton">
                    <a href="/Exporter.html">Admin</a>
                </li>
                <li className="bouton">
                    <a href="/index.html">Déconnexion</a>
                </li>
            </ul>
        </nav>
      </header>
      
      <main className="ZoneTravail">
          <div>
            <h1>Ici sera le graphe 1</h1>
            <h2>Ici le tableau du graphe 1</h2>

          </div>
          <div></div>
      </main>
      
      <footer>
        <p>réaliser par Yannick Leger</p></footer>
      </body>
    )
  }
  
  export default HomePage;
import React, { useState, useEffect} from 'react';
import Table1 from '../Table/Table1_depense_CSP_CatArticle';
import Table2 from '../Table/Table2_moyenne_pannier_par_CSP';
import Table3 from '../Table/Table3_Collecte';
import Table4 from '../Table/Table4_Ensemble';
import Graph1 from '../Graph/Graph1';
import Graph1_2 from '../Graph/Graph1-2';
import Graph2 from '../Graph/Graph2';



function HomePage({ isAdmin }) {
  const [content, setContent] = useState('default'); // État pour suivre le contenu

  // Fonctions pour gérer les clics des boutons et mettre à jour le contenu
  const handleButtonClick = (newContent) => {
    setContent(newContent);
  };


  // Contenu du main basé sur l'état
  let mainContent;
  switch (content) {
    case 'Graph1':
      mainContent = (
          <div >
            <Graph1  />
            <Graph1_2  />
          </div>)
          ;
      break;
    case 'Graph2':
      mainContent = (
          <div>
            <Graph2  />
          </div>)
          ;
      break;
    case 'Table1':
      mainContent = (
          <div>
            <h1>Dépense par cathegorie et par CSP</h1>
            <Table1  />
          </div>)
          ;
      break;
    case 'Table2':
      mainContent = (
          <div>
            <h1>moyenne du pannier par CSP</h1>
            <Table2  />
          </div>)
          ;
      break;
    case 'Table3':
      mainContent = (
          <div>
            <h1>Collecte</h1>
            <Table3  />
          </div>)
          ;
      break;
    case 'Table4':
      mainContent = (
          <div>
            <h1 style={{color: 'white'}}>Vue ensemble</h1>
            <Table4  />
          </div>)
          ;
      break;
    case 'acceuil':
    case 'default':
      mainContent = (
        <div>
          <h1>Ici sera le contenu de la page d'acceuil</h1>
          <h1>Ici sera le graphe 1</h1>
          <h2>Ici le tableau du graphe 1</h2>
        </div>
      );
      break;
    case 'graphiques':
      mainContent = (
        <div>
            <nav className="menu-nav">
              <ul>
                <li className="bouton" onClick={() => handleButtonClick('Graph1')}>
                  Dépenses 
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Graph2')}>
                  Paniers
                </li>
              </ul>
            </nav>
        </div>
      );
      break;
    case 'exporter':
      mainContent = (
        <div>
            <nav className="menu-nav">
              <ul>
                <li className="bouton" onClick={() => handleButtonClick('Table1')}>
                Dépense par cathegorie et par CSP
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table2')}>
                Moyenne du pannier par CSP
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table3')}>
                Collecte
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table4')}>
                Vue ensemble
                </li>
              </ul>
            </nav>
        </div>
      );
      break;
    case 'Admin':
      mainContent = (
        // Contenu pour le bouton "Administration"
        <h2>Ici la gestion des utilisateurs à creer</h2>
      );
      break;
  }

  return (
    <div>
      <header>
        <div id="logoheader">
{/*           <img
            id="logo"
            alt="logo" */}
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs" width="120" height="120" viewBox="0 0 120 120"><g transform="matrix(1,0,0,1,-0.6060606060606233,0.2522267206477409)"><svg viewBox="0 0 396 247" data-background-color="#ffffff" preserveAspectRatio="xMidYMid meet" height="623" width="1000" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="tight-bounds" transform="matrix(1,0,0,1,0.2400000000000091,-0.09999999999999432)"><svg viewBox="0 0 395.52 247.2" height="247.2" width="395.52"><g><svg></svg></g><g><svg viewBox="0 0 395.52 247.2" height="247.2" width="395.52"><g transform="matrix(1,0,0,1,75.54432,113.03227223737449)"><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998"><g><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998"><g><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998"><g><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998"><g id="textblocktransform"><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998" id="textblock"><g><svg viewBox="0 0 244.43135999999998 21.135455525251007" height="21.135455525251007" width="244.43135999999998"><g transform="matrix(1,0,0,1,0,0)"><svg width="244.43135999999998" viewBox="4 -28.799999237060547 333.6300048828125 28.849998474121094" height="21.135455525251007" data-palette-color="#f3a83c"><path d="M4-3.4L4-25.3 9.85-28.75 20.2-28.75 20.2-22.85 10.5-22.85 10.5-5.65 20-5.65 20 0 9.85 0 4-3.4ZM32.15-19.45L38.65-19.45 38.65-25.3 32.8-28.75 22.45-28.75 22.45-22.85 32.15-22.85 32.15-19.45ZM38.65-3.4L38.65-17.2 22.45-17.2 22.45-11.5 32.15-11.5 32.15-5.65 22.65-5.65 22.65 0 32.8 0 38.65-3.4ZM43.55-3.5L43.55-18.55 49.4-22 57.3-22 57.3-17.3 49.8-17.3 49.8-5.4 57.3-5.4 57.3-0.05 49.4-0.05 43.55-3.5ZM72.9-3.5L72.9-18.55 67.05-22 59.1-22 59.1-17.3 66.65-17.3 66.65-5.4 59.1-5.4 59.1-0.05 67.05-0.05 72.9-3.5ZM81.9 0.05L81.9-28.75 88.3-28.75 88.3 0.05 81.9 0.05ZM127.09-28.8L127.09 0 113.49 0 113.49-5.25 120.79-5.25 120.79-17.25 113.29-17.25 113.29-21.9 120.79-21.9 120.79-28.8 127.09-28.8ZM97.29-3.45L97.29-18.45 102.99-21.9 111.09-21.9 111.09-17.25 103.39-17.25 103.39-5.25 110.89-5.25 110.89 0 102.99 0 97.29-3.45ZM166.29-18.55L166.29-12.85 160.39-9.4 152.39-9.4 152.39-13.25 159.94-13.25 159.94-17.35 152.39-17.35 152.39-22.05 160.39-22.05 166.29-18.55ZM159.74-6.95L166.29-6.95 166.29-3.45 160.39 0 152.39 0 152.39-5.3 159.74-5.3 159.74-6.95ZM136.09-18.55L136.09-3.45 141.99 0 149.94 0 149.94-5.3 142.39-5.3 142.39-9.4 149.94-9.4 149.94-13.25 142.39-13.25 142.39-17.35 149.94-17.35 149.94-22.05 141.99-22.05 136.09-18.55ZM175.29-0.05L175.29-22 181.64-22 181.64-19.85 189.04-22 189.04-17.3 181.64-17.3 181.64-0.05 175.29-0.05ZM205.24-0.05L205.24-18.55 199.34-22 191.44-22 191.44-17.3 198.99-17.3 198.99-0.05 205.24-0.05ZM214.74-28.75L214.74-28.75 221.04-28.75 221.04-5.85 230.54-5.85 230.54 0 214.74 0 214.74-28.75ZM233.19-5.85L233.19-5.85 233.19 0 249.19 0 249.19-5.85 233.19-5.85ZM253.68-22L259.98-22 259.98 0.05 253.68 0.05 253.68-22ZM259.88-28.7L259.88-24.05 253.68-24.05 253.68-28.7 259.88-28.7ZM268.98-0.05L268.98-22 275.33-22 275.33-19.85 282.73-22 282.73-17.3 275.33-17.3 275.33-0.05 268.98-0.05ZM298.93-0.05L298.93-18.55 293.03-22 285.13-22 285.13-17.3 292.68-17.3 292.68-0.05 298.93-0.05ZM337.63-18.55L337.63-12.85 331.73-9.4 323.73-9.4 323.73-13.25 331.28-13.25 331.28-17.35 323.73-17.35 323.73-22.05 331.73-22.05 337.63-18.55ZM331.08-6.95L337.63-6.95 337.63-3.45 331.73 0 323.73 0 323.73-5.3 331.08-5.3 331.08-6.95ZM307.43-18.55L307.43-3.45 313.33 0 321.28 0 321.28-5.3 313.73-5.3 313.73-9.4 321.28-9.4 321.28-13.25 313.73-13.25 313.73-17.35 321.28-17.35 321.28-22.05 313.33-22.05 307.43-18.55Z" opacity="1" transform="matrix(1,0,0,1,0,0)" fill="#f3a83c" class="undefined-text-0" data-fill-palette-color="primary" id="text-0"></path></svg></g></svg></g></svg></g></svg></g></svg></g></svg></g></svg></g><path d="M226.887 107.032L226.887 41.3 391.487 41.3 391.487 205.9 226.887 205.9 226.887 140.168 228.793 140.168 228.793 203.994 389.581 203.994 389.581 43.206 228.793 43.206 228.793 107.032Z" fill="#f3a83c" stroke="transparent" data-fill-palette-color="primary"></path></svg></g><defs></defs></svg><rect width="395.52" height="247.2" fill="none" stroke="none" visibility="hidden"></rect></g></svg></g></svg>
 {/*            src="/public/Image/logo/png/logo-no-background.png"
            height="120"
          /> */}
        </div>
        <nav className="menu-nav">
          <ul>
            <li className="bouton" onClick={() => handleButtonClick('acceuil')}>
              Acceuil
            </li>
            <li className="bouton" onClick={() => handleButtonClick('graphiques')}>
              Graphiques
            </li>
            <li className="bouton" onClick={() => handleButtonClick('exporter')}>
              Exporter
            </li>
            {isAdmin && (
              <li className="bouton" onClick={() => handleButtonClick('Admin')}>
                Admin
              </li>
            )}
            <li className="bouton" onClick={() => window.location.reload()}>
              Déconnexion
            </li>
          </ul>
        </nav>
      </header>

      <main className="ZoneTravail">{mainContent}</main>

      <footer>
        <p>réalisé par Yannick Leger</p>
      </footer>
    </div>
  );
}

export default HomePage;

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
          <img
            id="logo"
            alt="logo"
            src="/public/Image/logo/png/logo-no-background.png"
            height="120"
          />
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

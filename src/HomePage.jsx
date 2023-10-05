import React, { useState, useEffect} from 'react';
import Table1 from './Composant/Table/Table1_depense_CSP_CatArticle';
import Table2 from './Composant/Table/Table2_moyenne_pannier_par_CSP';
import Table3 from './Composant/Table/Table3_Collecte';
import Table4 from './Composant/Table/Table4_Ensemble';



function HomePage({ isAdmin }) {
  const [content, setContent] = useState('default'); // État pour suivre le contenu

  // Fonctions pour gérer les clics des boutons et mettre à jour le contenu
  const handleButtonClick = (newContent) => {
    setContent(newContent);
  };


  // Contenu du main basé sur l'état
  let mainContent;
  switch (content) {
    case 'Table1':
      mainContent = (
          <div>
            <h1>Depenses_CSP_ClasseArticle</h1>
            <Table1  />
          </div>)
          ;
      break;
      case 'Table2':
        mainContent = (
            <div>
              <h1>moyenne_pannier_par_CSP</h1>
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
                  <h1>Ensemble</h1>
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
        // Contenu pour le bouton "Graphiques"
        <h1>be </h1>    );
      break;
    case 'exporter':
      mainContent = (
        <div>
            <nav className="menu-nav">
              <ul>
                <li className="bouton" onClick={() => handleButtonClick('Table1')}>
                  Tab1
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table2')}>
                  Tab2
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table3')}>
                  Tab3
                </li>
                <li className="bouton" onClick={() => handleButtonClick('Table4')}>
                  Tab4
                </li>
              </ul>
            </nav>
        </div>
      );
      break;
    case 'Admin':
      mainContent = (
        // Contenu pour le bouton "Administration"
        <h2>Ici la gestion des utilisateurs</h2>
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

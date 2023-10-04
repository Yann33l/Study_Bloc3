import React, { useState, useEffect} from 'react';


function HomePage({ isAdmin }) {
  const [content, setContent] = useState('default'); // État pour suivre le contenu
  const [products, setProducts] = useState([]); // État pour stocker les produits

  // Fonctions pour gérer les clics des boutons et mettre à jour le contenu
  const handleButtonClick = (newContent) => {
    setContent(newContent);
  };

  useEffect(() => {
    // Simulez ici l'obtention des produits de la base de données
    const productsFromDatabase = [
      { id: 1, name: 'Produit 1', description: 'Description du produit 1' },
      { id: 2, name: 'Produit 2', description: 'Description du produit 2' },
      // ... Ajoutez d'autres produits ici
    ];

    setProducts(productsFromDatabase);
  }, []);

  // Contenu du main basé sur l'état
  let mainContent;
  switch (content) {
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
        <h1>TableComponent </h1>    );
      break;
    case 'exporter':
      mainContent = (
        <div>
          <h1>Liste des produits</h1>
          <table>
            <thead>
              <tr>
                <th>Nom du produit</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td>{product.name}</td>
                  <td>{product.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
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

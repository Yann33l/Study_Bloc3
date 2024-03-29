import React, { useState } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

import Table1 from "../Table/Table1_depense_CSP_CatArticle";
import Table2 from "../Table/Table2_moyenne_pannier_par_CSP";
import Table3 from "../Table/Table3_Collecte";
import Table4 from "../Table/Table4_Ensemble";
import Table5 from "../Table/Table5_utilisateurs";
import Graph1 from "../Graph/Graph1";
import Graph1_2 from "../Graph/Graph1-2";
import Graph2 from "../Graph/Graph2";

function HomePage({ isAdmin }) {
  const [content, setContent] = useState("default");

  // Fonctions pour gérer les clics des boutons et mettre à jour le contenu
  const handleButtonClick = (newContent) => {
    setContent(newContent);
  };

  const handleGeneratePDF = () => {
    const content = document.getElementById("pdf-content");

    html2canvas(content, {
      backgroundColor: "rgb(54, 54, 54)",
      windowWidth: document.getElementById("pdf-content").offsetWidth,
      windowHeight: document.getElementById("pdf-content").offsetHeight,
    }).then((canvas) => {
      const pdf = new jsPDF(canvas.width > canvas.height ? "l" : "p");
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();

      pdf.addImage(canvas, "PNG", 0, 0, pdfWidth, pdfHeight);
      pdf.save("graphiques.pdf");
    });
  };

  // Contenu du main basé sur l'état
  let mainContent;
  switch (content) {
    case "acceuil":
    case "default":
      mainContent = (
        <div style={{ marginLeft: 30, color: "white" }}>
          <h1>Présentation de l'application</h1>
          <h3>Lien vers le code source de l'application</h3>
          <a
            style={{ color: "#D4AF37" }}
            href="https://github.com/Yann33l/Study_Bloc3"
            target="_blank"
            rel="bookmark"
          >
            https://github.com/Yann33l/Study_Bloc3
          </a>
          <br />
          <br />
          <p>
            Cette application permet de visualiser les données de ventes de
            l'entreprise Goldenline pour permetre l'étude des comportements des
            clients.
          </p>
          <p>
            Nous sommes constamment engagés dans l'amélioration de notre
            application. Voici les prochaines fonctionnalités que nous prévoyons
            de mettre en place :
          </p>
          <ul>
            <li>
              Remplacement du système de login actuel par un système de token :
              Cette mise à jour améliorera la sécurité de l'application en
              remplaçant le processus de connexion traditionnel par un système
              basé sur des jetons d'authentification. /Fait
            </li>
            <li>
              Ajout d'une sélection multiple des lignes pour exporter les
              tableaux : Cette fonctionnalité permettra aux utilisateurs de
              sélectionner plusieurs lignes de données à la fois, simplifiant
              ainsi le processus d'exportation de tableaux pour des analyses
              ultérieures. /Fait
            </li>
          </ul>
          <h2>Mon projet professionel</h2>
          <p>
            Mon ambition professionnelle est de poursuivre mon apprentissage du
            développement web par le biais d'un contrat d'alternance, de
            préférence dans le domaine de la santé. Travailler dans le secteur
            de la santé est particulièrement important pour moi, car cela me
            permettrait de combiner ma passion pour le développement web et
            l’analyse de données dans un domaine d’utilité public générant
            toujours plus de données à analyser. Je suis déterminé à continuer à
            acquérir des compétences et à contribuer de manière significative au
            secteur de la santé.{" "}
          </p>
        </div>
      );
      break;

    case "graphiques":
      mainContent = (
        <div>
          <nav className="sous_menu-nav">
            <ul>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Graph1")}
              >
                Dépenses
              </li>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Graph2")}
              >
                Paniers
              </li>
            </ul>
          </nav>
        </div>
      );
      break;
    case "Graph1":
      mainContent = (
        <>
          <div id="pdf-content" style={{ width: "800px" }}>
            <Graph1 />
            <Graph1_2 />
          </div>
          {isAdmin && (<button onClick={() => handleGeneratePDF("Generate PDF")}>
            generate PDF
          </button>)}
        </>
      );
      break;
    case "Graph2":
      mainContent = (
        <>
          <div id="pdf-content" style={{ width: 1200 }}>
            <Graph2 />
          </div>
          {isAdmin && (<button onClick={() => handleGeneratePDF("Generate PDF")}>
            generate PDF
          </button>)}
        </>
      );
      break;

    case "exporter":
      mainContent = (
        <div>
          <nav className="sous_menu-nav">
            <ul>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Table1")}
              >
                Dépense par cathegorie et par CSP
              </li>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Table2")}
              >
                Moyenne du pannier par CSP
              </li>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Table3")}
              >
                Collecte
              </li>
              <li
                className="bouton"
                onClick={() => handleButtonClick("Table4")}
              >
                Vue ensemble
              </li>
            </ul>
          </nav>
        </div>
      );
      break;
    case "Table1":
      mainContent = (
        <div>
          <h1 style={{ color: "white" }}>Dépense par cathegorie et par CSP</h1>
          <Table1 />
        </div>
      );
      break;
    case "Table2":
      mainContent = (
        <div>
          <h1 style={{ color: "white" }}>moyenne du pannier par CSP</h1>
          <Table2 />
        </div>
      );
      break;
    case "Table3":
      mainContent = (
        <div>
          <h1 style={{ color: "white" }}>Collecte</h1>
          <Table3 />
        </div>
      );
      break;
    case "Table4":
      mainContent = (
        <div>
          <h1 style={{ color: "white" }}>Vue ensemble</h1>
          <Table4 />
        </div>
      );
      break;

    case "Admin":
      mainContent = (
        <div>
          <h1 style={{ color: "white" }}>Gestion des utilisateurs </h1>
          <Table5 />
        </div>
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
            src="/Image/logo/png/logo-no-background2.png"
            height="120"
          />
        </div>
        <nav className="menu-nav">
          <ul>
            <li className="bouton" onClick={() => handleButtonClick("acceuil")}>
              Acceuil
            </li>
            <li
              className="bouton"
              onClick={() => handleButtonClick("graphiques")}
            >
              Graphiques
            </li>
            <li
              className="bouton"
              onClick={() => handleButtonClick("exporter")}
            >
              Exporter
            </li>
            {isAdmin && (
              <li className="bouton" onClick={() => handleButtonClick("Admin")}>
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

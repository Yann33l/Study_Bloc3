const dataTableStyle = {
    height: 700,
    width: "90%",
    margin: "auto",
    backgroundColor: "#ffffff",
    color: "#000000",
    border: "none",
    borderRadius: "5px",
    boxShadow: "0px 0px 5px 0px rgba(0,0,0,0.75)",
  };

const columnsTable1 = [
{ field: "id", headerName: "id", width: 10 },
{ field: "CSP", headerName: "CSP", width: 300 },
{ field: "depenses", headerName: "depenses", width: 150 },
{ field: "categorie_vetement", headerName: "categorie_vetement", width: 150 },
];

const columnsTable2 = [
    { field: "id", headerName: "id", width: 10 },
    { field: "CSP", headerName: "CSP", width: 300 },
    { field: "Moy_panier", headerName: "Moy_panier", width: 150 },
];

const columnsTable3 = [
    { field: "id", headerName: "id", width: 10 },
    { field: "collecte", headerName: "collecte", width: 150 },
    { field: "num_panier", headerName: "num_panier", width: 150 },
    { field: "Prix_panier", headerName: "Prix_panier", width: 150 },
    { field: "montant", headerName: "montant", width: 150 },
    { field: "categorie_article", headerName: "categorie_article", width: 150 },
    ];

const columnsTable4 = [
    { field: "id", headerName: "id", width: 10 },
    { field: "Client", headerName: "Client", width: 150 },
    { field: "Nbr enfants", headerName: "Nbr enfants", width: 150 },
    { field: "CSP", headerName: "CSP", width: 300 },
    { field: "id_panier", headerName: "id_panier", width: 150 },
    { field: "date achat", headerName: "date achat", width: 150 },
    { field: "id_article", headerName: "id_article", width: 150 },
    { field: "quantite_article", headerName: "quantite_article", width: 150 },
    { field: "prix_vente", headerName: "prix_vente", width: 150 },
    { field: "cout", headerName: "cout", width: 150 },
    { field: "categorie", headerName: "categorie", width: 150 },
    ];
    export { dataTableStyle, columnsTable1, columnsTable2, columnsTable3, columnsTable4 };

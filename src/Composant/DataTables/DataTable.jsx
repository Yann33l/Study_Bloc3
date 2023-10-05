// Ajout de la librairie React-Chartjs-2
// npm install --save react-chartjs-2 chart.js
// import { en fonction du graph } from 'react-chartjs-2';
// pour l'affichage de graphiques

// https://mui.com/x/react-data-grid/getting-started/#installation
import { DataGrid} from '@mui/x-data-grid';


// pour l'affichage de tableau
const TableComponent = () => {
    const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nom', headerName: 'Nom', width: 150 },
    { field: 'description', headerName: 'Description', width: 250 },
    // Ajoutez d'autres colonnes en fonction de vos données
  ];

    const rows = [
    { id: 1, nom: 'Snow', description: 'Jon', },
    { id: 2, nom: 'Lannister', description: 'Cersei', },
    { id: 3, nom: 'Lannister', description: 'Jaime', },
    { id: 4, nom: 'Stark', description: 'Arya', },
    { id: 5, nom: 'Targaryen', description: 'Daenerys', },

    ];
    return (
        <DataGrid
        rows={rows}
        columns={columns}
        loading={loading}
        />
    );
}

export default TableComponent;



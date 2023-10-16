import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import axios from 'axios';
import React, { useEffect } from "react";
import { API_URL } from '../API/api';
import { columnsTable5, dataTableStyle } from './TableStyle';

const Table5 = () => {
  const [data, setData] = React.useState([]);

  useEffect(() => {
    const getCollecte = async () => {
      try {
        const response = await axios.get(`${API_URL}/users/`);
        const responseData = response.data;
        setData(responseData);
      } catch (error) {
        console.error(error);
      }
    };

    getCollecte();
  }, []);

  const getRowId = (row) => row.Email;

const handleCheckBoxChange = async (event, params) => {
    const newValue = event.target.checked;
    const updatedData = data.map((row) => {
        if (row.Email === params.row.Email) {
            return {
                ...row,
                [params.field]: newValue,
            };
        } return row;
    });

  // Envoyer la mise à jour à la base de données via une requête HTTP
  // Voir si possible de passer par un objet
    if (params.field === "Admin") {
        try {
            await axios.put(`${API_URL}/editUserAdmin/?email=${params.row.Email}&admin=${newValue}`);
            setData(updatedData);
        } catch (error) {
            console.error("Erreur lors de la mise à jour : ", error);
        }
        }
    if (params.field === "Autorisation") {
        try {
            await axios.put(`${API_URL}/editUserAutorisation/?email=${params.row.Email}&autorisation=${newValue}`);
            setData(updatedData);
        } catch (error) {
            console.error("Erreur lors de la mise à jour : ", error);
        }
    }
    };


  const renderCheckCell = (params) => {
    return (
      <input
        type="checkbox"
        checked={params.value}
        onChange={(event) => handleCheckBoxChange(event, params)}
      />
    );
  };

  // Modifiez les colonnes "Admin" et "Autorisation" pour utiliser la fonction de rendu personnalisée "renderCheckCell"
  const columns = columnsTable5.map((column) => {
    if (column.field === "Admin" || column.field === "Autorisation") {
      return {
        ...column,
        renderCell: renderCheckCell,
      };
    }
    return column;
  });

  return (
    <DataGrid
      rows={data}
      columns={columns}
      loading={!data.length}
      sx={dataTableStyle}
      getRowId={getRowId}
      slots={{ toolbar: GridToolbar }}
    />
  );
};

export default Table5;

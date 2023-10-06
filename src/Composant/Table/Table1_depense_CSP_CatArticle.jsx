import React, { useEffect } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { columnsTable1, dataTableStyle } from "./TableStyle";
import axios from 'axios'
import {API_URL} from '../API/api'



const Table1 = () => {
  const [data, setData] = React.useState([]);

    // Methode 1: fetch
 /* useEffect(() => {
      fetch(`${API_URL}/depenses_CSP_ClasseArticle`)
        .then((response) => response.json())
        .then((json) => {
        const dataWithIds = json.results.map((row, index) => ({
          ...row,
          id: index + 1,
        }));
        setData(dataWithIds);
      });
    }, []);*/
   
    //Methode 2: axios
  useEffect(() => {
    
    const getDepenses_CSP_ClasseArticle = async () => {
      try {
        const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`);
        const responseData = response.data;
        setData(responseData)
        const dataWithIds = responseData.results.map((row, index) => ({
            ...row,
            id: index + 1, 
          }));
          setData(dataWithIds); 
      } catch (error) {
        console.error(error);
      }
    };
  
    getDepenses_CSP_ClasseArticle(); 
  }, []);

  return (
    <DataGrid
      rows={data}
      columns={columnsTable1}
      loading={!data.length}
      sx={dataTableStyle}
      getRowId={(row) => row.id} 
      slots={{ toolbar: GridToolbar }}
    />
  );
};

export default Table1;


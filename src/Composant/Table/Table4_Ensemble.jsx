import React, { useEffect } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { dataTableStyle, dataTableStyle2, columnsTable4 } from './TableStyle';
import axios from 'axios'
import {API_URL} from '../API/api'


const Table4 = () => {
  const [data, setData] = React.useState([]);

  useEffect(() => {
    const getCollecte = async () => {
      try {
        const response = await axios.get(`${API_URL}/visu_ensemble/`);
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
  
    getCollecte(); 
  }, []);

  return (
    <DataGrid
      rows={data}
      columns={columnsTable4}
      loading={!data.length}
      sx={dataTableStyle2}
      getRowId={(row) => row.id} 
      slots={{ toolbar: GridToolbar }}
    />
  );
};

export default Table4;


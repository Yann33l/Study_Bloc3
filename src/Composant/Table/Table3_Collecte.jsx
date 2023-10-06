import React, { useEffect } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { columnsTable3, dataTableStyle } from "./TableStyle";
import axios from 'axios'
import {API_URL} from '../API/api'


const Table3 = () => {
  const [data, setData] = React.useState([]);

  useEffect(() => {
    const getCollecte = async () => {
      try {
        const response = await axios.get(`${API_URL}/Collecte/`);
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
      columns={columnsTable3}
      loading={!data.length}
      sx={dataTableStyle}
      getRowId={(row) => row.id} 
    />
  );
};

export default Table3;


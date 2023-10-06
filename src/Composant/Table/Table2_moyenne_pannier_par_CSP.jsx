import React, { useEffect } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { columnsTable2, dataTableStyle } from "./TableStyle";
import axios from 'axios'
import {API_URL} from '../API/api'


const Table2 = () => {
    const [data, setData] = React.useState([]);
  

    useEffect(() => {
      const getmoyenne_pannier_par_CSP = async () => {
        try {
          const response = await axios.get(`${API_URL}/moyenne_pannier_par_CSP/`);
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
    
      getmoyenne_pannier_par_CSP(); 
    }, []);
  
    return (
      <DataGrid
        rows={data}
        columns={columnsTable2}
        loading={!data.length}
        sx={dataTableStyle}
        getRowId={(row) => row.id} 
      />
    );
  };
  
  export default Table2;
  
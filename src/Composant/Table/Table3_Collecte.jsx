import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import axios from "axios";
import React, { useEffect } from "react";
import { API_URL } from "../API/api";
import { getAuthHeader } from "../API/token";
import { columnsTable3, dataTableStyle } from "./TableStyle";

const Table3 = () => {
  const [data, setData] = React.useState([]);
  const authHeader = getAuthHeader();

  useEffect(() => {
    const getCollecte = async () => {
      try {
        const response = await axios.get(`${API_URL}/Collecte/`, authHeader);
        const responseData = response.data;
        setData(responseData);
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
      slots={{ toolbar: GridToolbar }}
      checkboxSelection
    />
  );
};

export default Table3;

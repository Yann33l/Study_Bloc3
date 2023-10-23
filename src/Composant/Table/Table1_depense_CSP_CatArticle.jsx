import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import axios from "axios";
import React, { useEffect } from "react";
import { API_URL } from "../API/api";
import { getAuthHeader } from "../API/token";
import { columnsTable1, dataTableStyle } from "./TableStyle";

const Table1 = () => {
  const [data, setData] = React.useState([]);
  const authHeader = getAuthHeader();

  const getDepenses_CSP_ClasseArticle = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/depenses_CSP_ClasseArticle/`,
        authHeader
      );
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
  useEffect(() => {
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
      checkboxSelection
    />
  );
};

export default Table1;

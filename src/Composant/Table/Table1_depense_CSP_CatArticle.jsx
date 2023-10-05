import React, { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
  { field: "id", headerName: "id", width: 150 },
  { field: "CSP", headerName: "CSP", width: 150 },
  { field: "depenses", headerName: "depenses", width: 150 },
  { field: "categorie_vetement", headerName: "categorie_vetement", width: 150 },
];

const dataTableStyle = {
  height: 700,
  width: "80%",
  margin: "auto",
  backgroundColor: "#ffffff",
  color: "#000000",
  border: "none",
  borderRadius: "5px",
  boxShadow: "0px 0px 5px 0px rgba(0,0,0,0.75)",
};

const Table1 = () => {
  const [data, setData] = React.useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/depenses_CSP_ClasseArticle")
      .then((response) => response.json())
      .then((json) => {
      const dataWithIds = json.results.map((row, index) => ({
        ...row,
        id: index + 1, // Vous pouvez utiliser un autre mécanisme pour générer un ID unique
      }));
      setData(dataWithIds);
    });
  }, []);

  return (
    <DataGrid
      rows={data}
      columns={columns}
      loading={!data.length}
      sx={dataTableStyle}
      getRowId={(row) => row.id} 
    />
  );
};

export default Table1;

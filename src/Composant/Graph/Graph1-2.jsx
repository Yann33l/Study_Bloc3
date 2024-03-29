import React, { useEffect, useState } from "react";
import axios from 'axios';
import { API_URL } from '../API/api';
import { Bar } from 'react-chartjs-2';
import { generateRandomColors } from './Graph_style';
import { getAuthHeader } from "../API/token";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );

  // Options du graphique
const chartOptions = {
responsive: true, 
maintainAspectRatio: false,
plugins: {
    legend: {
        display: true,
        position: 'bottom',
        labels: {
            font: {size: 16},
            color: 'white' 
            },
    },
},
layout: {
    padding: {
        left: 30, 
        right: 30, 
        top: 50, 
        bottom: 100 
    },
},        
scales: {
    x: {
        title: {
            display: true,
            text: 'Catégories',
            color: 'white',
            font: {size: 20}
        },
        ticks: {
            font: {size: 15},
            color: 'white', 
        },
    },
    y: {
        beginAtZero: true,
        title: {
            display: true,
            text: 'Dépenses',
            color: 'white',
            font: {size: 20}, 
        },
        ticks: {
            font: {size: 15},
            color: 'white', 
        },
    }, 
},
};

const Graph1_2 = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [],
    });
    const authHeader = getAuthHeader()

    useEffect(() => {
        const getDepenses_CSP_ClasseArticle = async () => {
            try {
                const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`, authHeader);
                const responseData = response.data;

                if (responseData.results) {
                    const uniqueCategories = [...new Set(responseData.results.map((row) => row.categorie_vetement))];
                    const uniqueCSPValues = [...new Set(responseData.results.map((row) => row.CSP))];

                    const datasets = uniqueCSPValues.map((csp) => {
                        const dataValues = uniqueCategories.map((category) => {
                            const filteredData = responseData.results.filter((row) => row.CSP === csp && row.categorie_vetement === category);
                            return filteredData.reduce((acc, curr) => acc + curr.depenses, 0);
                        });

                        return {
                            label: csp,
                            backgroundColor: generateRandomColors(1),
                            data: dataValues,
                        };
                    });

                    setData({
                        labels: uniqueCategories,
                        datasets: datasets,
                    });
                }
            } catch (error) {
                console.error(error);
            }
        };

        getDepenses_CSP_ClasseArticle();
    }, []);



    return (
        <div style={{ height: "600px", color: 'white'}}>
            <h1 style={{textAlign: 'center'}}>Répartition des dépenses par catégorie de vêtement pour chaque CSP</h1>
            <Bar data={data} options={chartOptions} />
        </div>
    );
}

export default Graph1_2;

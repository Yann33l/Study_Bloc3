import React, { useEffect, useState } from "react";
import axios from 'axios';
import { API_URL } from '../API/api';
import { Bar } from 'react-chartjs-2';
import { generateRandomColors } from './Graph_style';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { getAuthHeader } from "../API/token";

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

    layout: {
        padding: {
            left: 20,
            right: 20,
            top: 50,
            bottom: 100,
        },
    },
    plugins: {
        legend: {
            display: false,
        },
    },
    scales: {
        x: {display: true,
            title: {
                display: false,
            },
            ticks: {
                font: {
                    size: 15,
                },
                color: 'white', 
            },
        },
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Moyenne Panier',
                font: {
                    size: 20,
                },
                color: 'white', 

            },
            ticks: {
                font: {
                    size: 16,
                },
                color: 'white', 

            },
        },
    },
};


const Graph2 = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: [],
        }],
    });
    const authHeader = getAuthHeader()


    useEffect(() => {
        const getMoyennePannierParCSP = async () => {
            try {
                const response = await axios.get(`${API_URL}/moyenne_pannier_par_CSP/`, authHeader);
                const responseData = response.data;

                if (responseData.results) {
                    const uniqueCSPValues = [...new Set(responseData.results.map((row) => row.CSP))];
                    const dataValues = uniqueCSPValues.map((CSP) => {
                        // Filtrer les données pour le CSP actuel
                        const filteredData = responseData.results.filter((row) => row.CSP === CSP);
                        // Calculer la moyenne des Moy_panier pour ce CSP
                        const moyennePannier = filteredData.reduce((acc, row) => acc + row.Moy_panier, 0) / filteredData.length;
                        return moyennePannier;
                    });


                    setData({
                        labels: uniqueCSPValues,
                        datasets: [{
                            data: dataValues,
                            backgroundColor: generateRandomColors(uniqueCSPValues.length),
                        }],
                    });
                }
            } catch (error) {
                console.error(error);
            }
        };

        getMoyennePannierParCSP();
    }, []);


    return (
        <div style={{ height: "500px", color: 'white' }}>
            <h1 style={{textAlign: 'center'}}>Moyenne panier par classe socioprofessionelle </h1>
            <Bar data={data} options={chartOptions} />
        </div>
    );
}

export default Graph2;

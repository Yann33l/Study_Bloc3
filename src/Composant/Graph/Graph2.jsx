import React, { useEffect, useState } from "react";
import axios from 'axios';
import { API_URL } from '../API/api';
import { Bar } from 'react-chartjs-2';
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

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,

    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 50,
            bottom: 100,
        },
        background: {
            color: 'white', // Couleur de fond du graphique
        },
    },
    scales: {
        x: {
            title: {
                display: false,
            },
            ticks: {
                font: {
                    size: 16,
                    color: 'black', // Couleur du texte de l'axe x
                },
            },
        },
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Moyenne Panier',
                font: {
                    size: 20,
                    color: 'black',
                },
            },
            ticks: {
                font: {
                    size: 16,
                    color: 'black',
                },
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

    useEffect(() => {
        const getMoyennePannierParCSP = async () => {
            try {
                const response = await axios.get(`${API_URL}/moyenne_pannier_par_CSP/`);
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

                    // Générer des couleurs aléatoires pour les barres
                    const backgroundColors = generateRandomColors(uniqueCSPValues.length);

                    setData({
                        labels: uniqueCSPValues,
                        datasets: [{
                            data: dataValues,
                            backgroundColor: backgroundColors,
                        }],
                    });
                }
            } catch (error) {
                console.error(error);
            }
        };

        getMoyennePannierParCSP();
    }, []);

    const generateRandomColors = (count) => {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
            colors.push(color);
        }
        return colors;
    };

    return (
        <div style={{ height: "500px", color: 'white' }}>
            <h2>Répartition des dépenses par CSP et moyenne panier</h2>
            <Bar data={data} options={chartOptions} />
        </div>
    );
}

export default Graph2;

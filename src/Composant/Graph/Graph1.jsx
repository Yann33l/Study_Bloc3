import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import React, { useEffect, useState } from "react";
import axios from 'axios';
import { API_URL } from '../API/api';
import { generateRandomColors } from './Graph_style';
import { getAuthHeader } from "../API/token";

ChartJS.register(ArcElement, Tooltip, Legend);

// Options du graphique
const chartOptions = {
    responsive: true, // Désactiver la réponse automatique
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'bottom', // Position de la légende (peut être 'top', 'bottom', 'left' ou 'right')
            labels: {
                font: {
                    size: 16, // Taille de la police de la légende
                },
                color: 'white', // Couleur du texte de la légende
            },
        },
    },
    layout: {
        padding: {
            left: 0, // Marge à gauche
            right: 0, // Marge à droite
            top: 50, // Marge en haut
            bottom: 100, // Marge en bas
        },
    },
};


// Composant du graphique
const Graph1 = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [
            {
                data: [],
                backgroundColor: [], 
            },
        ],
    });
    const authHeader = getAuthHeader()

        // Fonction pour regrouper les dépenses par CSP identique
        const groupByCSP = (data) => {
            const groupedData = {};
            data.forEach((row) => {
                if (!groupedData[row.CSP]) {
                    groupedData[row.CSP] = [];
                }
                groupedData[row.CSP].push(row);
            });
            return groupedData;
        };

        // Fonction pour récupérer les dépenses par CSP
        const getDepenses_CSP_ClasseArticle = async () => {
            try {
                const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`, authHeader);
                const responseData = response.data;

                if (responseData.results) {
                    const groupedData = groupByCSP(responseData.results);

                    const labels = Object.keys(groupedData);
                    // Calculer le total des dépenses pour chaque CSP
                    const values = Object.values(groupedData).map(group => group.reduce((acc, curr) => acc + curr.depenses, 0));

                    setData({
                        labels: labels,
                        datasets: [
                            {
                                data: values,
                                backgroundColor: generateRandomColors(labels.length),
                            },
                        ],
                    });
                }
            } catch (error) {
                console.error(error);
            }
        };

    useEffect(() => {
        getDepenses_CSP_ClasseArticle();
    }, []);

            
    return (
        <div style={{ height: "500px", color: 'white' }}>
            <h1 style={{textAlign: 'center'}}>Dépenses par classe socioprofessionelle (CSP)</h1>
            <Doughnut data={data}  options={chartOptions}/>
        </div>
    );
}

export default Graph1;

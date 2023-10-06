import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import React, { useEffect, useState } from "react";
import axios from 'axios';
import { API_URL } from '../API/api';

ChartJS.register(ArcElement, Tooltip, Legend);

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


const Graph1 = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [
            {
                data: [],
                backgroundColor: [], // Vous pouvez personnaliser les couleurs ici
            },
        ],
    });

    useEffect(() => {
        const getDepenses_CSP_ClasseArticle = async () => {
            try {
                const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`);
                const responseData = response.data;

                // Assurez-vous que responseData.results est défini avant de mapper
                if (responseData.results) {
                    const groupedData = groupByCSP(responseData.results);

                    const labels = Object.keys(groupedData);
                    const values = Object.values(groupedData).map(group => group.reduce((acc, curr) => acc + curr.depenses, 0));
                    const backgroundColor = generateRandomColors(labels.length);

                    setData({
                        labels: labels,
                        datasets: [
                            {
                                data: values,
                                backgroundColor: backgroundColor,
                            },
                        ],
                    });
                }
            } catch (error) {
                console.error(error);
            }
        };

        getDepenses_CSP_ClasseArticle();
    }, []);

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

    // Fonction pour générer des couleurs aléatoires
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
            <h1>Dépenses par classe socioprofessionelle</h1>
            <Doughnut data={data}  options={chartOptions}/>
        </div>
    );
}

export default Graph1;

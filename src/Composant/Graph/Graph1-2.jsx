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
scales: {
    x: {
        title: {
            display: true,
            text: 'Catégories',
        },
    },
    y: {
        beginAtZero: true,
        title: {
            display: true,
            text: 'Dépenses',
        },
    },
},
};

const Graph1_2 = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [],
    });

    useEffect(() => {
        const getDepenses_CSP_ClasseArticle = async () => {
            try {
                const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`);
                const responseData = response.data;

                if (responseData.results) {
                    const uniqueCategories = [...new Set(responseData.results.map((row) => row.categorie_vetement))];
                    const uniqueCSPValues = [...new Set(responseData.results.map((row) => row.CSP))];

                    const categoryColors = generateRandomColors(uniqueCategories.length);

                    const datasets = uniqueCSPValues.map((csp, cspIndex) => {
                        const dataValues = uniqueCategories.map((category) => {
                            const filteredData = responseData.results.filter((row) => row.CSP === csp && row.categorie_vetement === category);
                            return filteredData.reduce((acc, curr) => acc + curr.depenses, 0);
                        });

                        return {
                            label: csp,
                            backgroundColor: categoryColors[cspIndex],
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

    const generateRandomColors = (count) => {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
            colors.push(color);
        }
        return colors;
    };


    return (
        <div style={{ height: "500px", color: 'white'}}>
            <h2>Répartition des dépenses par catégorie de vêtement pour chaque CSP</h2>
            <Bar data={data} options={chartOptions} />
        </div>
    );
}

export default Graph1_2;

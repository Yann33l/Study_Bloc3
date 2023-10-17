// Fonction pour générer des couleurs aléatoires
const generateRandomColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
        colors.push(color);
    }
    return colors;
};


const Colors = {
    CSP1: "rgba(255, 99, 132, 0.7)",
    CSP2: "rgba(54, 162, 235, 0.7)",
    CSP3: "rgba(255, 206, 86, 0.7)",
    CSP4: "rgba(75, 192, 192, 0.7)",
    CSP5: "rgba(153, 102, 255, 0.7)",
    CSP6: "rgba(255, 159, 64, 0.7)",
    CSP7: "rgba(255, 99, 132, 0.7)",
    CSP8: "rgba(54, 162, 235, 0.7)",
  };
export { Colors, generateRandomColors };

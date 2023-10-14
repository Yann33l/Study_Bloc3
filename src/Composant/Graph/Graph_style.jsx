// Fonction pour générer des couleurs aléatoires
const generateRandomColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
        colors.push(color);
    }
    return colors;
};
export { generateRandomColors };

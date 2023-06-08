import axios from 'axios';

const API_URL = 'http://localhost:3000'; // Remplacez par l'URL de votre API

export const checkCredentials = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    return response.data;
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }
};


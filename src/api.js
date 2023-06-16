import axios from 'axios';

const API_URL = 'http://0.0.0.0:8000'; // Remplacez par l'URL de votre API

export const checkCredentials = async (Email, Password) => {
  try {
    const response = await axios.post(`${API_URL}/users/`, { Email, Password });
    const data = response.data;

    // Vérification de la colonne "Admin" dans la réponse de l'API
    if (data.admin === 1) {
      data.isAdmin = true;
    } else {
      data.isAdmin = false;
    }

    return data;
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }
};
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'; 

export const checkCredentials = async (Email, Password) => {

  //Connexion à l'application
  try { 
    const requestData = {
      params : {
        email: Email,
        password: Password,
      }};

    const response = await axios.get(`${API_URL}/Connexion/`, requestData);
    const data = response.data;

// Vérification de la colonne "Admin" dans la réponse de l'API
    if (data.Admin === 1) {
      data.isAdmin = true;} 
    else {
      data.isAdmin = false;}
    return data;} 
  catch (error) {
    console.error('erreur etape 1 Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }};

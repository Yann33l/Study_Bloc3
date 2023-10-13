import axios from 'axios'

export let API_URL;

if (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') {
    // Environnement local
    API_URL = 'http://127.0.0.1:8000';
} else {
    // Environnement en ligne
    API_URL = 'https://goldenline.osc-fr1.scalingo.io';
    
}
//Local
//export const API_URL = 'http://127.0.0.1:8000'; 

//Scalingo
//export const API_URL = 'https://goldenline.osc-fr1.scalingo.io';


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

// Vérification de la colonne "Admin" dans la réponse de l'API pour connection page utilisateur / admin
    if (data.Admin === 1) {
      data.isAdmin = true;} 
    else {
      data.isAdmin = false;}
    return data;} 
  catch (error) {
    console.error('erreur etape 1 Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }};

  export const getDepenses_CSP_ClasseArticle = async () => {
    try {
      const response = await axios.get(`${API_URL}/depenses_CSP_ClasseArticle/`);
      const responseData = response.data;
      return responseData;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
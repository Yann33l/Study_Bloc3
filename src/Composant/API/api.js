import axios from 'axios';

export let API_URL;

if (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') {
    // Environnement local
    API_URL = 'http://127.0.0.1:8000';
} else {
    // Environnement en ligne
    API_URL = 'https://goldenline.osc-fr1.scalingo.io';
    
}

export const checkUser = async (Email) => {
  try {
    const requestData = {
      params : {
        email: Email,
      }
    };
    const response = await axios.get(`${API_URL}/userByEmail/`, requestData);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// !!!! a essayer de remplacer par un const requestDatas = {params : {email: Email, password: Password,}}; mais pose probleme car le serveur n'attend pas un objet. A CORRIGER 
// besoin d'aide +++
/* export const createUser = async (Email, Password) => {
  try { 
    const response = await axios.post(`${API_URL}/create_users1/?email=${Email}&password=${Password}`);
    const data = response.data;
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
} */

export const createUser = async (Email, Password) => {
  try {
    const response = await axios.post(`${API_URL}/create_users/`,{
      Email: Email,
      Password: Password,
      First_connexion: null,
      Last_change_password: null,
      Admin: false,
      Autorisation: false,
    });
    const data = response.data;
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export const checkCredentials = async (Email, Password) => {

  //Connexion à l'application
  try { 
/*     const requestData = {
      params : {
        email: Email,
        password: Password,
      }};

    const response = await axios.get(`${API_URL}/Connexion/`, requestData); */
    const requestData =  {
        Email: Email,
        Password: Password,
      };

    const response = await axios.post(`${API_URL}/Connexion2/`, requestData);
    const data = response.data;
    if (data.Autorisation === true) {
      if (data.Admin === true) {
        data.isAdmin = true;
        data.isAutorized = true; 
        return data;}
      else {
        data.isAdmin = false;
        data.isAutorized = true; 
        return data;} 
    }
    else {
      data.isAuth = false;
      return data;}
    }
  
// Vérification de la colonne "Admin" dans la réponse de l'API pour connection page utilisateur / admin

  catch (error) {
    console.error('erreur etape 1 Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }};


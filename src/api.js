import axios from 'axios'
import { useParams, Link, useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000'; 

export const checkCredentials = async (Email, Password) => {
  // Fonction de hashage du mot de passe
  const HashedPassword = Password+'123'
  console.log(HashedPassword)

  //Connexion à l'application
  try { 
  const requestData = {
    params : {
      email: Email,
      password: HashedPassword,
    }};
  const response = await axios.get(`${API_URL}/Connexion/`, requestData);
  const data = response.data;

// Vérification de la colonne "Admin" dans la réponse de l'API
    if (data.Admin === 1) {
      data.isAdmin = true;
    } 
    else {
      data.isAdmin = false;
    }
    console.log('retrun data.isAdmin = '+ data.isAdmin)

    return data;
  } 
  catch (error) {
    console.error('erreur etape 1 Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }};

import axios from 'axios'
import { useParams, Link, useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000'; 

export const checkCredentials = async (Email, Password) => {
  try {  console.log("is ok")
    const response = await axios.post(`${API_URL}/autentifiaction/`,{Email} );
    console.log('ok')
    const data = response.data;

    // Vérification de la colonne "Admin" dans la réponse de l'API
    if (data.admin === 1) {
      data.isAdmin = true;
    } else {
      data.isAdmin = false;
    }

    return data;
  } 
  catch (error) {
    console.error('erreur etape 1 Une erreur s\'est produite lors de la vérification des informations d\'identification :', error);
    throw error;
  }};

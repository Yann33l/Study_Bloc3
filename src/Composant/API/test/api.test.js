import axios from 'axios';
import { checkCredentials } from '../api';
import jest from 'jest-mock';

jest.mock('axios');

describe('checkCredentials', () => {
  const email = 'test@example.com';
  const password = 'password';
  const authToken = 'authToken';
  const authHeader = {
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  };
  const userInfo = {
    id: 1,
    name: 'John Doe',
    email: 'test@example.com',
  };

  beforeEach(() => {
    axios.post.mockReset();
  });

  it('should return user info when credentials are correct', async () => {
    axios.post.mockResolvedValueOnce({ data: { access_token: authToken } });
    axios.post.mockResolvedValueOnce({ data: userInfo });

    const result = await checkCredentials(email, password);

    expect(axios.post).toHaveBeenCalledTimes(2);
    expect(axios.post).toHaveBeenCalledWith(`${API_URL}/Connexion/`, {
      Email: email,
      Password: password,
    });
    expect(axios.post).toHaveBeenCalledWith(`${API_URL}/user/info/`, null, authHeader);
    expect(result).toEqual(userInfo);
  });

  it('should throw an error when credentials are incorrect', async () => {
    const error = new Error('Unauthorized');
    error.response = { status: 401 };
    axios.post.mockRejectedValueOnce(error);

    await expect(checkCredentials(email, password)).rejects.toThrow(error);

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith(`${API_URL}/Connexion/`, {
      Email: email,
      Password: password,
    });
  });

  it('should throw an error when there is a network error', async () => {
    const error = new Error('Network Error');
    axios.post.mockRejectedValueOnce(error);

    await expect(checkCredentials(email, password)).rejects.toThrow(error);

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith(`${API_URL}/Connexion/`, {
      Email: email,
      Password: password,
    });
  });
});
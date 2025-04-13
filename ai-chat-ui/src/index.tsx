import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

// Auth0 configuration - use environment variables from root directory
const domain = process.env.REACT_APP_AUTH0_DOMAIN || '';
const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID || '';
const redirectUri = window.location.origin;

// Only log in development mode
if (process.env.NODE_ENV === 'development') {
  console.log('Auth0 Configuration being used:', {
    domain: domain ? 'Configured' : 'Missing',
    clientId: clientId ? 'Configured' : 'Missing',
    redirectUri
  });

  // Additional check for .env location
  console.log('Environment variable source check:', {
    isDevelopment: process.env.NODE_ENV === 'development',
    apiUrl: process.env.REACT_APP_API_URL,
    hasRootEnv: Boolean(process.env.REACT_APP_AUTH0_DOMAIN)
  });
}

// Ensure required environment variables are set
if (!domain || !clientId) {
  console.error('Auth0 configuration is incomplete. Please check your environment variables in the root .env file.');
}

root.render(
  <React.StrictMode>
     <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: redirectUri,
        scope: "openid profile email"
      }}
      cacheLocation="localstorage"
    >
      <App />
    </Auth0Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

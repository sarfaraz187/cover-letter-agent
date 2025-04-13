import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

// Auth0 configuration - use environment variables
const domain = process.env.REACT_APP_AUTH0_DOMAIN || '';
const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID || '';

// Only log in development mode
if (process.env.NODE_ENV === 'development') {
  console.log('Auth0 Configuration being used:', {
    domain: domain ? 'Configured' : 'Missing',
    clientId: clientId ? 'Configured' : 'Missing',
  });
}

// Ensure required environment variables are set
if (!domain || !clientId) {
  console.error('Auth0 configuration is incomplete. Please check your environment variables.');
}

root.render(
  <React.StrictMode>
     <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: window.location.origin,
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

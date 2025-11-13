import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

import { QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider } from 'antd'
import { queryClient } from './api/config';
import { BrowserRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ConfigProvider 
        theme={{
          token: {
            colorPrimary: '#543D3F',
            colorInfo: '#543D3F',
          },
        }}>
          <BrowserRouter>
            <App/>
          </BrowserRouter>
        </ConfigProvider>
    </QueryClientProvider>
  </React.StrictMode>
)

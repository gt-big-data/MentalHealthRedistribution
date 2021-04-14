import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider } from '@chakra-ui/react';
import 'focus-visible/dist/focus-visible';

import App from './components/App';

ReactDOM.render(
  <ChakraProvider>
    <App />
  </ChakraProvider>
  , document.getElementById('root'));
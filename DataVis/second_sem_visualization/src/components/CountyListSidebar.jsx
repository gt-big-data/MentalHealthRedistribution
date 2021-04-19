import React, { useContext } from 'react';
import { Flex, Button, Fade, Box } from '@chakra-ui/react';

import { CountyContext } from '../contexts';
import CountyListEntry from './CountyListEntry';

const Sidebar = () => {
  // eslint-disable-next-line no-unused-vars
  const { selectedCounties, setSelectedCounties } = useContext(CountyContext);

  console.log(selectedCounties);

  return (
    <Fade in={selectedCounties.length > 0}>
      { selectedCounties.length < 1 ? <></> :
        <Flex direction='column' position='fixed' h='80vh' w='20vw' top='10vh' right='5vw' backgroundColor='#fff' borderRadius='20px' py={5} px={5} boxShadow='0px 4px 10px rgba(106, 166, 255, 0.4)'>
          <Box boxShadow='inset 0px 4px 10px rgba(106, 166, 255, 0.4)' height='40%' borderRadius='20px' overflowY='scroll'>
            {
              selectedCounties.map((county, i) => {
                console.log(county);
                return <CountyListEntry key={i} county={county} />;
              })
            }
          </Box>
          <Button position='absolute' bottom='70px' w='80%' left='50%' transform='translateX(-50%)' backgroundColor='#6AA6FF' color='#fff' onClick={() => {}}>
                Calculate Optimal Locations
          </Button>
          <Button position='absolute' bottom='20px' w='80%' left='50%' transform='translateX(-50%)' backgroundColor='#ff7d86' color='#fff' onClick={() => {setSelectedCounties([]);}}>
                Clear List
          </Button>
        </Flex>
      }
    </Fade>
  );
};

export default Sidebar;
import React, { useContext } from 'react';
import { Flex, Button, Heading, Text, Fade } from '@chakra-ui/react';
import { CloseIcon } from '@chakra-ui/icons';

import { CountyContext } from '../contexts';

const Sidebar = () => {
  // eslint-disable-next-line no-unused-vars
  const { selectedCounty, setSelectedCounty } = useContext(CountyContext);

  return (
    <Fade in={selectedCounty.length > 0}>
      { selectedCounty.length < 1 ? <></> :
        <Flex direction='column' position='fixed' h='80vh' w='20vw' top='10vh' left='5vw' backgroundColor='#fff' borderRadius='20px' py={5} px={5} boxShadow='0px 4px 10px rgba(106, 166, 255, 0.4)'>
          <>
            <Heading>{`${selectedCounty[0].properties.name} County`}</Heading>
            <Text>{selectedCounty[0].index}</Text>
            <Button position='absolute' bottom='5' mx='auto' left='50%' transform='translateX(-50%)' variant='unstyled' onClick={() => {setSelectedCounty([]);}} >
              <CloseIcon/>
            </Button>
          </>
        </Flex>
      }
    </Fade>
  );
};

export default Sidebar;
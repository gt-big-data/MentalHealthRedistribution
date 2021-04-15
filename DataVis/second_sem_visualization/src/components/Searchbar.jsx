import React, { useContext } from 'react';
import { Input, Button, InputRightElement, InputGroup } from '@chakra-ui/react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { motion } from 'framer-motion';

import { CountyContext } from '../contexts';

const MotionGroup = motion(InputGroup);

const variants = {
  notSelected: { left: '20vw' },
  selected: { left: '30vw' },
};

const Searchbar = () => {
  const { selectedCounty } = useContext(CountyContext);

  return (
    <MotionGroup 
      animate={selectedCounty.length < 1 ? 'notSelected' : 'selected'}
      variants={variants}
      whileHover={{ scale: 1.05 }}
      position='fixed' top='10vh' left={selectedCounty.length < 1 ? '20vw' : '30vw'} w='60vw'>
      <Input placeholder='Search by County' borderRadius={50} backgroundColor='#fff' borderWidth={0} boxShadow='0px 4px 10px rgba(106, 166, 255, 0.4)' />
      <InputRightElement width="6rem">
        <Button borderRadius={50} width='6rem' backgroundColor='#6AA6FF'>
          <FontAwesomeIcon icon={faSearch} color='#fff' />
        </Button>
      </InputRightElement>
    </MotionGroup>
  );
};

export default Searchbar;
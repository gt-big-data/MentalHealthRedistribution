/* eslint-disable react/prop-types */
import React, { useContext } from 'react';
import { Flex, Text, Button } from '@chakra-ui/react';
import { CloseIcon } from '@chakra-ui/icons';

import { CountyContext } from '../contexts';

const CountyListEntry = (props) => {
  const { removeFromSelectedCounties } = useContext(CountyContext);
  return (
    <Flex direction='row' h='50px' w='100%' borderBottom='1px' px='10px' borderBottomColor='rgba(106, 166, 255, 0.4)'>
      <Text w='85%' lineHeight='50px'>{`${props.county.properties.name} County`}</Text>
      <Button my='auto' variant='unstyled' onClick={() => {removeFromSelectedCounties(props.county);}} >
        <CloseIcon/>
      </Button>
    </Flex>
  );
};

export default CountyListEntry;
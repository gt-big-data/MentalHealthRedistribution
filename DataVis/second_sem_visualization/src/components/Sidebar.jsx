import React, { useContext, useEffect, useState } from 'react';
import { Flex, Button, Heading, Text, Fade } from '@chakra-ui/react';
import { CloseIcon } from '@chakra-ui/icons';
import axios from 'axios';

import { CountyContext } from '../contexts';

const url = 'http://mental-health-redistribution.uc.r.appspot.com';

const Sidebar = () => {
  // eslint-disable-next-line no-unused-vars
  const {
    selectedCounty,
    setSelectedCounty,
    addToSelectedCounties,
  } = useContext(CountyContext);

  const [countyData, setCountyData] = useState({});

  useEffect(() => {
    const getData = async () => {
      const response = await axios.get(
        `${url}/county_info?county=${selectedCounty[0].properties.name}%20County,%20${selectedCounty[0].state}`,
      );
      setCountyData(response.data);
      console.log(response.data);
    };
    if (selectedCounty[0]) {
      getData();
    }
  }, [selectedCounty[0]]);

  return (
    <Fade in={selectedCounty.length > 0}>
      {selectedCounty.length < 1 ? (
        <></>
      ) : (
        <Flex
          direction="column"
          position="fixed"
          h="80vh"
          w="20vw"
          top="10vh"
          left="5vw"
          backgroundColor="#fff"
          borderRadius="20px"
          py={5}
          px={5}
          boxShadow="0px 4px 10px rgba(106, 166, 255, 0.4)"
        >
          <>
            <Heading>{`${selectedCounty[0].properties.name} County`}</Heading>
            <Text>{`State: ${selectedCounty[0].state}`}</Text>
            <br />
            <Text>
              {`Mental Health Need Classification: ${countyData['Mental Health Need Classification']}`}
            </Text>
            <br />
            <Text>
              {`2014 Mortality Rates From Alcohol Use: ${countyData['2014 Mortality Rates From Alcohol Use']}`}
            </Text>
            <Text>
              {`2014 Mortality Rates From Drug Use: ${countyData['2014 Mortality Rates From Drug Use ']}`}
            </Text>
            <Text>
              {`2014 Mortality Rates From Self-Harm: ${countyData['2014 Mortality Rates From Self-Harm']}`}
            </Text>
            <Text>
              {`2014 Mortality Rates From Violence: ${countyData['2014 Mortality Rates From Violence']}`}
            </Text>
            <Button
              position="absolute"
              bottom="60px"
              w="80%"
              left="50%"
              transform="translateX(-50%)"
              backgroundColor="#6AA6FF"
              color="#fff"
              onClick={() => {
                addToSelectedCounties(selectedCounty[0]);
              }}
            >
              Add to List
            </Button>
            <Button
              position="absolute"
              bottom="5"
              mx="auto"
              left="50%"
              transform="translateX(-50%)"
              variant="unstyled"
              onClick={() => {
                setSelectedCounty([]);
              }}
            >
              <CloseIcon />
            </Button>
          </>
        </Flex>
      )}
    </Fade>
  );
};

export default Sidebar;

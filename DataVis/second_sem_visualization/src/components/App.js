import React from 'react';
import { Heading, ListItem, UnorderedList, Flex, Link } from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';

const App = () => {
  return (
    <Flex w='60%' direction='column' mx='auto'>
      <Heading as='h1' fontSize='32px'>Mental Health Resource Classification</Heading>
      <Heading as='h2' fontSize='24px'>Overview</Heading>
      <UnorderedList ml={10}>
        <ListItem>Counties are classified from (0-9), Higher value = poor mental health resource availability</ListItem>
        <ListItem>Classified based on historical statistics from lots of metrics, including self-harm drug/alcohol abuse just to name a few.
        </ListItem>
      </UnorderedList>
      <Heading as='h2' fontSize='24px'>Extension/Next Steps</Heading>
      <UnorderedList ml={10}>
        <ListItem>Unsupervised approach: Use neural networks to predict optimal locations for new mental health centers based on these classifications as well as location of current mental health centers</ListItem>
      </UnorderedList>
      <Heading as='h2' fontSize='24px'>Resources/Source Code</Heading>
      <UnorderedList ml={10}>
        <ListItem><Link href='https://docs.google.com/document/d/150Hc7q6I4S-W8EjiD32tP6UhliiDqbFmeJZ3ZjDodmI/edit?usp=sharing' color='teal.500' isExternal>Project Proposal<ExternalLinkIcon mx="2px" /></Link></ListItem>
        <ListItem><Link href='https://github.com/gt-big-data/MentalHealthRedistribution' color='teal.500' isExternal>GitHub Repository<ExternalLinkIcon mx='2px' /></Link></ListItem>
      </UnorderedList>
    </Flex>
  );
};

export default App;
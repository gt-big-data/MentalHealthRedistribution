/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Heading, ListItem, UnorderedList, Flex, Link, Box, Input, Button, InputRightElement, InputGroup } from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';
import d3Legend from 'd3-svg-legend';
import * as d3 from 'd3';
import { feature, mesh } from 'topojson-client';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
// import {
//   ComposableMap,
//   Geographies,
//   Geography,
// } from 'react-simple-maps';

import countyData from '../data/us.json';
import csvData from '../data/data.csv';

class App extends Component {
  constructor() {
    super();
    this.state = {
      classificationData: [],
      state: []
    };
  }

  componentDidMount() {
    this.drawLegend();
    this.drawMap();
  }

  drawLegend() {
    const color = d3.scaleQuantize([0, 9], d3.schemeBlues[9]);
    // var quantize = d3
    //   .scaleLinear()
    //   .domain([0, 9])
    //   .range(
    //     [, 'rgb(71, 187, 94)']
    //   );

    var svg = d3.select('#legend');

    svg
      .append('g')
      .attr('class', 'legendQuant')
      .attr('transform', 'translate(20,20)');

    var legend = d3Legend
      .legendColor()
      // .labelFormat()
      // .useClass(true)
      .title('Legend')
      .titleWidth(100)
      .cells(10)
      .shapeWidth(40)
      .orient('vertical')
      .scale(color);

    svg.select('.legendQuant').call(legend);
  }

  async processCSV(){
    const csv = await d3.csv(csvData);
    const mapData = new Map(csv.map(({id, classification}) => [id, classification]));
    const states = new Map(countyData.objects.states.geometries.map(d => [d.id, d.properties]));
    this.setState({ classificationData: mapData, stateData: states });
  }

  async drawMap() {
    const svg = d3.select('#map');
    const path = d3.geoPath();

    const color = d3.scaleQuantize([0, 9], d3.schemeBlues[9]);

    await this.processCSV();

    svg
      .selectAll('.county')
      .data(feature(countyData, countyData.objects.counties).features)
      .join('path')
      .attr('fill', d => color(this.state.classificationData.get(d.id)))
      .attr('d', path)
      .append('title')
      .text(d => `${d.properties.name}, ${this.state.stateData.get(d.id.slice(0, 2)).name}\n${parseInt(this.state.classificationData.get(d.id)) + 1}`);

    svg
      .append('path')
      .datum(mesh(countyData, countyData.objects.states, (a, b) => a !== b))
      .attr('fill', 'none')
      .attr('stroke', 'white')
      .attr('stroke-linejoin', 'round')
      .attr('d', path);
  }

  render() {
    return (
      <Box backgroundColor='#EBF3FF' height='100%'>
        <Flex w='60%' direction='column' mx='auto'>
          <InputGroup mt={5}>
            <Input placeholder='Search by County' borderRadius={50} backgroundColor='#fff' borderWidth={0} boxShadow='0px 4px 10px rgba(106, 166, 255, 0.4)' />
            <InputRightElement width="6rem">
              <Button borderRadius={50} width='6rem' backgroundColor='#6AA6FF'>
                <FontAwesomeIcon icon={faSearch} color='#fff' />
              </Button>
            </InputRightElement>
          </InputGroup>
          {/* <svg id="legend" style={{ height: 230 }}></svg> */}
          <svg id="map" style={{ width: 1000, height: 600, marginBottom: 30 }}></svg>
        </Flex>
      </Box>
    );
  }
}

export default App;

/* eslint-disable no-unused-vars */
import React, { Component, useContext, useEffect, useState } from 'react';
import { Heading, ListItem, UnorderedList, Flex, Link, Box, Input, Button, InputRightElement, InputGroup } from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';
import d3Legend from 'd3-svg-legend';
import * as d3 from 'd3';
import { feature, mesh } from 'topojson-client';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
// import {
//   ComposableMap,
//   Geographies,
//   Geography,
// } from 'react-simple-maps';

import Sidebar from './Sidebar';

import countyData from '../data/us.json';
import csvData from '../data/data.csv';
import Searchbar from './Searchbar';
import { CountyContext } from '../contexts';

class App extends Component {
  constructor() {
    super();
    this.state = {
      classificationData: new Map(),
      stateData: new Map(),
      selectedCounty: [],
      mentalCenters: []
    };
    this.setSelectedCounty = this.setSelectedCounty.bind(this);
  }

  async componentDidMount() {
    const getData = async () => {
      const data = await axios.get('http://127.0.0.1:5000/potential_mental_health_centers');
      this.setState({mentalCenters: data.data});
    };
    await getData();
    // drawLegend();
    this.drawMap();
    console.log(this.state.mentalCenters);
  }

  setSelectedCounty(county) {
    this.setState({selectedCounty: county});
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

  async processCSV() {
    const csv = await d3.csv(csvData);
    const mapData = new Map(csv.map(({id, classification}) => [id, classification]));
    const states = new Map(countyData.objects.states.geometries.map(d => [d.id, d.properties]));
    console.log(mapData);
    this.setState({classificationData: mapData});
    this.setState({stateData: states});
  }

  async drawMap() {
    const svg = d3.select('#map');
    const path = d3.geoPath();

    const color = d3.scaleQuantize([0, 8], d3.schemeBlues[9]);

    await this.processCSV();

    svg
      .selectAll('.county')
      .data(feature(countyData, countyData.objects.counties).features)
      .join('path')
      .on('click', (e, feature) => {
        this.setState({
          selectedCounty: [{
            ...feature,
            index: parseInt(this.state.classificationData.get(feature.id)) + 1
          }]
        });
      })
      .attr('fill', d => color(this.state.classificationData.get(d.id)))
      .attr('d', path)
      .append('title')
      .text(d => `${d.properties.name}, ${this.state.stateData.get(d.id.slice(0, 2)).name}\n${parseInt(this.state.classificationData.get(d.id)) + 1}`);
    
    // svg
    //   .selectAll('.center')
    //   .data(this.state.mentalCenters)
    //   .enter().append('circle')
    //   .style('stroke', 'gray')
    //   .style('fill', 'red')
    //   .attr('height', 10000)
    //   .attr('width', 10000)
    //   .attr('x', 21)
    //   .attr('y', -150);

    svg
      .append('path')
      .datum(mesh(countyData, countyData.objects.states, (a, b) => a !== b))
      .attr('fill', 'none')
      .attr('stroke', 'white')
      .attr('stroke-linejoin', 'round')
      .attr('d', path);
  }

  render() {
    const {selectedCounty} = this.state;
    const {setSelectedCounty} = this;

    return (
      <CountyContext.Provider value={{selectedCounty, setSelectedCounty}}>
        <Box backgroundColor='#EBF3FF' height='100vh'>
          <Flex w='60%' direction='column' mx='auto'>
            <Searchbar />
            {/* <svg id="legend" style={{ height: 230 }}></svg> */}
            <svg id="map" style={{ width: 1000, height: 600, marginBottom: 30 }}></svg>
            <Sidebar />
          </Flex>
        </Box>
      </CountyContext.Provider>
    );
  }
}

export default App;

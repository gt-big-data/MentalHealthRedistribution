/* eslint-disable no-unused-vars */
import React, { Component, useContext, useEffect, useState } from 'react';
import { Heading, ListItem, UnorderedList, Flex, Link, Box, Input, Button, InputRightElement, InputGroup, Spinner, Center } from '@chakra-ui/react';
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
import CountyListSidebar from './CountyListSidebar';

import countyData from '../data/us.json';
import geojsonData from '../data/usGeojson.json';
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
      selectedCounties: [],
      potentialMentalCenters: [],
      currMentalCenters: []
    };
    this.setSelectedCounty = this.setSelectedCounty.bind(this);
    this.setSelectedCounties = this.setSelectedCounties.bind(this);
    this.addToSelectedCounties = this.addToSelectedCounties.bind(this);
    this.removeFromSelectedCounties = this.removeFromSelectedCounties.bind(this);
  }

  async componentDidMount() {
    const getData = async () => {
      const currData = await axios.get('http://127.0.0.1:5000/current_mental_health_centers');
      const potentialData = await axios.get('http://127.0.0.1:5000/potential_mental_health_centers');
      this.setState({potentialMentalCenters: potentialData.data, currMentalCenters: currData.data});
    };
    await getData();
    // drawLegend();
    this.drawMap();
  }

  setSelectedCounty(county) {
    this.setState({selectedCounty: county});
  }

  setSelectedCounties(counties) {
    this.setState({selectedCounties: counties});
  }

  addToSelectedCounties(county) {
    let counties = this.state.selectedCounties;
    if (!counties.includes(county)) {
      counties.push(county);
    }
    this.setState({selectedCounties: counties});
  }

  removeFromSelectedCounties(county) {
    let counties = this.state.selectedCounties;
    counties.splice(counties.indexOf(county), 1);
    this.setState({ selectedCounties: counties });
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
    this.setState({classificationData: mapData});
    this.setState({stateData: states});
  }

  scale(scaleFactor, offsetX, offsetY) {
    return d3.geoTransform({
      point: function(x, y) {
        this.stream.point(offsetX + x * scaleFactor, offsetY + y  * scaleFactor);
      }
    });
  }

  async drawMap() {
    let width = 960;
    let height = 500;

    // let zoom = d3.zoom().on('zoom', (event) => {
    //   svg.style('stroke-width', 1.5 / event.transform.k + 'px');
    //   // g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")"); // not in d3 v4
    //   svg.attr('transform', event.transform); // updated for d3 v4
    // });

    const svg = d3.select('#map');
    var projection = d3
      .geoAlbersUsa()
      .scale(1300)
      .translate([487.5, 305]);

    const path = d3.geoPath().projection(this.scale(1, 225, 30));

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
    
    svg
      .append('path')
      .datum(mesh(countyData, countyData.objects.states, (a, b) => a !== b))
      .attr('fill', 'none')
      .attr('stroke', 'white')
      .attr('stroke-linejoin', 'round')
      .attr('d', path);

    svg
      .selectAll('.curr')
      .data(this.state.currMentalCenters)
      .enter()
      .append('circle')
      .style('stroke', '#bfd6ff')
      .style('fill', '#669cff')
      .attr('r', 3)
      .attr('d', path)
      .attr('cx', (d) => {
        if (projection([d.lon, d.lat]) !== null) {
          return projection([d.lon, d.lat])[0] + 225;
        }
      })
      .attr('cy', (d) => {
        if (projection([d.lon, d.lat]) !== null) {
          return projection([d.lon, d.lat])[1] + 30;
        }
      });
    
    svg
      .selectAll('.potential')
      .data(this.state.potentialMentalCenters)
      .enter()
      .append('circle')
      .style('stroke', '#ffdfba')
      .style('fill', '#ffad4f')
      .attr('r', 3)
      .attr('d', path)
      .attr('cx', (d) => {
        return projection([d.lon, d.lat])[0] + 225;
      })
      .attr('cy', (d) => {
        return projection([d.lon, d.lat])[1] + 30;
      });
  }

  render() {
    const {selectedCounty, selectedCounties} = this.state;
    const {setSelectedCounty, setSelectedCounties, addToSelectedCounties, removeFromSelectedCounties } = this;

    return (
      <CountyContext.Provider value={{selectedCounty, setSelectedCounty, selectedCounties, setSelectedCounties, addToSelectedCounties, removeFromSelectedCounties }}>
        <Flex w='100vw' h='100vh' backgroundColor='#ebf3ff' direction='column'>
          <Searchbar />
          {/* <svg id="legend" style={{ height: 230 }}></svg> */}
          {this.state.potentialMentalCenters.length === 0 && this.state.currMentalCenters.length === 0 ? <Spinner position='absolute' top='50%' left='50%' transform='translate(-50%, -50%)' size='xl' color="#6AA6FF"/> : <svg id="map" style={{ width: '100vw', height: '100vh', marginBottom: 30 }}></svg>}
          <Sidebar />
          <CountyListSidebar />
        </Flex>
      </CountyContext.Provider>
    );
  }
}

export default App;

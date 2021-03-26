import React, { Component } from 'react';
import { Heading, ListItem, UnorderedList, Flex, Link } from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';
import d3Legend from 'd3-svg-legend';
import * as d3 from 'd3';
import { feature, mesh } from 'topojson-client';
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
      .text(d => `${d.properties.name}, ${this.state.stateData.get(d.id.slice(0, 2)).name}\n${this.state.classificationData.get(d.id)}`);

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
      <Flex w="60%" direction="column" mx="auto">
        <Heading as="h1" fontSize="32px">
          Mental Health Resource Classification
        </Heading>
        <Heading as="h2" fontSize="24px">
          Overview
        </Heading>
        <UnorderedList ml={10}>
          <ListItem>
            Counties are classified from (0-9), Higher value = poor mental
            health resource availability
          </ListItem>
          <ListItem>
            Classified based on historical statistics from lots of metrics,
            including self-harm drug/alcohol abuse just to name a few.
          </ListItem>
        </UnorderedList>
        <Heading as="h2" fontSize="24px">
          Extension/Next Steps
        </Heading>
        <UnorderedList ml={10}>
          <ListItem>
            Unsupervised approach: Use neural networks to predict optimal
            locations for new mental health centers based on these
            classifications as well as location of current mental health centers
          </ListItem>
        </UnorderedList>
        <Heading as="h2" fontSize="24px">
          Resources/Source Code
        </Heading>
        <UnorderedList ml={10}>
          <ListItem>
            <Link
              href="https://docs.google.com/document/d/150Hc7q6I4S-W8EjiD32tP6UhliiDqbFmeJZ3ZjDodmI/edit?usp=sharing"
              color="teal.500"
              isExternal
            >
              Project Proposal
              <ExternalLinkIcon mx="2px" />
            </Link>
          </ListItem>
          <ListItem>
            <Link
              href="https://github.com/gt-big-data/MentalHealthRedistribution"
              color="teal.500"
              isExternal
            >
              GitHub Repository
              <ExternalLinkIcon mx="2px" />
            </Link>
          </ListItem>
        </UnorderedList>
        <svg id="legend" style={{ height: 230 }}></svg>
        <svg id="map" style={{ width: 1000, height: 600, marginBottom: 30 }}></svg>
        {/* <ComposableMap>
          <Geographies geography={data}>
            {({geographies}) => geographies.map(geo =>
              <Geography key={geo.rsmKey} geography={geo} />
            )}
          </Geographies>
        </ComposableMap> */}
      </Flex>
    );
  }
}

export default App;

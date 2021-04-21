# Mental Health Redistribution
- GT Big Data Big Impact Fall 2020/Spring 2021 Project
## Design Doc and Project Overview:
https://gtvault.sharepoint.com/:w:/s/BigDataBigImpact/EY6vpVRpPFJCkFRCd9M_lZIB4fX2rYmK2x9LA8m1vKwRqQ?e=shtuta
## Members
- Analysis Project Lead: Patrick Liu
- Data Visualization Lead: Tushna Eduljee (Fall '20), Edmund Xin (Spring '21)
- Platform Lead: Abhi Joshi
- Analysis Team:
    - Rhea Mathew (Fall '20, Spring '21)
    - Vishnu Suresh (Fall '20)
    - Matthew Li (Fall '20, Spring '21)
    - Jasmine Li (Fall '20)
    - Ethan Mendes (Spring '21)
    - Shiva Devarajan (Spring '21)
- Data Vis Team:
    - Rachel Daniel  (Fall '20)
    - Yash Patel  (Fall '20)
    - Sidarth Rajan (Fall '20)
    - Athena Wu (Fall '20)
    - Edmund Xin (Spring '21)
- Platform Team:
    - Aayush Seth (Fall '20)
    - Jesse Chen (Fall '20, Spring '21)
    - Kritik Acharya (Fall '20, Spring '21)
    - Steven Leone (Spring '21)

## Running the Flask API Locally
- simply change directories until you are in the `flask_app` folder
- run `python3 main.py`!
### Accessing Deployed API
- the current API is deployed on `mental-health-redistribution.uc.r.appspot.com`, and current endpoints it supports are
    - `/potential_mental_health_centers`: returns potential mental health center location's name, address, city, state, latitude/longitude
    - `/current_mental_health_centers`: returns current mental health center's name, address, city, state, latitude/longitude
    - `/county_info`: given a county that is queried, returns various mental health stats compiled from .gov data for the county.
    - `/optimal_centers`: given a list of counties, calculates the new optimal mental health center locations, sorted in a list from best->worst.
## Running the React App
- simply change directories into the `second_sem_visualization` folder
- run `yarn start`!

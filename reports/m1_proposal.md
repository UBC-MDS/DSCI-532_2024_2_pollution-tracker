# Milestone 1 Proposal - Pollution Tracker
Group 2 - Merete Lutz, Kun Ya, Weiran Zhao, Sid Grover

## Motivation and Purpose

Our role: Data scientist consultancy firm

Target audience: Public health officials

Air pollution is worldwide one of the greatest threats to human and environmental health. Pollutants like particulate matter (PM), carbon monoxide (CO), and ozone ($O_3$) are inhaled and absorbed into the body through the lungs, leading to an increased risk of mortality and diseases like stroke, heart disease, lung cancer, and pneumonia. This increased risk of morbidity and mortality can be seen after a relatively short exposure period for some pollutants, and at-risk populations such as the elderly, children, and pregnant women are particularly susceptible to the effects of air pollution. To address this global issue, we propose an air pollution visualization app that will help public health officials tease apart pollutant trends both locally and globally, so that they may better advise their population through air quality advisories and public health measures.

## Description of the Data

Our dashboard will use the [World Air Quality Data 2024 (Updated)](https://www.kaggle.com/datasets/kanchana1990/world-air-quality-data-2024-updated) data set licensed under the [Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/). We will be visualizing over 50,000 records from across the globe, with measurements taken from March 13, 2014 to March 25th, 2024. Each observation has 10 associated variables which we will use to visualize pollution, they are described below:

- Location information: (`Country Code`, `City`, `Location`, `Coordinates`, `Country Label`)
- Pollutant measurement: (`Pollutant`, `Unit`, `Value`)
- Time of Measurement: (`Last Updated`)
- Who conducted measurement: (`Source Name`)

There is missing information in the `City` column, and the `Location` column includes information that is not standardised across countries, so we plan on using the `Coordinates` values for our geospatial data. We are also not concerned with the `Source Name` column. Most of our analysis will be looking at `Coordinates`, `Pollutant`, `Unit`, `Value`, `Last Updated`, and `Country Label`.

We will use these columns to derive new variables, such as an [Air Quality Index (AQI)](https://www.airnow.gov/aqi/aqi-basics/) for each pollutant, and an overall air quality score. These metrics will give our users a more intuitive idea of pollutant concentration, as they provide a standardized range across all pollutants of what is considered acceptable and unacceptable. Engineering these variables will allow our dashboard to be as interpretable as possible, especially for a layperson who isn't an expert in air pollution.

## Research Questions

Persona: Dr. Hu is a public health official in the Ministry of Health. She wishes to monitor public health outcomes, advise on health policy, and initiate public health programs. Dr. Hu is not a data science professional but she has immense knowledge of epidemiology, medicine, and public health. 


## App Sketch and Description


### Bibliography
Air quality, energy and health (no date) World Health Organization. Available at: https://www.who.int/teams/environment-climate-change-and-health/air-quality-energy-and-health/health-impacts (Accessed: 29 March 2024).

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

Dr. Hu is a public health official in the Ministry of Health. She wishes to monitor public health outcomes, advise on health policy, and initiate public health programs. Dr. Hu is not a data science professional but she has immense knowledge of epidemiology, medicine, and public health. 

Dr. Hu wishes to understand the impact of air pollution on public health and identify areas where government intervention can reduce negative health outcomes. She plans to use this dashboard to identify problem areas, recommend specific courses of action for the public health ministry, and deliver new health campaigns tailored to the needs of citizens to mitigate the ill-effects of air pollution. 

Through the Pollution Tracker dashboard, Dr. Hu aims to:

* Explore global and local air pollution trends over several years to gain an in-depth understanding of pollution patterns and their evolution over time.
* Compare levels of key pollutants (PM, CO, Ozone, NOx, SOx) across various regions to pinpoint differences and similarities in air quality.
* [Identify] pollution hotspots where urgent action is needed, and highlight times when pollution levels rise significantly, to sound the alarm for potential air quality crises.
* Derive actionable insights by analyzing pollution levels, trends, rates of change, and anomalies. These insights will inform public health advisories, guide health policy formulation, and mitigate air pollution health impacts for a healthier and happier population.

**Usage Scenarios:** Dr. Hu logs into the “Pollution Tracker” dashboard and app designed by Group2 Data Science Consultants Inc. She wishes to prepare a comprehensive report to be shared with both technical and non-technical stakeholders within the ministry. She follows these steps to build her report:

1. Dr. Hu selects her country from a sidebar with a dropdown menu functionality. This sets the granularity level to her country and displays interactive line charts and bar charts with trends, changes, and patterns in ozone, PM2.5, CO, SOx, and NOx levels for her country.
2. Dr. Hu wishes to take a closer look, so she moves to the “pollutant map” and selects a pollutant. In this map, she clearly sees levels of said pollutant in different areas. She notices a clear distinction between pollutant values in urban and rural areas - pointing to an impending health crisis driven by air pollution.
3. To compare her country’s risk to those of other countries, she selects the “compare” button and chooses another country and time span. This allows her to see a clear comparison between pollutant levels for her country and her selected country (for example, Canada and the US over May-July 2023, due to increased forest fires)
4. Concerned by these elevated pollutant levels in urban areas, she considers only the most recent data by filtering for time span. She notices, from the line chart, that pollutant levels are higher during the winter months. This compels her to investigate this further, which is when she discovers it may be related to the burning of heating oil - which releases pollutants at high rates and causes respiratory issues as well.
5. Using the AQI metrics provided by the dashboard, she identifies areas with consistently poor air quality. She cross-references this data with public health reports on respiratory issues during the same period and spots a clear correlation.
6. Based on her findings, Dr. Hu suggests policy measures to reduce pollutant levels across various cities. She works with municipal authorities to implement varying programs that promote the burning of cleaner fuel. Over time, Dr. Hu can use the various plots to measure the effectiveness of the impact of her policies. She can use the line charts to see how pollutant levels, over the same period, change year-over-year. She can also use the pollutant map, comparing it to pollutant maps at previous times, to visually inspect if her policies made any difference. 





## App Sketch and Description


### Bibliography
Air quality, energy and health (no date) World Health Organization. Available at: https://www.who.int/teams/environment-climate-change-and-health/air-quality-energy-and-health/health-impacts (Accessed: 29 March 2024).

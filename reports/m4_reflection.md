# Milestone 4 Reflection

## What we have implemented in Milestone 4

### 1. Data Wrangling:
- Removed Antarctica from the world map due to minimal observations.
- Dropped latitude and longitude columns in the processed data for simplicity.
- Adopted Parquet format for faster data loading.

### 2. Functionality Enhancements:
- Excluded pollution types lacking AQI standards to streamline data relevance.
- Integrated a 'Learn More' button for detailed explanations of AQI and pollution types.
- Implemented a regression trend line to smooth data over a longer window, highlighting general trends.
- Resolved an issue where plots were not displaying with default selections in Milestone 3.
- Restricted user selections to a maximum of four to prevent overcrowding of the visual display.
- Enhanced performance and loading efficiency through multiple approaches including using DuckDB connections of vegafusion, adding caching to callbacks, and filtering data with queries.

### 3. Aesthetic Improvements:
- Adjusted minor chart elements: renamed legend titles, sorted legends by order, and removed the y-axis on bar charts.
- Hid unnecessary axis titles and aligned font sizes across chart titles.
- Set a custom Favicon for the dashboard for better branding.

### 4. Repository Structure:
- Removed unnecessary packages from the requirements.txt file to clean up dependencies.
- Added a Creative Commons license to ensure the open-source availability and usage of the dashboard.

### 5. Documentation:
- Enhanced the README file to clearly state the questions our dashboard addresses and the functionality it provides.


## Future Improvements and Additions

### Predictive Model and Visualization of "Danger Zones"
- We aim to build a predictive model that highlights "danger zones" based on pollution trends, using historical pollution and traffic data. This model will likely use multiple linear regression and random forest regressors to forecast future pollution levels. A visualization feature will enable users to identify potentially high-pollution areas effectively.

### Real-Time Pollution Data API
- We plan to develop an API to retrieve the latest pollution data from the World Health Organization (WHO). This API will process the data and update our dashboard continuously, ensuring that users have access to the most current information without needing to manually upload data.

### Enhanced Dashboard Performance
- To address latency issues and enhance user engagement, we will optimize our dashboard’s performance using caching, memoization, and WebGL graphics. WebGL will leverage GPU capabilities to render graphics more efficiently than traditional SVGs, improving the overall speed and responsiveness of the dashboard.




# Milestone 3 Reflection 

At the very beginning of this class, the team set out an ambitious goal to build a dashboard that looked as follows:
<img src = "img/sketch.png">

## Meeting Original Goals + New Additions
This dashboard had an option to select multiple continents, select a region, set a time frame, to display data for one pollutant (of the several pollutants). The dashboard also contained a ranking of top 15 countries, a trend of pollution over time, and a pollutant tracker. **We're stoked to share that we've built a dashboard that not only meets, but exceeds, the expectations we set at the outset of milestone 1!** We've added several **new features** that we had not decided upon during milestone 1:
* Engineered a new AQI and AQI category feature, then plotted it on a Chloropleth map
* Dealt with AQI edge cases at high concentration values, and engineered the function to calculate AQI up to 500 (the most polluted cities in the world have an AQI under 250)
* Designed an air pollution trend function that reduces the impact of noisy data (locally weighted scatterplot smoothing) to communicate a clear trend in pollutant concentration values (suggested by Joel)
* Added data summary cards/blocks to share key statistics  
* Centered the map and highlighted bar in bar chart to link it with country selection (suggested by Joel)
* Add multiple country selection in the pollution trend over time chart (suggested by Joel)
* Change the date selection tool to select data by Month

Additionally, there are **no corner cases that we have not accounted for** yet. The only hiccup this week is related to AQI calculation, but that has been solved. We followed 531/532 best design principles in order to bring maximum benefits to our end users, while maintaining our professional standards. 

## Our Current Standing
#### The Good and Bad of the Pollution Dashboard
As of Milestone 3, the dashboard does it's job very well: It clearly communicates trends in pollution over time (by country/continent), offers comparison to top 15 polluted countries, provides an accurate AQI value, summarises key data points by pollutant and country, and much more. 

However, it could be a better predictive tool by selecting potential "danger zones". The dashboard also experiences some latency, which can be improved by identifying performance bottlenecks (through `cprofile` for dash) and implementing asynchronous data loading/lazy loading. Finally, the dashboard could be split into modules, which is the team's focus for now. 

This brings us to discuss potential improvements. 

## Improvements
We plan to take this dashboard to the next level by:
* link the continent/region, country, and time feature to each other
* build a predictive model and visualisation that highlights "danger zones" based on trends in pollution levels - in order to bring attention to problem areas
* Make minor visual changes (bring bar closer to chloropleth map, use a common color scheme for entire dashboard, add collapsible components, add navigation bar)
* address any other feedback from our classmates Arturo, Jing, and Joey that has not already been implemented

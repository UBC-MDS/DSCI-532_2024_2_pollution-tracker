# Milestone 2 Reflection

## What we have implemented so far

Overall, our dashboard is quite faithful to our original sketch. We have implemented our four filtering methods (pollutant, region, country, time), and have the three plots we originally proposed (global map, top 15 countries, and pollutant over time).

## What we have not yet implemented

## Divergence from original sketch

We have added a data summary section with summary statistics for the filtered data, so that our users have a better idea of the number of observations and their range of values.

## Current Issues with the Dashboard

Currently we have some issues with the aesthetics of the dashboard. Our data summary section has formatting that does not match the rest of the dash. Overall our plots do not align well, and you must scroll to see the charts in full. We also have some redundant titles that need fixing.

## Deviations from Best Practices

## Strengths and Weaknesses

## Future Improvements and Additions

* Currently, our plot for the "Top 15 countries" does not change based on the country we have filtered for. We hope that for the next week we can adjust this plot so that the selected country will be included as the first bar on the chart with perhaps different coloring so that we can compare it to the top polluters.
* We are also not quite happy with the way our time filter is currently working. We are considering perhaps filtering by month-year rather than day-month-year, so that it is easier to select larger periods of time without having to click through many months at a time.
* Currently our AQI feature engineering results in lots of missing values for this column. We believe this may be due to rounding errors from small values, and extremely large values that are out of the boundaries we have included for AQI. We want to look into ways to improve this feature engineering, and are also considering changing the AQI feature from being numerical to categorical (i.e. 'Good', 'Moderate', 'Unhealthy for Sensitive Groups') for which there is domain precedence.
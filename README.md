# Pollution Tracker

## A dashboard to explore local and global trends in air pollutions

![gif](./img/app.gif)

Welcome to our repository! Feel free to look around. If you want to go straight to the dashboard, click [here](https://dsci-532-2024-2-pollution-tracker.onrender.com/). Read on to find out more about what we're doing and why.

### What is the dashboard?
_Pollution Tracker_ utilizes the [World Air Quality Data 2024 (Updated)](https://www.kaggle.com/datasets/kanchana1990/world-air-quality-data-2024-updated) dataset to visualize global air pollution levels. With data on pollutants like PM2.5 and NO2 from around the world, our dashboard makes it easy to see current conditions and trends.

### Who is it for?
_Pollution Tracker_ is intended for use by public health officials but designed for anyone interested in the environment, public health, or public policy. We hope it enables these individuals to get a clear idea of air quality metrics and their trends. Our project is built on data sourced from OpenAQ, an environmental non-profit who collects air pollution data from around the world. This dashboard aims to be different from other air quality apps, by looking at global data and long-term trends.

### Why should we care?
Air pollution is worldwide one of the greatest threats to human and environmental health. Pollutants like particulate matter (PM), carbon monoxide (CO), and ozone ($O_3$) are inhaled and absorbed into the body through the lungs, leading to an increased risk of mortality and diseases like stroke, heart disease, lung cancer, and pneumonia. This increased risk of morbidity and mortality can be seen after a relatively short exposure period for some pollutants, and at-risk populations such as the elderly, children, and pregnant women are particularly susceptible to the effects of air pollution.

### What is AQI? 
Air Quality Index (AQI) is an indicator of air quality developed by government health authorities to communicate the level of air pollution in an area. When AQI levels are high, several subgroups are affected by it's negative impacts - children, seniors, and those with respiratory and cardiorespiratory illnesses. In times of high AQI, health bodies suggest people stay indoors, use high-efficiency particulate absorbing (HEPA) filters, wear NIOSH N95, and avoid any risk to their health. 

AQI is calculated as the maximum of the index of pollutant $p$, where this index is defined as: $I_p = \left\lfloor \frac{(I_{\text{high}} - I_{\text{low}}) \times (C_p - C_{\text{low}})}{(C_{\text{high}} - C_{\text{low}})} + I_{\text{low}} \right\rfloor \quad$ $\forall p \in [\{\text{CO}_2, \text{CO}, \text{O}_3, \text{PM2.5}, \text{PM10}, \text{SO}_x, \text{NO}_x\}]$. This index is the linear interpolation of concentration between concentration breakpoints ${C}$ for pollutant $p$. However, the values are often represented as one of five groups (labels vary by country): good, moderate, unhealthy for sensitive groups, unhealthy, very unhealthy, and hazardous. 

Needless to say, high AQI is a major problem for millions of people and health authorities. Given that this dashboard is intended for use by health officials, engineering an AQI feature is imperative for ensuring our public health officials are well-equipped to deal with pollution-related crises. This feature not only eliminates the need for users to convert pollutant concentration into AQI, but also saves time and prevents conversion errors. 

### Can I run your app locally?
If you'd like to play around with our project, feel free to clone this repository using whatever method you prefer. The SSH key method is below:

From your terminal, navigate to the location you would like to download the repository and run the following command:

```bash
git clone git@github.com:UBC-MDS/DSCI-532_2024_2_pollution-tracker.git
```

To use our developer environment, run the following command in the terminal from the root of the repository:

```bash
 conda env create -f environment.yml
```

Activate the environment with the following command:

```bash
 conda activate pollution-tracker
```

To launch the dashboard, navigate to the src folder of the repository in your terminal and enter the following command:

```bash
python app.py
```

You should see some output in your terminal that looks similar to: 

```bash
Dash is running on http://111.1.1.1:8080/
```

The exact numbers may be different. Copy and paste this link into your preferred browser and the app should load momentarily.

### How can I get involved?
If you have any feedback or input for our team, you can get into contact with us by creating a [new issue](https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker/issues/new). More instructions on contributing can be found [here](https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker/blob/main/CONTRIBUTING.md). Please abide by our [code of conduct](https://github.com/UBC-MDS/DSCI-532_2024_2_pollution-tracker/blob/main/CODE_OF_CONDUCT.md) when contributing to our project.

### Who are we?
We are [Merete Lutz](https://github.com/meretelutz), [Kun Ya](https://github.com/carinaya), [Weiran Zhao](https://github.com/weiranzhao97), and [Sid Grover](https://github.com/killerninja8); a group of Masters of Data Science students at the University of British Columbia.

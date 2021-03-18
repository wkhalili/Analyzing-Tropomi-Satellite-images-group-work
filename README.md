# CH4 Data Representation from satellite Sentinel 5P

<p align="center">Joep van Benten

<p align="center">Wala’a Mahmoud

<p align="center">Natanael Gomes

<p align="center">Zulukade Wusiman

<p align="center">Mitsy Prada

<p align="center">Akshit Bhardwaj


## Introduction 

The goal of our project is to detect methane leakages based on satellite measurements from TROPOMI. Most of the rubric aspects have been applied in this project. Unfortunately, we conclude that it will be very difficult to detect leakages purely based on TROPOMI data, explained in more detail throughout the document.

The structure of the repository has become somewhat chaotic due to the parallel work of the members of this group on data fusion, analysis and presentation of results, for which multiple solutions exist.

 

## Incidents

To learn how to detect a leakage we need to see how a leakage looks like in TROPOMI data. The first incident case studied is the Ohio natural gas well blowout. They used the total column CH4 measurements from the TROPOMI data. They pick a period, in this period only two days of measurements met their selection threshold. They discovered that due to cloud cover leaving the orbit, it will show no measurements at some days. But we decided to study more incident cases to see if the incidents will show a pattern on the TROPOMI data.

We wanted to get the data of Ohio incident from TROPOMI website, but the website shows only data from 2019 and 2020. Thus, we searched more news of gas (methane or natural gas) leakage. The result is on the GitHub repository called gas_leakage_incident.xlsx.

 

## Requirements

Our goal is to use TROPOMI data to detect a methane leakage.

\-     Download Data

\-     Combine data

\-     Build fusion architecture 

\-     Construct a common representation format

\-     Analyze Data

\-     Build detection algorithm

## Download Data

We found out that the CH4 data of TROPOMI has multiple orbits per day. That means we need to download the data based on the region we wanted to study. Otherwise it will take a lot of space to store it. We thought about using API to get the data, but there is no API available. Thus, we have to manually download the data from the places where the incidents happened. 

The data we downloaded contains important information; coordinates, CH4 measurements and dates. In this way, we decided to fuse all the data from different orbits in the same day based on the area where the incident happened. And for studying the leakage [1] we decided to use the data of 10 days before and after the incident happened. 

 

 

## Fusion architecture

Our fusion architectures are:

1. Fuse the data from all the orbits in the same day.

2. Detect the leakage over 20 days (10 days before and after the incident date).

 

## Combining data & representation format

 This part contains multiple implemented methods to combine data of multiple orbits and days.

**Method 1: combine orbits of the same day (used in ‘notebook’)**

\-     Create a list ‘dates’ of all days.

\-     For each orbit of the same day extract the latitude, longitude and methane value.

\-     Create a list ‘data_per_day’ containing for each day a list of [latitude, longitude, methane].

**Method 2: Normalized data fusion (used in ‘Tropomi_CH4_Leakages.ipynb’)**

\-     Given the data from two orbits, Orbit1 and Orbit2, composed of coordinates (latitude, longitude), methane concentration and quality index of each coordinate.

\-     Locate the area of overlap using geometry: create two polygons using the 4 extreme coordinates (north, south, east, west), identify the intersection of the two polygons to obtain the overlapping area.

\-     For the coordinates of Orbit1 inside of the intersection calculate the distance to the closest coordinate in the Orbit2. If the distance is smaller than 9.89 km (diagonal between coordinates) combine the two values into one.

\-     To combine the data normalizing the values by their quality index, we gave more weight to data with better quality index.

**Method 3: Store the data (latitudes, longitudes, methane mixing ratio) into X by Y arrays（used** **in** **‘tropomi project-CH4 average.ipynb’**)

\-     X is number of days; Y is amount of orbits

## Data visualization

Visualizations enable humans to understand the data. We came out with several options for this challenge.

### **Basemap**

One of the matplotlib toolkits is basemap, which enables to plot data on a world map. Below is a basemap plot shown containing (1) the data of multiple orbits and (2) a blue plane of each orbit coverage.

![basemap1](/image/report%20figs/basemap1.PNG)

<p align="center">Figure 1: Basemap over china


Videos are created to see how the data of a location changes over time. The videos contain for each plot a frame, see (reference to video folder).

### **Interactive plots**

The Python library Folium enables to create interactive maps using the leaflet.js library. The basic version enables to zoom in and out within a Jupyter notebook. The image below shows all data points from an orbit containing a methane value (the colormap is not yet added).

![folium2](/image/report%20figs/folium2.PNG)

<p align="center">Figure 2: Itheractive plots using scatter


Also, data from multiple days can be shown and controlled via the time slider at the bottom. The image below is a plot of detected moving clusters (explained later in the document).

![folium1](/image/report%20figs/folium1.PNG)

<p align="center">Figure 3: Itheractive plots using scatter for multiple days




## Data Analysis

### **Clusters** 

When we open an ncd file, i.e. the satellite data, we find that there are Fill values in place for some readings. These readings are basically omitted data points and the value is just there as a placeholder. 

![img](image/report%20figs/fig4.png)

<p align="center">Figure 4: cluster

For our data frame we omit these fill values and only plot the relevant values. Plotting these values on a map it shows up as follows.

### **Statistical representation**

We chose a rectangular area that covers a big part of China, and build the CH4, latitude and longitude lists for the area of study and for the period of one month. Then we calculated the average, percentile, minimum and maximum of each day, and standard deviation. From the result of studying one month of data, we can see that there is a pick on the CH4_maximum line between the 7th and the 9th of May, this might reflect the construction incident with date 6th of May in coordinates 40.820417, 111.662833 (see gas_leakage_incident.xlsx).

![CH4_statistical_data](image/report%20figs/CH4_statistical_data.png)

<p align="center">Figure 5: CH4 statistical data of China during May




## Conclusions

We have found multiple incidents of methane leakages. We expected that visualizing the leakages would give us an understanding of how we can detect them via an algorithm. To visualize the leakage is data of multiple orbits and days combined. The visualization (link to videos) show that only Tropomi data is insufficient to see a leakage.

 

## Reference 

[1]. Pandey, S., Gautam, R., Houweling, S., Denier van der Gon, H., Sadavarte, P., Borsdorff, T., et al. (2019). Satellite observations reveal extreme methane leakage from a natural gas well blowout. Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.1908712116





## **Instructions for data files**

We have a shared folder to include all data files, this files must be included on the folder 'data' in the repo folder.
In the code always refer to the folder 'data' so we can run the same code in any computer.
the data folder and the checkpoint folder are in the gitignore and will not be tracked by git.

## **Videos folder**

The videos folder contains a collection of videos produced using the data from the netCDF4 files, to objective is to investigate the leakages listed on the "gas_leakage_incident.xlsx" file. The videos are produced with 0.5 frames per second and have a red circle with raius of 50 km around the incident coordenates. It is considered 10 days before and after the incident. In the folder 'fusion' there is a collection of videos using the data combined of 2 orbits around the incident, also 0.5 frames per second. In the case a netCDF4 file is not available the day is skipped.
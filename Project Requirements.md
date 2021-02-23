# Project Requirements

## High level requirements:

-	The system can detect methane gas leakage using Tropomi Sentinel-5p L2_CH4 data.
-	The system can show the information graphically, including the before, during and after the detected leakage event, including the methane concentration, the geographical map and the estimated location of the leakage.
-	



## Sub-requirements:

- Investigate if the S-5p data can be processed using Neural Network.

- Verify the accuracy of the algorithm.

- Investigate if the algorithm can be used for estimate the amount of methane leaked.

- 

  

## Observations:

- There is no main requirement about which level of the data we need to use, agreed on the group to use L2, i.e. methane concentration.
- There is no requirements or learning outcomes regarding user interface UI, or graphical user interface GUI. 

## Questions:

- Are we going to consider the wind? **No.**
- How many days (or how much data) do we need to consider? **Considering 10 days before and after.**
- On the Assessment Aspect representational format is something related how the data is stored? **The data is stored in the format netCDF4.**
- Is virtualization not related to Tropomi?
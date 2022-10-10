# Generic Real Estate Consulting Project

The data will either be provided by an annoucement (downloadable via URL) or uploaded directly to the `raw` directory.

- Group member: Shuying Huang(1174100), Wenxin Zhu(1136510), Xinyi Rui(1135819), Yixuan Song(1170491), Zihan Qin(1133441)

**Research Goal:** Predict the house price for the next three years and find the determine features about the house price. Compute solid recommendation base on the prediction and analysis. 

**Timeline:** The timeline for the research area is 2022.

To run the pipeline, please run the files in order:
1. `web_scraping.py`: save in scripts folder, scraping data from domain website.
2. `pop forecast.ipynb`: notebook to predict population for the next 3 years.
3. `Open_Route_Service.ipynb`: notebook use API to calculate the distance from the house to Melbourne city.
4. `preprocess.ipynb`: notebook to preprocess raw data access from domain website.
5. `prediction_lr.ipynb`: save in model folder, linear regression model to predict the top10 growth rate suburbs.
6. `MLPRegressor.ipynb`: save in model folder, Multi-layer Regression model to predict the most livable and affodable suburb.
7. `growth rate visualization.ipynb`: visualize growth rate in different postcode.
8. `lr_prediction_visualization.ipynb`: visualiza schools and price in geograph.
9. `pop visualization.ipynb`: visualize population corresponding to postcode.
10. `price visualization.ipynb`: visualize price corresponding to postcode.
11. `MLP visualization.ipynb`: visualize average predicted price and growth rate corresponding to postcode.
12. `Summary.ipynb`: summary the overall approach taken and the limitations, assumptions made along the way. 
13. `Sprint6.md`: this is the final checkpoint.

**External data**
Population data: https://www.abs.gov.au/statistics/people/population/regional-population/latest-release
School data: https://discover.data.vic.gov.au/dataset/school-locations-2022
Data used to merge population data and postcode: https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.006July%202011?OpenDocument
Postcode shapefile used to plot maps(go to Downloads for GDA94 digital boundary files and select Postal Areas - 2021 - Shapefile, this shapefile used to plot maps): https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files

<h1>Multicitreria-Analysis-Beehives</h1>
<h3>Authors: <i>Franziska Walheim, Lena Buchner</i></h3>
<h2>General Information</h2>
As Honeybees are an essential part of the ecosystem, we want to base this analysis on testing possibilities of cultivating bees in urban spaces.<br>
Therefore we created a model using <i>QGIS</i>, that generates a map showing the best suitable location for bees in the study area Dresden.<br>
There are several criteria that need to be considered when choosing a location for a beehive. Due to these results we decided to use the <i>Multi-Criteria Method</i> for our model. This gives us the possibility to consider multiple criteria at once.
<br>
<h3>Criteria:</h3>
<table>

  <table>
    <tr>
      <th>Criteria</th>
      <th>Examples</th>
    </tr>
    <tr>
      <td>sun exposure</td>
      <td>ideally South-East</td>
     </tr>
     <tr>
       <td>disruptions</td>
       <td>energy-poles, industrial sites,...</td>
     </tr>
     <tr>
      <td>food-sources</td>
      <td>flowers, fields, trees,...</td>
    </tr>
    <tr>
      <td>windbreak</td>
      <td>trees, bushes,...</td>
    </tr>
    <tr>
      <td>water-source</td>
      <td>preferably standing water</td>
    </tr>
    <tr>
      <td>slope</td>
      <td>higher slope=less cold air</td>
    </tr>
  </table>


<h2>Preperation</h2>
<b>Software:</b> QGIS (we used 3.16.12; not required)<a href="https://qgis.org/de/site/forusers/download.html"> for installation click here</a>
<br><br>
<b>Downloading Data</b> (all of the necessary files contained in <i>data</i>): 
<ul>
  <li>OSM (disruption, food-sources, windbreak, water-source): 
   <br> -> ohsome API (use the api_bees.bat)</li>
  <li>DEM (slope, aspect):
    <br> -> srtm-data (srtm_39_01.zip <a href="https://srtm.csi.cgiar.org/srtmdata/">source</a>)</li>
    <li> Dresden (administrative border):
      <br> -> geodaten-sachsen (dresden.zip <a href="https://www.geodaten.sachsen.de/downloadbereich-verwaltungsgrenzen-4344.html">source</a>)</li></ul>

<h2>Execution</h2>
<b>API-Script:</b>
<br>
Clone this respository to your computer so you have all the data and scripts available.
<br>
The given API script (api_bees.bat) downloads a part of the needed data. The script gives informations on how to change the study area that this model is being tested on. The containing bounding-box downloads the data for the city of dresden.
<br>
after this step you will have all the needed data available:<br>
- disruptions_2021.geojson<br>
- food_2021.geojson<br>
- water_2021.geojson<br>
- windbreak_2021.geojson<br>
- desden.shp<br>
- srtm_39_01.tif<br>
<br>
Open all these layers in your QGIS Software.
<br><br>
There are two possible ways of executing this model:
<br><br>
1. Using the given <b>model</b> (model_multicriteria.model3)
- gives easy and visual overview of the process<br>
- suitable for less experienced users<br>
<br>
2. Using the given <b>script</b> (bees.py)
- fast processing<br>
- overview over commands<br>
<br><br>
Both ways are available in the QGIS Toolbox.
<br><br>
<h2>Visualization</h2>
  
  We found the easiest way to visualize the results is using the singleband-pseudocolour option. There you can choose a colour scheme and create 10 classes using a quantile classification. To build the classes click classify. Know your data should be easier to analyse. The higher number are showing a higher suitability for beehives.

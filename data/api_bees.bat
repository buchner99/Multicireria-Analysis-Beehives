::Ohsome API
::Authors: Franziska Walheim, Lena Buchner
::this API creates 4 Layer (.geojson) with the necessary data for the study area Dresden
::if you wish to change the study area, edit the bounding box (tool for creating bounding box: https://boundingbox.klokantech.com/) 

curl -X POST ^
--data-urlencode "bboxes=13.579324,50.974937,13.966063,51.17772" ^
--data-urlencode "time=2021-11-01" ^
--data-urlencode "filter=(natural=tree or natural=scrub or natural=heath or natural=shrubbery or natural=wood) and geometry:point" ^
-o windbreak_2021.geojson ^
"https://api.ohsome.org/v1/elements/geometry"

curl -X POST ^
--data-urlencode "bboxes=13.579324,50.974937,13.966063,51.17772" ^
--data-urlencode "time=2021-11-01" ^
--data-urlencode "filter=(natural=water) and geometry:polygon" ^
-o water_2021.geojson ^
"https://api.ohsome.org/v1/elements/geometry"

curl -X POST ^
--data-urlencode "bboxes=13.579324,50.974937,13.966063,51.17772" ^
--data-urlencode "time=2021-11-01" ^
--data-urlencode "filter=(natural=tree or natural=scrub or natural=heath or natural=grassland or natural=wood or landuse=grass or landuse=village_green or landuse=flowerbed) and geometry:polygon" ^
-o food_2021.geojson ^
"https://api.ohsome.org/v1/elements/geometry"

curl -X POST ^
--data-urlencode "bboxes=13.579324,50.974937,13.966063,51.17772" ^
--data-urlencode "time=2021-11-01" ^
--data-urlencode "filter=(landuse=industrial or power=pole or power=tower or power=portal or power=generator or power=connection) and geometry:polygon" ^
-o disruption_2021.geojson ^
"https://api.ohsome.org/v1/elements/geometry"






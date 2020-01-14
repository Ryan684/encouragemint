MVP2: Recommend plants for a garden based on season, specifically for rainfall.
     - Average rainfall of a location for a whole year isn't a fair reading.

    - recommend/spring (march, april, may)
    - recommend/summer (june, july, august)
    - recommend/autumn (september, october, november)
    - recommend/winter (december, january, february)

datasource: Weather API of some sort that accepts season/months and co-cordinates as input for average weather?
    - last 12 months datasource is fine. probably most accurate instead of a bigger dataset.
    - filter moisture_use on trefle params with average rainfall for that season at that location
        - need to find moisture_use possible values on Trefle, then transform that rainfall data into those classifications.
    return works the same way, just dump the trefle response to encouragemint resonse data for now.


potential API - https://api.meteostat.net/#introduction . have to query for stations near garden latlong, then historical weather
                for that station in the history/monthly and filter? use normals endpoint to look at weather readings from nearest station?


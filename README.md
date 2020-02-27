<h1>Encouragemint<h1>
This API allows you to hold an inventory of plants of interest in your garden, and can make recommendations
on plants that will thrive in your garden based on key pieces of information that can be gleaned from public
APIs and databases. For example, it can make recommendations on plants for specific seasons based on:</br>
<li>Average rainfall for your garden</li>
<li>The shade/sunlight your garden gets by it's direction</li>

You can also filter plants by:</br>
<li>The desired bloom period</li>
<li>The desired duration (Perennial, Annual, Biennial)</li>

<h2>Features in the pipeline</h2>
<li>More intelligent garden recommendations (Soil toxicity, temperatures etc).</li>
<li>More optional filters for plant attributes as part of garden recomendations.</li>

<h2>Endpoints (MORE DETAIL REQUIRED. SWAGGER DEFINITION?)</h2>
<li>/profile [POST, PUT, PATCH, GET]</li>
<li>/garden [POST, PUT]</li>
<li>/plants [POST, PUT]</li>
<li>/recommend/<garden_id> [GET]</li>


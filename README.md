<h1>Encouragemint</h1>
This API makes recommendations on plants that will thrive in your garden based on key pieces of information that can be 
gleaned from public APIs and databases. For example, it can make recommendations on plants for specific seasons 
based on:</br>
<ul>
    <li>Average rainfall for your garden</li>
    <li>The shade/sunlight your garden gets by it's direction</li>
    <li>The desired bloom period</li>
    <li>The desired duration (Perennial, Annual, Biennial)</li>
</ul>

<h2>Features in the pipeline</h2>
<li>More intelligent garden recommendations (Soil toxicity, temperatures etc).</li>
<li>More optional filters for plant attributes as part of garden recommendations.</li>
<li>Integration of Amazon Lookup API for recommended plants, so users can choose to buy the plant.</li>

<h2>Endpoints</h2>
<li>/recommend [POST]</li>

<h2>Post Payload Fields</h2>
    <b>location</b>: An address as specific as possible, but can be as loose as your town. I.E, 'London, UK'.</br>
    <b>direction</b>: The direction of your garden, if you stood looking out from your backdoor. Values can be:
    <ul>
        <li>NORTH</li>
        <li>EAST</li>
        <li>SOUTH</li>
        <li>WEST</li>
    </ul>
    <b>duration</b>: How long the plant survives. I.E if just one year, it's an annual. Values can be:
    <ul><li>PERENNIAL</li>
        <li>ANNUAL</li>
        <li>BIENNIAL</li></ul>
    <b>bloom_period</b>: The season you want the plant to bloom in. Values can be: </br>
    <ul>
        <li>EARLY SPRING</li>
        <li>LATE SPRING</li> 
        <li>ALL SPRING</li>
        <li>EARLY SUMMER</li>
        <li>LATE SUMMER</li>
        <li>ALL SUMMER</li>
        <li>EARLY AUTUMN</li>
        <li>LATE AUTUMN</li>
        <li>ALL AUTUMN</li>
        <li>EARLY WINTER</li>
        <li>LATE WINTER</li>
        <li>ALL WINTER</li>
    </ul>

<h2>Logs</h2>
Currently, the app writes its logs both to a console and a debug.log file in the root directory of the project.

<h2>Deployment</h2>
To run this app locally, you can use manage.py runserver or docker-compose to run it locally in a container using
'docker-compose up' from the root directory of the project. In either case, the API will run locally at
http://127.0.0.1:8000/</br>

The UI will run at http://127.0.0.1:3000

To run this application external to your local machine on a Kubernetes cluster, follow the steps in the
/kubernetes directory README.



<h2>Prerequisites for Kubernetes deployment</h2>
There are several steps you need to complete first to be able to use Encouragemint in a Kubernetes cluster:
<li>Request access to contribute/pull the private docker hub image for Encouragemint (ryan684/encouragemint).</li><br><br>

<li>Get an API key (Free) for Trefle - https://trefle.io/reference#section/Authentication</li>
<li>Get an API key (Free) for Meteostat - https://api.meteostat.net/#key</li>
<li>Get an API key (Free-trial available) for Google's geocoding API -
https://developers.google.com/maps/documentation/geocoding/get-api-key</li><br><br>

Once you have completed the above steps, you'll need to complete the following to on the cluster where you will
run Encouragemint.<br><br>

<li>You first need to create a secret for your dockerhub credentials
(see https://developers.google.com/maps/documentation/geocoding/get-api-key). Label this .yml file
'docker_hub_credentials' with a matching metadata name.</li><br><br>

<li>Secondly, create an opaque secret yml file for your api keys named 'api_keys'
(see https://developers.google.com/maps/documentation/geocoding/get-api-key, note that you'll need
to base64 your api keys just like they do for the example with credentials).</li>

<h2>How do I deploy Encouragemint to a Kubernetes Cluster?</h2>
To deploy Encouragemint to a Kubernetes cluster, connect to the cluster and execute these kubectl commands
from it's cli:<br><br>

<li>kubectl apply -f docker_hub_credentials.yml</li>
<li>kubectl apply -f api_keys.yml</li>
<li>kubectl apply -f service.yml</li>
<li>kubectl apply -f deployment.yml</li><br><br>

In the initial cut of this Kubernetes configuration, the Encouragemint service simply uses a Nodeport, so you
can access the Encouragemint Django API root at https://<Node IP><Node Port>/.

<h2>Improvements to explore<h2>
<li>Use of a package manager to slimline the deployment I.E Helm?</li>
<li>Find a better solution for managing secrets with GIT/containers I.E a vault of some kind for credentials.</li>
<h2>Prerequisites For Kubernetes Deployment</h2>
There are several steps you need to complete first to be able to use Encouragemint in a Kubernetes cluster:<br><br>

<li>Request access to contribute/pull the private docker hub image for Encouragemint (ryan684/encouragemint).</li>
<li>Get an API key (Free) for Trefle - https://trefle.io/reference#section/Authentication</li>
<li>Get an API key (Free) for Meteostat - https://api.meteostat.net/#key</li>
<li>Get an API key (Free-trial available) for Google's geocoding API -
https://developers.google.com/maps/documentation/geocoding/get-api-key</li><br>

Once you have completed the above steps, you'll need to complete the following on the cluster where you're going to
run Encouragemint:<br>

<li>Firstly create a secret for your dockerhub credentials (see
https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret-manually). Label this .yml file
'docker_hub_credentials' with a matching metadata name.</li>
<li>Secondly, create an opaque secret yml file for your api keys named 'api_keys'
(see https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret-manually, note that you'll need
to base64 your api keys just like they do for the example with credentials).</li>

<h2>How do I deploy Encouragemint to a Kubernetes Cluster?</h2>
To deploy Encouragemint to a Kubernetes cluster, execute these kubectl commands from your cluster's
cli in this order:<br><br>

<li>kubectl apply -f docker_hub_credentials.yml</li>
<li>kubectl apply -f api_keys.yml</li>
<li>kubectl apply -f rabbitmq-deployment.yml</li>
<li>kubectl apply -f rabbitmq-service.yml</li>
<li>kubectl apply -f web-deployment.yml</li>
<li>kubectl apply -f worker-deployment.yml</li>
<li>kubectl apply -f web-service.yml</li><br>

In the initial cut of this Kubernetes configuration, the Encouragemint service simply uses a Nodeport, so you
can access the Encouragemint Django API root at https://{Node IP}:{Node Port}/.

<h2>Improvements to explore</h2>
<li>Use of a package manager to slimline the deployment I.E Helm?</li>
<li>Find a better/more secure solution for managing secrets within GIT/containers I.E a vault of some kind
for credentials.</li>
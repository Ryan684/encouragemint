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
https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret-manually). Label this .yaml file
'docker-hub-credentials' with a matching metadata name.</li>
<li>Secondly, create an opaque secret yml file for your api keys named 'keys'
(see https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret-manually, note that you'll need
to base64 your keys just like they do for the example with credentials). This will need to contain the encoded
secrets for the email account password for Encouragemint, the API keys for Trefle, Meteostat and Google Geocoder. NOTE:
both your secrets file and dockerhub credential file must have namespace: default in the metadata section.</li>

<h2>How do I deploy Encouragemint to a Kubernetes Cluster?</h2>
Currently, there is no integration with Kubernetes deployment tools like helm, but you can use the 'deploy_app.sh'
script to run all the kubectl apply commands in the correct order to deploy Encouragemint onto your Kubernetes cluster.

In the initial cut of this Kubernetes configuration, the Encouragemint service simply uses a Nodeport, so you
can access the Encouragemint Django API root at https://{Node IP}:{Node Port}/.

<h2>Improvements to explore</h2>
<li>Use of a package manager to slimline the deployment I.E Helm?</li>
<li>Find a better/more secure solution for managing secrets within GIT/containers I.E a vault of some kind
for credentials.</li>
<li>Add the manifests to run the front end.</li>
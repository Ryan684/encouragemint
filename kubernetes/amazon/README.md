<h1>Aws Notes</h1>
<p>Work in progress - procedure for deploying to AWS and configuring the infrastructure. 
This is manual for now while learning the platform.</p>

<h3>Creating an IAM Policies</h3>
<li>aws iam create-policy \
    --policy-name Encouragemint-ALB \
    --policy-document file://eks_encouragemint_alb_policy.json</li>
<li>aws iam create-policy \
    --policy-name Encouragemint-EKS \
    --policy-document file://eks_encouragemint_eks_policy.json</li><br>
TODO: Look into minimising access in policies. Not sure this is as low as entitlements can be yet.

<h3>Creating a User/Functional Account</h3>
<p>Created via the console. TODO: Look into storing in a json file and creating via the CLI.</p>

<h3>Deploying A Cluster</h3>
<p>Currently just using all the defaults - so this can be executed:</p>

<li>eksctl create cluster --name encouragemint-cluster --region eu-west-1 --fargate</li>

<h3>Connecting your Kubectl Config to Cluster</h3>
<li>aws eks --region eu-west-1 update-kubeconfig --name encouragemint-cluster</li>

<h3>Create OIDC Provider for Cluster</h3>
<li>eksctl utils associate-iam-oidc-provider --region=eu-west-1 --cluster=encouragemint-cluster --approve</li>

<h3>Creating an IAM Group</h3>
<li>eksctl create iamserviceaccount \
  --cluster=encouragemint-cluster \
  --namespace=default \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::599155278506:policy/Encouragemint-ALB \
  --override-existing-serviceaccounts \
  --approve</li>

<h3>Deploying Image to Cluster</h3>
<li>Run deploy_app.sh to deploy all the components to AWS.</li>

<h3>Deploy an Application Load Balancer</h3>
<li>kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"</li>
<li>helm repo add eks https://aws.github.io/eks-charts</li>
<li>aws ec2 describe-vpcs (extract the vpcId for the encouragemint vpc)</li>
<li>helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
    --set clusterName=encouragemint-cluster \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller \
    --set region=eu-west-1 \
    --set vpcId=(VPC id from last step) \
    -n default</li>
<li>kubectl apply -f api-ingress.yaml

<h3>Tear Down Cluster</h3>
<li>eksctl delete cluster --name encouragemint-cluster --region eu-west-1</li>

<h3>Future Enhancements</h3>
<li>Look into using CircleCI orbs to automate once working manually.</li>
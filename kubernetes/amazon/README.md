<h1>Aws Notes</h1>
<p>Work in progress - procedure for deploying to AWS and configuring the infrastructure.</p>

<h3>Creating an IAM Policies</h3>
<li>aws iam create-policy \
    --policy-name Encouragement-ALB \
    --policy-document file://eks_encouragemint_alb_policy.json</li>
<li>aws iam create-policy \
    --policy-name Encouragement-EKS \
    --policy-document file://eks_encouragemint_eks_policy.json</li><br>
TODO: Look into creating this policy via the CLI. Also, 
work on minimising access in policy. Not sure this is as low entitlements as it can be yet.

<h3>Creating an IAM Group</h3>
<p>Created via console. TODO: Look into storing in a json file and creating via the CLI.</p>

<h3>Creating a User/Functional Account</h3>
<p>Created via the console. TODO: Look into storing in a json file and creating via the CLI.</p>

<h3>Deploying A Cluster</h3>
<p>Currently just using all the defaults - so this can be executed:</p>

<p>eksctl create cluster --name encouragemint-cluster --region eu-west-1 --fargate</p>

<p>TODO: Consider keeping a json copy of this config for version control if worthwhile and using that via the CLI 
instead?</p>

<h3>Connecting AWS to Kubectl</h3>
<p>aws eks --region eu-west-1 update-kubeconfig --name encouragement-cluster</p>

<h3>Deploying Image to Cluster</h3>
TODO

<h3>Deploy an Application Load Balancer</h3>
<li>kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"</li>
<li>helm repo add eks https://aws.github.io/eks-charts</li>
<li>aws ec2 describe-vpcs (extract the vpcId for the encouragemint vpc)</li>
<li>helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
    --set clusterName=encouragemint-cluster \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller \
    --set region=eu-west-1 \
    --set vpcId=(VPC from before) \
    -n default</li>
<li>kubectl get deployment -n kube-system aws-load-balancer-controller</li>

<h3>Future Enhancements</h3>
<p>Look into using CircleCI orbs to automate once working manually.</p>
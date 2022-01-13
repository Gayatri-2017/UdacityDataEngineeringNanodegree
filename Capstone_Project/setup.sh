#!/bin/bash

if [[ $# -lt 1 ]] ; then
    echo 'Please run the command as ./setup.sh google-api-path'
    exit 0
fi

# SERVICE_NAME=sde-batch-de-project
# IAM_ROLE_NAME=sde-spectrum-redshift
REDSHIFT_VPC=sg-04ff7027cc7a3c542

# REDSHIFT_USER=sde_user
# REDSHIFT_PASSWORD=sdeP0ssword0987
# REDSHIFT_PORT=5439

host=redshift-cluster-1.crlmb3zbf4dr.us-west-2.redshift.amazonaws.com
database=dev
REDSHIFT_CLUSTER=redshift-cluster-1
REDSHIFT_USER=redshift-user
REDSHIFT_PORT=5439
REDSHIFT_PASSWORD=Redshift123

echo "Setting up Virtual Environment"
# Create a virtual environment
pip install virtualenv
virtualenv world-covid-analysis-proj-env
source world-covid-analysis-proj-env/bin/activate


# Installing other packages
echo "Installing packages within Virtual Environment"
world-covid-analysis-proj-env/bin/pip install google-cloud-bigquery
world-covid-analysis-proj-env/bin/pip install boto3
world-covid-analysis-proj-env/bin/pip install pandas
world-covid-analysis-proj-env/bin/pip install pyarrow
world-covid-analysis-proj-env/bin/pip install fsspec
world-covid-analysis-proj-env/bin/pip install  s3fs
world-covid-analysis-proj-env/bin/pip install configparser

# Installing and connecting to Redshift
git clone https://github.com/aws/amazon-redshift-python-driver.git
cd amazon-redshift-python-driver/
world-covid-analysis-proj-env/bin/pip install .
world-covid-analysis-proj-env/bin/pip install wheel
world-covid-analysis-proj-env/bin/pip install botocore==1.22.5


export GOOGLE_APPLICATION_CREDENTIALS=$2"/molten-gantry-301621-06b56bfa11e8.json"

echo "Creating an AWS Redshift Cluster named "$REDSHIFT_CLUSTER""
# aws redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER --node-type dc2.large --master-username $REDSHIFT_USER --master-user-password $REDSHIFT_PASSWORD --cluster-type single-node --publicly-accessible --iam-roles "arn:aws:iam::"$AWS_ID":role/"$IAM_ROLE_NAME"" >> setup.log
# aws redshift create-cluster --cluster-identifier redshift-cluster-2 --node-type dc2.large --master-username redshift-user --master-user-password Redshift123 --cluster-type single-node --publicly-accessible --region us-west-2 --vpc-security-group-ids sg-04ff7027cc7a3c542 
aws redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER --node-type dc2.large --master-username $REDSHIFT_USER --master-user-password $REDSHIFT_PASSWORD --cluster-type single-node --publicly-accessible --region us-west-2 --vpc-security-group-ids $REDSHIFT_VPC >> setup.log

while :
do
   echo "Waiting for Redshift cluster "$REDSHIFT_CLUSTER" to start"
   sleep 100
   REDSHIFT_CLUSTER_STATUS=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2 --query 'Clusters[0].ClusterStatus' --output text)
   if [[ "$REDSHIFT_CLUSTER_STATUS" == "available" ]]
   then
	break
   fi
done

echo "Redshift cluster $REDSHIFT_CLUSTER created successfully"

REDSHIFT_HOST=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2 --query 'Clusters[0].Endpoint.Address' --output text)













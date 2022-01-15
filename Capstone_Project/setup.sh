#!/bin/bash

if [[ $# -lt 1 ]] ; then
    echo 'Please run the command as ./setup.sh google-api-path'
    exit 0
fi

REDSHIFT_VPC=sg-04ff7027cc7a3c542
REDSHIFT_CLUSTER=redshift-cluster-1
REDSHIFT_DATABASE=dev
REDSHIFT_USER=redshift-user
REDSHIFT_PORT=5439
REDSHIFT_PASSWORD=Redshift123
# Redshift123

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


# export GOOGLE_APPLICATION_CREDENTIALS=$2"/molten-gantry-301621-06b56bfa11e8.json"

export GOOGLE_APPLICATION_CREDENTIALS=$2

echo "Creating an AWS Redshift Cluster named "$REDSHIFT_CLUSTER""
aws redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER --node-type dc2.large --master-username $REDSHIFT_USER --master-user-password $REDSHIFT_PASSWORD --cluster-type single-node --publicly-accessible --region us-west-2 --vpc-security-group-ids $REDSHIFT_VPC >> setup.log

while :
	do
	   echo "Waiting for Redshift cluster "$REDSHIFT_CLUSTER" to start"
	   sleep 60
	   REDSHIFT_CLUSTER_STATUS=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2 --query 'Clusters[0].ClusterStatus' --output text)
	   if [[ "$REDSHIFT_CLUSTER_STATUS" == "available" ]]
	   then
		break
	   else
	   	echo "Currently the status is: "$REDSHIFT_CLUSTER_STATUS
	   fi
	done

echo "Redshift cluster $REDSHIFT_CLUSTER created successfully"

REDSHIFT_HOST=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2 --query 'Clusters[0].Endpoint.Address' --output text)

echo "Enter the following info in config.cfg"
echo "[redshift_connection]"
echo "host="$REDSHIFT_HOST
echo "database="$REDSHIFT_DATABASE
echo "user="$REDSHIFT_USER
echo "port="$REDSHIFT_PORT
echo "password="$REDSHIFT_PASSWORD
echo "[aws_connection]"
echo "aws_access_key_id="$(aws configure get aws_access_key_id)
echo "aws_secret_access_key="$(aws configure get aws_secret_access_key)














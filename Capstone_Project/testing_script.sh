#!/bin/bash


# SERVICE_NAME=sde-batch-de-project
# IAM_ROLE_NAME=sde-spectrum-redshift
# REDSHIFT_VPC=redshift-security-group
REDSHIFT_VPC=sg-04ff7027cc7a3c542

# REDSHIFT_USER=sde_user
# REDSHIFT_PASSWORD=sdeP0ssword0987
# REDSHIFT_PORT=5439

host=redshift-cluster-1.crlmb3zbf4dr.us-west-2.redshift.amazonaws.com
database=dev
REDSHIFT_CLUSTER=redshift-cluster
REDSHIFT_USER=redshift-user
REDSHIFT_PORT=5439
REDSHIFT_PASSWORD=Redshift123

echo "Creating bucket "$1""
# aws s3api create-bucket --acl public-read-write --bucket $1 --output text >> setup.log

if ! [aws s3 ls "s3://my-bucket" 2>&1 | grep -q 'An error occurred']
then 
	aws s3api create-bucket --acl public-read-write --bucket $1 --output text --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2  >> setup.log
else
    echo "bucket does not exist or permission error."
fi


# echo "Creating an AWS Redshift Cluster named "$REDSHIFT_CLUSTER""
# # aws redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER --node-type dc2.large --master-username $REDSHIFT_USER --master-user-password $REDSHIFT_PASSWORD --cluster-type single-node --publicly-accessible --iam-roles "arn:aws:iam::"$AWS_ID":role/"$IAM_ROLE_NAME"" >> setup.log
# aws redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER --node-type dc2.large --master-username $REDSHIFT_USER --master-user-password $REDSHIFT_PASSWORD --cluster-type single-node --publicly-accessible --region us-west-2 --vpc-security-group-ids $REDSHIFT_VPC >> setup.log

# while :
# do
#    echo "Waiting for Redshift cluster "$REDSHIFT_CLUSTER" to start, sleeping for 60s before next check"
#    sleep 60
#    REDSHIFT_CLUSTER_STATUS=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2  --query 'Clusters[0].ClusterStatus' --output text)
#    if [[ "$REDSHIFT_CLUSTER_STATUS" == "available" ]]
#    then
# 	break
#    fi
# done

# REDSHIFT_HOST=$(aws redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER --region us-west-2 --query 'Clusters[0].Endpoint.Address' --output text)


Covid Analysis all over the world

# Purpose

The notorious Covid-19, has right now become a part of everyone's lives decisions. It's a daily routine to check the number of cases all over the world, and to get sense of which countries in the world have most cases, and deaths. For anyone manufacturing medical products to help the covid patients globally, or for anyone tracking the numbers for planning the travel, this project is very helpful. Our goal is to build highly available, scalable, and real-time data source to provide updates for the number of active Covid-19 cases and deaths globally. Also, we have data quality checks to ensure the data doesn't contain any discrepancies and unexpected results. 

## Datasets

### The Worldcovid data set from the Google Big Query. 
It's a publicly available data, sourced from trusted sources like CSSE at Johns Hopkins University and government agencies, covering a wide range of metrics including confirmed cases, new cases, % population, mortality rate and deaths, aggregated at various geographic levels including city, county, state and country. New data is published on daily basis.

### Geocoding and Positioning data from PositionStack API
PositionStack API is used for obtaining Geocoding related information for a given latitude longitude pair. It provides all location based information such as postal code, address, street, state, region, country. The Worldcovid data set contains lat-lon information for most of it's data, which is used to query the detailed and usable geocoding information from PositionStack API. 

## Tech Stack used

Google Big Query
AWS S3
AWS Redshift
Tableau
Python library: boto3, google, pandas

<!-- ![IntendedCapstoneProjectWorkflow](readme_images/IntendedCapstoneProjectWorkflow.png) -->

![CapstoneProjectWorkflow](readme_images/CapstoneProjectWorkflow.png)

Tableau Link: https://public.tableau.com/app/profile/gayatri.ganapathy/viz/WorldCovid_16405002080110/Dashboard2?publish=yes

# Data Model

![DataModel-StarSchema](readme_images/DataModel-StarSchema.png)

# Project Steps

![ProjectSteps](readme_images/ProjectSteps-1.png)




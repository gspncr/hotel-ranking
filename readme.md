[![Build Status](https://dev.azure.com/gspncr/facility-scoring/_apis/build/status/gspncr.facility-scoring?branchName=master)](https://dev.azure.com/gspncr/facility-scoring/_build/latest?definitionId=1&branchName=master)

[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/gspncr/gspncr%2Ffacility-scoring%2Ffacility-scoring?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWM3YmQ5NzgzMDU2OTc1MTdiNzE2OTE2.iDFBIDm5TkPau_1RhFNBVAHdEFNoBrokFJc28CMxZsw&type=cf-1)]( https://g.codefresh.io/pipelines/facility-scoring/builds?repoOwner=gspncr&repoName=facility-scoring&serviceName=gspncr%2Ffacility-scoring&filter=trigger:build~Build;branch:master;pipeline:5c7bdc49510767514829da0b~facility-scoring)

# 🚽

A scoring system for facilities visited at sites. Bring your own postgresQL DB. Written in Flask and DB Flask Alchemy to access PostgreSQL 11 data store

## How to use
The code is publicly there and a dockerfile is provided. Do not publish the docker image to a public repo with your database settings, use an environment variable (unpublished) or do not even publish publicly at all. why anyway ¯\_(ツ)_/¯

### Using the Dockerfile
The Dockerfile is requiring dev tools for Python, GCC is required in the build because the PostgreSQL adaptor is written in C so need a framework to convert that, and postgresql-dev of course.
`docker run -t -d --name facility-rating -p 8080:8080 facility-rating`
The docker image will run with port 8080 exposed so either modify that in your own run or change the port when you are running the image. In Kubernetes I am doing this setting an external service to :80 :443 mapping to :8080

### Example?
https://toilet.gspncr.com

## What do I do for the DB?
Include an environment variable in the format `FS_DB=postgres://db-user:db-password@db-hostname:5432/DBNAME?sslmode=require`

After that, in your environment, apply the configuration by executing (once 🙃) `dbsetup.py`

## What do I do for Twilio?
First up, Twilio module is absolutely optional. There is more on it in the Wiki
Include an environment variable for the auth and the SID
`twilio_account_SID=string`
`twilio_auth_token=string`

## What libraries?
Flask and Flask SQL Alchemy
You might also need `build-deps, gcc, python-dev, musl-dev, postgresql-dev` in your environment (see the Dockerfile explicitly calls else will fail) which most dev machines will already have otherwise install these libraries in your machines Python env.

[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/gspncr/gspncr%2Fhotel-ranking%2Fhotel-ranking?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWM3YmQ5NzgzMDU2OTc1MTdiNzE2OTE2.iDFBIDm5TkPau_1RhFNBVAHdEFNoBrokFJc28CMxZsw&type=cf-1)]( https://g.codefresh.io/pipelines/hotel-ranking/builds?repoOwner=gspncr&repoName=hotel-ranking&serviceName=gspncr%2Fhotel-ranking&filter=trigger:build~Build;branch:master;pipeline:5c9bb36dffcc2195f0091f0e~hotel-ranking)

# 🏨

A scoring system for hotels. Bring your own postgresQL DB. Written in Flask and DB Flask Alchemy to access PostgreSQL 11 data store

## How to use
The code is publicly there and a dockerfile is provided. Do not publish the docker image to a public repo with your database settings, use an environment variable (unpublished) or do not even publish publicly at all. why anyway ¯\_(ツ)_/¯

### Using the Dockerfile
The Dockerfile is requiring dev tools for Python, GCC is required in the build because the PostgreSQL adaptor is written in C so need a framework to convert that, and postgresql-dev of course.
`docker run -t -d --name hotel-rating -p 8080:8080 hotel-rating`
The docker image will run with port 8080 exposed so either modify that in your own run or change the port when you are running the image. In Kubernetes I am doing this setting an external service to :80 :443 mapping to :8080

### Example?
https://hotels.gspncr.com

## What do I do for the DB?
Include an environment variable in the format `HS_DB=postgres://db-user:db-password@db-hostname:5432/DBNAME?sslmode=require`

After that, in your environment, apply the configuration by executing `dbsetup.py`

## What do I do for Twilio?
First up, Twilio module is absolutely optional. There is more on it in the Wiki
Include an environment variable for the auth and the SID
`twilio_account_SID=string`
`twilio_auth_token=string`

## What libraries?
Flask and Flask SQL Alchemy
You might also need `build-deps, gcc, python-dev, musl-dev, postgresql-dev` in your environment (see the Dockerfile explicitly calls else will fail) which most dev machines will already have otherwise install these libraries in your machines Python env.

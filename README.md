# coding-challenge
Coding Challenge

## Challenge 1 

Requirements 

You are a data engineer at Globant and you are about to start an important project. This project
is big data migration to a new database system. You need to create a PoC to solve the next
requirements:
1. Move historic data from files in CSV format to the new database. (Completed)
2. Create a Rest API service to receive new data. This service must have: 
- Each new transaction must fit the data dictionary rules.(Completed)
- Be able to insert batch transactions (1 up to 1000 rows) with one request. (Completed)
- Receive the data for each table in the same service. (Completed)
- Keep in mind the data rules for each table. (Completed)
3. Create a feature to backup for each table and save it in the file system in AVRO format. (In Progress)
4. Create a feature to restore a certain table with its backup. (Not Started)

You need to publish your code in GitHub. It will be taken into account if frequent updates are
made to the repository that allow analyzing the development process. (Completed)

### Clarifications
1. You decide the origin where the CSV files are located. (Completed)
2. You decide the destination database type, but it must be a SQL database. (Completed)
3. The CSV file is comma separated. (ok)
4. "Feature" must be interpreted as "Rest API, Stored Procedure, Database functionality,
Cron job, or any other way to accomplish the requirements". (ok)

### Not mandatory, but taken into account:
1. Create a markdown file for the Readme.md (Completed)
2. Security considerations for your API service (Completed)
3. Use the Git workflow to create versions (Completed)
4. Create a Dockerfile to deploy the package (Completed)
5. Use cloud tools instead of local tools (Completed)
You can use Python, Java, Go or Scala to solve it! -> Python :)

## Solution Notes

- Developed using an Azure Blob Storage, Flask API and SQLite (SqlAlchemy)
- The solution includes JWT for Security 
- The solution API is deployed by using docker 
- The metadata is handled by marshmallow 
- The app includes swagger-ui for api documentation
- The solution will be deployed in Render.com

## Challenge 2 

## Solution Notes 

- Endpoints to Get All Jobs, Departments, Hired_Employees Completed 
- PowerBi Report (Pending)



# Birthday Reminder App
## About the project
### Description
The Birthday Reminder application is a simple REST API that allows users to save and retrieve their birthday information. Users can update their username and date of birth (YYYY-MM-DD format), and the application counts down the days to their birthday or provides a personalized birthday message if the special day is today.

## Getting Started
The solution contains two Dockerfiles - one for PostgreSQL DB and the second one to bring up the Python app with Birthday API.
For local deployment:
1. Create a docker network to allow communication between db and python containers
   ```
   docker network create db-app-network
   ```
2.  Bring up the DB
     ```
     docker build -t postgres-db ./psql-db
     docker run --name postgres-db --network db-app-network -d postgres-db
     ```
     This will bring up the container with a created database named "db"   
3. Bring up the python app
   ```
   docker build -t birthday-python-app ./birthday-reminder-app
   docker run -it --rm --name bday-python-app --network db-app-network birthday-python-app
   ```
   This will bring up a container with started python process that will process the API calls.

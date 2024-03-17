# split-bill-ms

It is a backend service for split-a-bill app to maintain and settle expenses.

Here is the project structure:
1. assets: For storing any pictures/data files etc
2. db: For establishing connection with our dynamo db
3. models: For defining all the data models we will be using throughout this project
4. apis: For defining all of the api paths (or controllers)
5. services: For creating the core logic used by each api
6. utils: For creating utility functions

app.py: Contains the main initialization of the Flask app instance
config.py: Will contain constants and other configuration parameters( e.g. db connection strings etc)

<u>Checking if the app is up and running</u>

hit the endpoint GET /admin/health in the browser url bar
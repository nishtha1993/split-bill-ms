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

GENERAL CODE GUIDELINES:
1. write the api call under /apis, the logic of which should be in a corresponding file under /services. e.g. /apis/user.py each api would call corresponding /services/user.py
2. In the services code, modularize it completely where each small piece of functionality is written as a function and placed under /utils for reuse across the project
3. Log everything everwhere, propogate the requestId which is generated in the first line of every api call all the way down.
4. If at all your api needs input schema validation put it under /models ( see /models/user.py for example)

EXAMPLE CODE FOR DYNAMO

Check out example from previous commit here
https://github.com/nishtha1993/split-bill-ms/blob/9029277c8ce6ca35b35676ff9031ff9c6202d594/application.py
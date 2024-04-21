# split-bill-ms

It is a backend service for split-a-bill app to maintain and settle expenses.

Here is the project structure:
1. src/models: For defining all the data models we will be using throughout this project
2. src/apis: For defining all of the api paths (or controllers)
3. src/services: For creating the core logic used by each api
4. src/utils: For creating utility functions
5. .github/workflows: Contains github actions for deployment to Elastic BeanStalk

app.py: Contains the main initialization of the Flask app instance
config.py: Contains constants and other configuration parameters( e.g. db connection strings etc)

# APIS IMPLEMENTED:
Expense <br>
1. /expense/addExpense

Friend <br>
2. /friend/getMyFriends
3. /friend/getMyFriendsHistory
4. /friend/settle
5. /friend/nudge

Group <br>
6. /group/getMyGroups <br>
7. /group/createGroup <br>
8. /group/joinGroup <br>
9. /group/getGroupStats <br>
10. /group/getGroupExpenses <br>

ML <br>
11. /ml/parseFromTextract <br>

S3 <br>
12. /s3/put/<bucket> <br>

Search <br>
13. /search/search-expense/<expenseName> <br>
14. /search/search-group/<groupName> <br>

User <br>
15. /user/signin <br>
16. /user/get_user/<email> <br>
17. /delete/<email> <br>


# GENERAL CODE GUIDELINES FOLLOWED:
1. write the api call under /apis, the logic of which should be in a corresponding file under /services. e.g. /apis/user.py each api would call corresponding /services/user.py
2. In the services code, modularize it completely where each small piece of functionality is written as a function and placed under /utils for reuse across the project
3. Log everything everwhere, propogate the requestId which is generated in the first line of every api call all the way down.
4. If at all your api needs input schema validation put it under /models ( see /models/user.py for example)






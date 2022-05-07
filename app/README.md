# Welcome!

Hi! this your determinant test for the position of Django backend developer at **LibertyAssured**.  If you have any issues, you can read this docs or also contact Lolu for further clarification.


##  Overview

For this exercise you will be cover some basic concepts of web development and production ready deployment  and you will hence be tested in the following basic concepts.

- Django and Django query-sets
- PostgreSQL Setup and connection to Django
- Cloud deployment
- PEP guidelines, conformity and quality of code 
- General understanding of the python programming language.

## Test Rundown

You will be required to fork this repository into your personal account and then carry out few operations of extending functionality of the application and then make a pull request with your branch name to the **Liberty** main branch as you progress.

## Test Guide

After completing stage the process in in the rundown, please create branch for your self, please make sure to name the the branch with the following convention **\<yourname>/update**, and also all commits to your branch should carry a message in the following format **\<ACTIVITY>[Activity details]**.

- A sample branch name would be **paul/update**, and., 
- A sample commit message would be **FIX[ADDED CORS CONTROL]**

## Task Description

You are required to extend a skeleton application to such that it can recreate or conform to the responses which you would be seeing below.
**----------------**
- Request -> register (Create User account)
```yaml
{
"email":"teiker@libertymail.com",
"username":"way2teiker",
"password":"Solarizedgowns",
}
```
- Response -> 
```yaml
{
   "message": "Created user successfully",
   "username": "way2teiker",
   "status-code": 200
}

``` 
**---------------------**
- Request -> get_all_coins (Get and display all coins)
- Response -> 
```yaml
[{
   "name": "BTC",
   "USD-PRICE": "42,3529",
   "volume": "19,331,340"
},
{
   "name": "SAND",
   "USD-PRICE": "100",
   "volume": "19,331,340,302"
},
{
   "name": "ETH",
   "USD-PRICE": "4,356",
   "volume": "199,331,340"
}
]
``` 
**---------------------**
- Request -> add_favourite (Add favourite coins to username)
```yaml
{
"username":"way2teiker",
"favourite":"USDT",
}
```
- Response -> 
```yaml
{
   "message": "Added USDT to Favourite successfully",
   "username": "way2teiker",
   "coin-name": "USDT",
   "status-code": 200
}
``` 
**---------------------**
- Request -> view_favourites (Add favourite coins to username)
```yaml
{
"username":"way2teiker"
}
```
- Response -> 
```yaml
{"message":"Welcome back way2teiker thanks for using our platform",
"subscribed_favourites": [
                            {
							   "name": "BTC",
							   "USD-PRICE": "42,3529",
							   "volume": "19,331,340"
							},
							{
							   "name": "SAND",
							   "USD-PRICE": "100",
							   "volume": "19,331,340,302"
							},
							{
							   "name": "ETH",
							   "USD-PRICE": "4,356",
							   "volume": "199,331,340"
							}
				        ]      
``` 
** **---------------------** **

## Resources for task

Please register on https://docs.coinapi.io/?python#exchange-rates for free and get an api-key for your use.
Once this is done you can use their API docs for the propagation of your task.

**Finally**
You have been provided with a virtual machine IP address hosted on Digital Ocean please host your project appropriately using NGINX,  GUNICORN and POSTGRESQL (as database). A password for the droplet will be provided.

- Please add your postman link to the above created endpoints for review.
- Also note that you can ignore the Docker and CI/CD instantiations on the application.

### Good luck, as we look forward to working with you at Liberty Assured in building amazing projects and relationships.
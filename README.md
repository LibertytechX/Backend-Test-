
# Welcome!

Hi! this your determinant test for the position of Django backend developer at **PayBox360**.  If you have any issues, you can read this docs or also contact Lolu for further clarification.


##  Overview

For this exercise you will be cover some basic concepts of web development and production ready deployment  and you will hence be tested in the following basic concepts.

- Django and Django query-sets
- PostgreSQL Setup and connection to Django
- Cloud deployment
- PEP guidelines, conformity and quality of code 
- General understanding of the python programming language.

## Test Rundown

You will be required to fork this repository into your personal account and then carry out few operations of extending functionality of the application and then make a pull request with your branch name to the main branch as you progress.

## Test Guide

After completing stage the process in in the rundown, please create branch for your self, please make sure to name the the branch with the following convention **\<yourname>/update**, and also all commits to your branch should carry a message in the following format **\<ACTIVITY>[Activity details]**.

- A sample branch name would be **paul/update**, and., 
- A sample commit message would be **FIX[ADDED CORS CONTROL]**

## Task Description

You are required to extend a skeleton application and build it into an inventory management system to such that it can provide the abilities below:


**Project: Simple E-commerce API**

**Requirements:**
1. **User Management:**
   - Implement user registration and login with JWT authentication.
   
2. **Product Management:**
   - Create models for Product and Category.
   - Implement CRUD operations for products (create, read, update, delete).

3. **Order Management:**
   - Create an Order model.
   - Allow users to place orders with multiple products.
   - Implement a basic order history endpoint for users.

**Detailed Instructions:**

1. **Setup:**
   - Create a new Django project.
   - Configure the project with Django REST Framework.
   - Make sure to use PostgreSQL

2. **User Authentication:**
   - Use Django's built-in User model.
   - Implement registration and login endpoints using JWT for authentication.

3. **Product and Category Models:**
   - Create models with appropriate fields (e.g., name, description, price for Product; name for Category).
   - Establish relationships (e.g., a product belongs to a category).
   - Implement endpoints for managing products (list, detail, create, update, delete).

4. **Order Model:**
   - Create an Order model with fields like user (ForeignKey), product (ManyToManyField), quantity, and date.
   - Implement an endpoint for placing orders.
   - Create an endpoint to retrieve the order history for the authenticated user.

5. **Testing:**
   - Write unit tests for each endpoint.

**Evaluation Criteria:**
- Correctness: The implementation should meet the requirements.
- Code Quality: Clean, readable, and maintainable code.
- Use of Django Best Practices: Proper use of Django features and conventions.
- Testing: Quality and coverage of unit tests.

**Bonus:**
- Implement search functionality for products.
- Add pagination to product listing.


## Resources for task

**Finally**
You will be provided with a virtual machine IP address hosted on Digital Ocean please host your project appropriately using NGINX,  GUNICORN and POSTGRESQL (as database). A password for the droplet will be provided.

- Please add your postman link to the above created endpoints for review.
- Also note that you can ignore the Docker and CI/CD instantiations on the application.

### Good luck, as we look forward to working with you at Liberty Assured in building amazing projects and relationships.



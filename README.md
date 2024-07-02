# Ecommerce Project

## Features

### 1. User Management

- **User Registration and Login**: Users can register an account and log in using JWT authentication, ensuring secure access to the platform.

### 2. Product Management

- **CRUD Operations for Products**: Allows for creating, reading, updating, and deleting products, providing complete control over the product catalog.
- **Product Categorization**: Enables organizing products into categories for better navigation and searchability.
- **Image Upload and Management**: Handles product images, including uploading, updating, and deleting images.


### 3. Category Management

- **Create Category**: Allows for creating new product categories, enabling better organization of the product catalog.
- **Read Category**: Provides details of a specific category, including its name and associated products.
- **Update Category**: Allows for updating existing category information, such as changing the category name or description.
- **Delete Category**: Allows for deleting a category, removing it from the product catalog.
- **List Categories**: Retrieves a list of all categories, enabling easy navigation and management of product groupings.


### 4. Order Management

- **Order Placement and Processing**: Users can place new orders and process existing ones, ensuring smooth order transactions.
- **Order History and Tracking**: Users can view and track the history of their orders..

### 5. Search and Filtering

- **Full-text Search for Products**: Provides comprehensive search functionality across the product catalog.
- **Pagination for Product Listings**: Manages pagination to ensure efficient loading and display of product listings.

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional, for containerization)

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/Nathan-Yinka/Ecommerce-Backend-Test.git
    cd Ecommerce-Backend-Test
    ```

2. Create a virtual environment and install dependencies:
    #### macOS/Linux
        ```bash
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

    #### Windows
        ```bash
        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt
        ```

3.  ``` bash
        cd app

    ```

4. Run database migrations:
    ```bash
    python manage.py migrate --settings=app.settings.local
    ```

5. Start the development server:
    ```bash
    python manage.py runserver --settings=app.settings.local
    ```

6. Access the application at `http://localhost:8000`

### Using Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/Nathan-Yinka/Ecommerce-Backend-Test.git
    cd Ecommerce-Backend-Test
    ```

2. Ensure Docker is installed and running on your machine.

3. Build and start the containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

4. Access the application at `http://localhost`

## API Documentation

Detailed API documentation can be found [here](https://documenter.getpostman.com/view/28578777/2sA3dvkChF). It includes endpoints for user authentication, product management, order processing, and more.

## Testing

Unit tests and integration tests are implemented to ensure the application's reliability. Run tests using:
```bash
python manage.py test --settings=app.settings.local

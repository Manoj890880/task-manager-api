## Task Manager API

The Task Manager API is a simple RESTful API built using Flask that allows you to manage tasks. It provides endpoints to create, retrieve, update, and delete tasks. The API uses MySQL as the underlying database to store task information.

## Table of Contents

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
  - [1. Hello World Endpoint](#1-hello-world-endpoint)
  - [2. Get All Tasks](#2-get-all-tasks)
  - [3. Get a Specific Task](#3-get-a-specific-task)
  - [4. Add a New Task](#4-add-a-new-task)
  - [5. Update a Task](#5-update-a-task)
  - [6. Delete a Task](#6-delete-a-task)
- [Error Handling](#error-handling)
- [Data Storage](#data-storage)
- [API Security](#api-security)
- [API Documentation](#api-documentation)
- [Conclusion](#conclusion)

## Getting Started

To run the Task Manager API on your local machine, follow these steps:

1. Install the required dependencies:

2. Clone the repository and navigate to the project folder.

3. Ensure you have a MySQL database set up. The API assumes that the MySQL database is running locally, and the required configuration is provided in the code.

4. Run the API server:

The API will be accessible at `http://localhost:5000/`.

## API Endpoints

### 1. Hello World Endpoint

**URL:** `/`

**Method:** GET

**Description:** A simple endpoint that returns a hello message.

**Response:**
- 200: Returns a simple hello message.

### 2. Get All Tasks

**URL:** `/tasks`

**Method:** GET

**Authentication:** Basic Authentication (Username: admin, Password: admin)

**Description:** Retrieves a list of all tasks from the database.

**Response:**
- 200: Returns a JSON object containing a list of tasks.

### 3. Get a Specific Task

**URL:** `/tasks/<int:task_id>`

**Method:** GET

**Authentication:** Basic Authentication (Username: admin, Password: admin)

**Description:** Retrieves a specific task by its ID from the database.

**Parameters:**
- task_id (int): ID of the task to retrieve.

**Response:**
- 200: Returns a JSON object containing the task details.
- 404: If the specified task ID is not found.

### 4. Add a New Task

**URL:** `/tasks`

**Method:** POST

**Authentication:** Basic Authentication (Username: admin, Password: admin)

**Description:** Adds a new task to the database.

**Request Body:**
- title (string, required): Title of the task.
- description (string, required): Description of the task.
- due_date (string, required, format: "YYYY-MM-DD"): Due date of the task.

**Response:**
- 200: Returns a JSON object confirming the successful addition of the task.
- 400: If the request data is invalid or missing fields.

### 5. Update a Task

**URL:** `/tasks/<int:task_id>`

**Method:** PUT

**Authentication:** Basic Authentication (Username: admin, Password: admin)

**Description:** Updates an existing task in the database.

**Parameters:**
- task_id (int): ID of the task to update.

**Request Body:**
- title (string, required): New title of the task.
- description (string, required): New description of the task.
- due_date (string, required, format: "YYYY-MM-DD"): New due date of the task.

**Response:**
- 200: Returns a JSON object confirming the successful update of the task.
- 400: If the request data is invalid or missing fields.
- 404: If the specified task ID is not found.
- 500: If an internal server error occurs.

### 6. Delete a Task

**URL:** `/tasks/<int:task_id>`

**Method:** DELETE

**Authentication:** Basic Authentication (Username: admin, Password: admin)

**Description:** Deletes a task from the database.

**Parameters:**
- task_id (int): ID of the task to delete.

**Response:**
- 200: Returns a JSON object confirming the successful deletion of the task.
- 404: If the specified task ID is not found.
- 500: If an internal server error occurs.

## Error Handling

The API includes error handling for the following HTTP status codes:

- 400: Bad Request - When the request data is invalid or missing required fields.
- 404: Not Found - When the specified task ID is not found.
- 500: Internal Server Error - For other unexpected errors.

## Data Storage

The API stores task data in a MySQL database. The database configuration is provided in the code (`app.py`). Make sure to set up the database before running the API.

## API Security

The API is protected using Basic Authentication. The default credentials for accessing the API are:

- Username: admin
- Password: admin

**Note:** In a production environment, it is recommended to use more secure authentication mechanisms, such as OAuth or JWT.

## API Documentation

The API documentation is generated using Flasgger, which provides Swagger documentation. You can access the API documentation by running the API and visiting `http://localhost:5000/apidocs/`.

## Conclusion

This README file provides an overview of the Task Manager API, its endpoints, authentication, error handling, and data storage. You can use this API to manage tasks in a simple task management system. For any questions or issues, feel free to contact the developer.

Thank you for using the Task Manager API! Happy coding! 🚀

# SoftDesk Support - Project Documentation

## Installation Prerequisites

Before installing the project, ensure you have Pipenv installed on your system. You can find the instructions for installing Pipenv at the following link:

[Pipenv Installation Guide](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)

## Installation Process

### Cloning the Repository

To start, clone the project repository using the following command:

```bash
git clone https://github.com/ErnestoAquino/SoftDesk-Support.git
```

### Accessing the Project Directory

Once the repository is cloned, access the project directory:

```bash
cd SoftDesk-Support
```

### Installing Dependencies

Install the project dependencies by executing:

```bash
pipenv install
```

### Activating the Virtual Environment

Activate the virtual environment created by `Pipenv` with:

```bash
pipenv shell
```

### Starting the Server

Finally, start the project server with:

```bash
python SoftDeskSupportAPI/manage.py runserver
```

---

## Usage Guide

### Using Postman

Postman is recommended for interacting with the API. Below are the steps for the most common operations.

### Creating a User

Make a POST request to the following endpoint to create a new user:

- **URL:** `http://localhost:8000/api/users/`
- **Method:** POST
- **Body:**

  ```json
  {
      "username": "example-name",
      "password": "example-password",
      "age": 20,
      "can_be_contacted": false,
      "can_data_be_shared": false
  }
  ```

---
### Obtaining a Token

Once the user is created, obtain a token for authentication and interaction with the API:

- **URL:** `http://localhost:8000/api/token/`
- **Method:** POST
- **Body:**

  ```json
  {
      "username": "example-name",
      "password": "example-password"
  }
  ```

### Viewing Projects

With the token, you can view a list of projects. However, you won't have access to the details of projects that are not authored by you:

- **URL:** `http://localhost:8000/api/projects/`
- **Method:** GET
- **Authorization:** Bearer Token

### Creating Projects

To create a new project, use your token for authentication:

- **URL:** `http://localhost:8000/api/projects/`
- **Method:** POST
- **Authorization:** Bearer Token
- **Example Body:**

  ```json
  {
      "name": "Example name project",
      "description": "Example description",
      "type": "frontend"
  }
  ```

You will receive a response similar to this:

  ```json
  {
      "url": "http://localhost:8000/api/projects/11/",
      "name": "Example name project",
      "description": "Example description",
      "type": "frontend"
  }
  ```

### Accessing Project Details

Access the details of your project through its URL. Also, you have the option to update (PUT or PATCH) or delete (DELETE) the project from the detail view:

- **URL:** `http://localhost:8000/api/projects/11/`
- **Method:** GET
- **Authorization:** Bearer Token
- **Example Response:**

  ```json
  {
      "id": 11,
      "name": "Example name project",
      "description": "Example description",
      "type": "frontend",
      "created_time": "2023-12-12T15:26:46.883188Z",
      "author_username": "example-name",
      "issues": [],
      "contributors": [
          "example-name"
      ]
  }
  ```

---
### Contributor Management

From the project detail view, you can manage contributors:

#### Viewing Project Contributors

- **URL:** `http://localhost:8000/api/projects/11/contributors/`
- **Method:** GET
- **Authorization:** Bearer Token

#### Adding a Contributor

To add a contributor, send the username of the person:

- **URL:** `http://localhost:8000/api/projects/11/contributors/`
- **Method:** POST
- **Authorization:** Bearer Token
- **Example Body:**

  ```json
  {
      "user": "user6"
  }
  ```

#### Removing a Contributor

To remove a contributor, send the username of the person:

- **URL:** `http://localhost:8000/api/projects/11/contributors/`
- **Method:** DELETE
- **Authorization:** Bearer Token
- **Example Body:**

  ```json
  {
      "user": "user6"
  }
  ```
---
### Issue Management

Only the author or contributors of a project can create and manage issues.

#### Viewing Project Issues

- **URL:** `http://localhost:8000/api/projects/11/issues/`
- **Method:** GET
- **Authorization:** Bearer Token

#### Creating an Issue

- **URL:** `http://localhost:8000/api/projects/11/issues/`
- **Method:** POST
- **Authorization:** Bearer Token
- **Example Body:**

  ```json
  {
      "title": "Title example",
      "description": "Description Example",
      "status": "to_do",
      "priority": "high",
      "tag": "bug"
  }
  ```

#### Accessing Issue Details

To access, modify, or delete an issue (only author):

- **URL:** `http://localhost:8000/api/projects/11/issues/25/`
- **Method:** GET (For details)
- **Method:** PUT or PATCH (For modification)
- **Method:** DELETE (For deletion)
- **Authorization:** Bearer Token

---

## Comments on Issues

Contributors can add and view comments on issues.

#### Viewing Comments on an Issue

- **URL:** `http://localhost:8000/api/projects/11/issues/25/comments/`
- **Method:** GET
- **Authorization:** Bearer Token

#### Creating a Comment

- **URL:** `http://localhost:8000/api/projects/11/issues/25/comments/`
- **Method:** POST
- **Authorization:** Bearer Token
- **Example Body:**

  ```json
  {
      "description": "This is a comment"
  }
  ```



This will return a response like this:

  ```json
  {
      "id": "0b303eb3-9512-4c1f-9cf5-0f6cf47fe5c6",
      "description": "This is a comment"
  }
  ```

#### Accessing Comment Details

Project contributors can access the details of a comment using its ID. Continuing with the previous example:

- **URL:** `http://localhost:8000/api/projects/11/issues/25/comments/0b303eb3-9512-4c1f-9cf5-0f6cf47fe5c6`
- **Method:** GET
- **Authorization:** Bearer Token

The response would be as follows:

  ```json
  {
      "id": "0b303eb3-9512-4c1f-9cf5-0f6cf47fe5c6",
      "description": "This is a comment",
      "author_username": "example-name",
      "created_time": "2023-12-12 16:19:55"
  }
  ```

From this endpoint, contributors can see who created the comment and when. Only the author of the comment can make PUT, PATCH, and DELETE requests.

---

## Deleting a User Account

A user can delete their account, which will cascade delete their projects, issues, and comments:

- **URL:** `http://localhost:8000/api/users/21/`
- **Method:** DELETE
- **Authorization:** Bearer Token

---



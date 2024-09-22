
# Project Name

A Django application utilizing Django REST Framework (DRF) with token authentication, featuring a custom permission system based on user roles and language-specific permissions.

## Table of Contents

- [Introduction](#introduction)
- [Features 🚀](#features-🚀)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [Running Migrations](#running-migrations)
- [Running the Project](#running-the-project)
- [Swagger Documentation](#swagger-documentation)
- [Authentication](#authentication)
  - [Obtaining a Token](#obtaining-a-token)
  - [Using the Token](#using-the-token)
- [Permission Per Language System](#permission-per-language-system)
  - [Models Overview](#models-overview)
  - [Permission Checks](#permission-checks)
  - [Permission Flow](#permission-flow)
  - [Example Usage](#example-usage)
- [Field-Level Permissions with `FieldPermissionSerializer`](#field-level-permissions)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Test Coverage](#test-coverage)
- [Conclusion](#conclusion)

## Introduction

This project is a Django-based web application that provides APIs for content management with fine-grained permission controls. It leverages Django REST Framework for API development and uses token-based authentication for securing endpoints. The application features a custom permission system that allows for role-based access control with additional constraints based on content language.

## Features 🚀

- **Role-Based Access Control**: Assign roles to users with specific permissions.
- **Language-Specific Permissions**: Control access to content based on language.
- **Token Authentication**: Secure APIs using DRF's token authentication.
- **Swagger Integration**: Interactive API documentation available at `/swagger/`.
- **Comprehensive Testing**: Robust test suite covering various permission scenarios.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)
- Git
- Virtualenv (recommended)

## Installation

Follow the steps below to set up the project locally:

### 1. Clone the Repository
```sh
git clone https://github.com/bahaminabbasi/interview-permission-repo.git
cd yourproject
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.
```sh
python -m venv venv
```
Activate the virtual environment:

- On Windows:
```sh
venv\Scripts\activate
```
- On Unix or MacOS:
```sh
source venv/bin/activate
```
### 3. Install Dependencies

Install the required Python packages using `pip`:
```sh
pip install -r requirements.txt
```
Ensure that the `requirements.txt` file exists in the root directory and includes all necessary packages.

## Running Migrations

Before running the project, apply the database migrations to set up the necessary tables:
```sh
python manage.py migrate
```
This will create the database schema based on your Django models.

## Running the Project

Start the Django development server using:
```sh
    python manage.py runserver
```
The application will be accessible at `http://localhost:8000/` by default.

## Swagger Documentation

API documentation is available via Swagger UI. You can access it at:

    http://localhost:8000/swagger/

Replace `localhost:8000` with the appropriate host and port if different.

## Authentication

This project uses Django REST Framework's token-based authentication. To access secured endpoints, you need to include a valid authentication token in your requests.

### Obtaining a Token

To obtain an authentication token, you typically need to send a POST request to the login endpoint with your username and password. For example:

    POST http://localhost:8000/api/v1/auth/auth/login/
    Content-Type: application/json

    {
      "username": "yourusername",
      "password": "yourpassword"
    }

The response will include a token:

    {
      "token": "yourauthtoken"
    }

### Using the Token

Include the token in the `Authorization` header of your requests:

    Authorization: Token yourauthtoken

## Permission Per Language System

The application features a custom permission system that controls user access based on roles and the language of content. Permissions are defined per language, and users can have different permissions for different languages.

### Models Overview

- **User**: Extends Django's `AbstractUser`, includes a `mobile` field and a ManyToMany relationship with `RolePerm`.
- **Role**: Represents a user role (e.g., Editor, Viewer).
- **Perm**: Defines a permission, including the action (e.g., create, update) and the language it applies to.
- **RolePerm**: Associates a `Role` with a `Perm`.
- **PostItem**: Represents content items with a language and author.

### Permission Checks

Permissions are enforced using custom permission classes and helper functions. Key components include:

- **HasRolePermission**: A custom DRF permission class that checks if a user has the required role-based permission for an action and language.
- **Helper Functions**:
  - `check_user_is_owner(user, obj)`: Checks if the user is the author of the object.
  - `check_user_permission_for_object(user, obj, mapped_action, action)`: Checks if the user has permission to perform an action on an object, considering ownership and language.

### Permission Flow

1. **User Authentication**: The user authenticates and provides a token with each request.
2. **Permission Assignment**: Users are assigned roles, and roles are associated with permissions for specific actions and languages.
3. **Request Handling**:
   - For list actions, the queryset is filtered based on the user's permissions for different languages.
   - For object-level actions (retrieve, update, delete), permissions are checked using the helper functions, considering both the action and the language of the content.
4. **Ownership Verification**: For actions that modify content (update, delete), the user must be the owner (author) of the content.

### Example Usage

- A user with the `Editor` role can have `update` permissions for English content but not for French content.
- The permission system ensures that users can only perform actions they are explicitly permitted to, and only on content in languages they have permissions for.

### Field-Level Permissions

The application includes a custom serializer base class, `FieldPermissionSerializer`, which enforces field-level permissions for both read and write operations. By inheriting from this class, other serializers can apply field-level access control based on user permissions.

#### Usage
Just inherit `FieldPermissionSerializer` on your model serializers:
```python
class PostItemSerializer(FieldPermissionSerializer):
    class Meta:
        model = PostItem
        fields = '__all__'
```

### Overview

The `FieldPermissionSerializer` overrides the default serialization and validation methods to check user permissions for each field during serialization (read) and deserialization (write).

### Key Features

- **Field-Level Read Permissions**: Controls which fields are included in the serialized output based on the user's permissions.
- **Field-Level Write Permissions**: Validates that the user has permission to modify specific fields during create or update operations.
- **Dynamic Permission Checks**: Utilizes the user's role-based permissions to determine access at runtime.

### Implementation

Here's the implementation of the `FieldPermissionSerializer`:

## Testing

The project includes a comprehensive test suite to ensure the permission system works as expected.

### Running Tests

Execute the tests using:
```sh
pytest
```
or
```sh
python -m pytest
```
### Test Coverage

The tests cover various scenarios, including:

- **Ownership Tests**: Confirm that users can only modify content they own.
- **Permission Assignment Tests**: Verify that users gain or lose access appropriately when permissions are assigned or removed.
- **Content Modification Tests**: Ensure that changes to content attributes (e.g., language) affect permissions as expected.
- **Dynamic Permission Changes**: Test the system's behavior when permissions or roles are modified during runtime.
- **Edge Cases**: Handle scenarios like deleting permissions, roles, or related objects to ensure the system remains stable.

## Conclusion

This project demonstrates a robust permission system that integrates role-based access control with language-specific permissions. By following the setup instructions and understanding the permission flow, you can effectively utilize and extend the system for your application's needs.

For further assistance or to contribute to the project, please refer to the repository's issue tracker or contact the maintainers.
=======
Checkout to `dev` branch.

Test project's definitions and requirements:

https://docs.google.com/document/d/19Pmr3BzNwnakKvO1jn5vU4Lagh2AuZcGaM32shlrzSk/edit?usp=sharing



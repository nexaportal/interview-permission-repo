
<h3 align="center">Interview Permission Repository</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Platform](https://img.shields.io/badge/platform-reddit-orange.svg)](https://www.reddit.com/user/Wordbook_Bot)
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> 
🚀 This Django project is built with DRF, offering role-based permissions, multi-language support, and automatic API documentation through Swagger. 
</p>

## 📝 Table of Contents

- [About](#about)
- [Features](#features)
- [Setup and Installation](#getting_started)
- [Running the Project](#running)
- [Code Formatting and Linting](#code_quality)
- [Running Tests your own bot](#tests)
- [Authorization](#authorization)
- [Permissions](#permissions)

## 🧐 About <a name = "about"></a>

This project is a Django-based RESTful API using Django REST Framework (DRF) that includes features like role-based permissions, multi-language support for categories and posts, and automatically generated API documentation using Swagger. Additionally, the project integrates code quality tools like Black and Flake8 for formatting and linting.

## ✨  Features <a name = "features"></a>

Role-Based Permissions: Manage user roles and permissions effectively.
Multi-language Support: Handle categories and posts in different languages.
Swagger Documentation: Automatically generated API documentation for ease of use.
Code Quality Tools: Integrated with Black (formatter) and Flake8 (linter).

## 🏁 Setup and Installation <a name = "getting_started"></a>

### Prerequisites
Ensure you have the following installed:

#### . Python 3.8 or later
#### . pip (Python package installer)
#### . virtualenv (optional but recommended)

```
git clone https://github.com/mhdi01/interview-permission-repo
cd yourproject
```

### Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Create a Superuser
```
python manage.py createsuperuser
```
### Run the Development Server
```
python manage.py runserver
````

## 🚀 Running the Project <a name = "running"></a>

To start the development server, run:
```
python manage..py runserver
```
Access the API at: http://127.0.0.1:8000/

For Swagger documentation, visit: http://127.0.0.1:8000/swagger/


## 🛠️ Code Formatting and Linting <a name = "code_quality"></a>

### Black
Black is used for code formatting.

Install Black:
```
pip install black
```
Format the code:

```
black .
```

### flake8
Flake8 checks for style issues and potential errors.


Install flake8
```
pip install flake8
```
Format the code:
```
flake8 .
```

## ✅ Running Tests <a name = "tests"></a>
Run tests :
```
pytest
```

## 📄 Authorization <a name = "authorization"></a>
Simplejwt library used to authorize user credentials.
to authorize user credentials a header will be sent by the request:
header sample is :
```
Authorization : Bearer <Token>
```

## 🛡️ Permissions <a name = "permissions"></a>
#### Different Roles can be defined based on restrictions needed. each role can have multiple permissions to Create/Update/Get/Delete categories or posts.

### Flow:
###### . Create/Update Request: If a user wants to create or update a category or a post , Permissions will be checked based on the language the items have. when they pass the permission layer Field validation Layer will be applied. Field validation layer will validate permitted fields for a user

###### . List/Retrieve Request: If a user wants to list or retrieve a single category or post, Permission will be applied Based on the fields and languages not as a general restriction. It means if an item has an english language and the user doesn`t have credential for english Language, that item wont be shown to ther user. forbidden response wont be sent for that.

## 🔑 Key Points
###### DynamicCategoryItemSerializer is implemented as a restriction for fields to serialize fields needed in the response
###### implementing a simple and easy to read method in the serialization layer for the feature needed.


## 💭 Conclusion <a name = "conclusion"></a>
###### Role Based Permission Service is devided into two different applications.
###### It is tried to develop a robust service which is extendable for more entities as a permission layer.
###### Tests are covered for most test scenarios defined as crtiteria in the service.
###### Libraries added in situation which are useful such as simplejwt , drf-yasg.

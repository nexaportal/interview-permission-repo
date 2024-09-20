# Project Name

A Django application utilizing Django REST Framework (DRF) with token authentication, featuring a custom permission system based on user roles and language-specific permissions.

## Table of Contents

- [Introduction](#introduction)
- [Features 🚀](#features-)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Migrations](#running-migrations)
- [Running the Project](#running-the-project)
- [Swagger Documentation](#swagger-documentation)
- [Authentication](#authentication)
- [Permission Per Language System](#permission-per-language-system)
- [Testing](#testing)
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

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject

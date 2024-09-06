# Flexitables

This project is a Django-based application that allows for dynamic creation and management of database schemas, tables, and columns. It leverages Django REST Framework to provide API endpoints for managing organizations, tables, and columns dynamically.

## Features

- Create and manage organizations with their own database schemas.
- Dynamically create and manage tables within each organization's schema.
- Dynamically add and manage columns within each table.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Cloning the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Akshat0410/flexitables.git
cd flexitables
```


### Building the Docker Containers

Build the Docker containers using Docker Compose:

```bash
docker-compose build
```

### Starting the Application

Start the application using Docker Compose:

```bash
docker-compose up
```
The application should now be running and accessible at `http://localhost:8000`.

### Running Migrations

After building the containers, run the following commands to make and apply migrations:

```bash
docker-compose run django python manage.py migrate
```

## API Endpoints

The application provides the following API endpoints:

- `/api/organizations/` - Manage organizations.
- `/api/organizations/{org_id}/tables/` - Manage tables within an organization.
- `/api/organizations/{org_id}/tables/{table_id}/columns/` - Manage columns within a table.
- `/api/organizations/{org_id}/models` - Returns all the models within the organization.

## Postman Collection

You can find the Postman collection for this project [here](https://drive.google.com/file/d/1D_BgVc7GN4Ic1_O659te5mjpoixd6ALK/view?usp=drive_link).


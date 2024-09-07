# Flexitables

Flexitables is a Django-based application that allows dynamic creation and management of database schemas, tables, and columns. It leverages Django REST Framework to provide API endpoints for managing organizations, tables, and columns on the fly. This flexible structure lets organizations have their own custom database schemas with tables and columns created as needed.

## Features

- **Organization Management**: Create and manage organizations, each with its own database schema.
- **Dynamic Table Management**: Create and manage tables within each organization's schema.
- **Dynamic Column Management**: Add and manage columns dynamically within any table.
- **Data Management**: Manage data within dynamically created tables for each organization.

## Prerequisites

Before starting, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Akshat0410/flexitables.git
```

Move in the cloned repository

```bash
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
Incase you encounter an error here try running the migration in a new bash/terminal and then again `docker-compose up`

### Running Migrations

After building the containers, run the following commands to make and apply migrations:

```bash
docker-compose run django python manage.py migrate
```
The migration file is pushed to this repo, so it is not required to explicitly run the `makemigrations` command

## API Endpoints

The application provides the following API endpoints:

- `/api/organizations/` - Manage organizations.
- `/api/organizations/{org_id}/tables/` - Manage tables within an organization.
- `/api/organizations/{org_id}/tables/{table_id}/columns/` - Manage columns within a table.
- `/api/organizations/{org_id}/tables/{table_id}/data` - Manage data within a table.
- `/api/organizations/{org_id}/models` - Returns all the dynamically created models within an organization.

## Few Points to remember
1. Supported values for db_type in the `organizations` api are:
    - `SQL`
    - `NOSQL`

2. While creating a column, supported values for the data_type are:
    - `CharField`
    - `IntegerField`
    - `BooleanField`

    They are mapped to equivalent `django_fields`.

3. For every table that is created `id` field is created by default, which is the primary key for every table. We donot have support to create `PRIMARY KEY` at runtime.

## Postman Collection

You can find the Postman collection for this project [here](https://drive.google.com/file/d/1fgz8cSjOZ1cmE6V7v06gWoRBOx7z6zt6/view?usp=drive_link).

## Loom Video

Watch the Loom video for a quick overview of the project:

[![Watch the video](https://cdn.loom.com/sessions/thumbnails/https://www.loom.com/share/6d9d1758fb3549c393eb4ee3523ec9f5?sid=95a46071-805b-4342-b8ca-654cb610ab67-with-play-button.png)](https://www.loom.com/share/6d9d1758fb3549c393eb4ee3523ec9f5?sid=56c86d6b-8f67-4131-a1ea-517b34cc0b81)


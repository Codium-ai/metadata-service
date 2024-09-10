




## Run Locally

1. Create an empty PostgreSQL database and update the `settings.dev.toml` file with the database details.
2. Create a virtual environment and install the dependencies.
3. Run `main.py` (a database schema will be generated in your database).
4. View the API Swagger at: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs).

## Run via Docker

1. From the `metadata_service` directory, run:
   ```sh
   docker build -t metadata_service_img .

2. Run the container with:
    ```sh
    docker run -p 8000:8000 metadata_service_img


## Working with Alembic to manade database migrations
Whenever you make changes to the database schema, 
you need to create a databse revision script.
On service startup, alembic will update the db to the latest revision, by running all the revision scripts in order.

### Creating a schema revision

1. create a new revision
    ```sh
    alembic revision -m "create account table"
    ```
   This will generate a new script in migrations directory.
   Implement the upgrade and downgrade functions in the script.

### Other Alembic commands

2. generate revision script
    ```sh
    alembic revision --autogenerate -m "your db change description"
    ```
2. upgrade database
    ```sh
    alembic upgrade head
    ```
3. downgrade database
    ```sh
    alembic downgrade -1
    ```

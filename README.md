# GeoKapti Project

**GeoKapti** is a FastAPI application that allows for location registration and management, as well as calculating distances between them. This app includes an API to create and register locations in MongoDB, measure route distances, and perform asynchronous tasks.

## Features

- **Location Registration**: Allows registration of a location with latitude and longitude coordinates, storing the information in MongoDB.
- **Asynchronous Distance Calculation**: Calculates the total distance between multiple locations asynchronously.
- **Background Task System**: Utilizes Celery and Redis to process distance calculations in the background.
- **Data Validation and Error Handling**: Manages cases with incomplete or invalid data and ensures duplicates are handled when necessary.
- **Logging Integration**: Logs each registration operation for better traceability.
- **API Version**: The current project version is `1.0.0`.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jguerrero10/geokapti.git
   cd geokapti
    ```
2. **Set up the virtual environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies** (using Poetry):

    ```bash
   poetry install
   ```

4. **Configure Docker** Ensure Docker and docker-compose are installed. Then run:

    Create a `.env` file in the root directory and add the following variables:

    ```bash
   docker-compose up -d
    ```
## Usage

### Start the Application

To start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.


### API Documentation

You can view the API documentation in Swagger or ReDoc:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Deployments

You can deploy the project to multiple cloud providers using the _deploy.sh_ script. This script allows you to choose between Azure, AWS, or Google Cloud.

#### Deployment Requirements

Before running the script, ensure that you have:

- Docker installed and configured.
- The CLI tools for each provider:
  - Azure CLI
  - AWS CLI
  - Google Cloud CLI
- Authentication set up for each provider:
  - Azure: Run az login
  - AWS: Run aws configure
  - Google Cloud: Run gcloud auth login

#### Usage

The _deploy.sh_ script takes one argument to specify the cloud provider for deployment:

```bash
./deploy.sh {azure|aws|gcloud}
```

Each deployment function in the script handles the following:

1. **Build the Docker image**: Creates a Docker image for the FastAPI application.
2. **Push the image to the container registry**: Pushes the Docker image to the container registry of the specified cloud provider.
3. **Deploy the container**: Deploys the container to the cloud provider's Kubernetes cluster.

After running the command, the application will be deployed to the specified cloud provider.


### Endpoints

1. **Register a Location**: `POST /api/v1/locations/`

    Register a location with latitude and longitude coordinates.

    ```json
    {
        "name": "Location Name",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    ```
2. **Calculate Distance**: `POST /api/v1/distance/`

    Calculate the total distance between multiple locations.

    ```json
    {
        "locations": [
            {"latitude": 40.7128, "longitude": -74.0060},
            {"latitude": 34.0522, "longitude": -118.2437}
        ]
    }
    ```

3. **Get Distance Result**: `GET /api/v1/distance/{task_id}`

    Retrieve the result of a distance calculation task.

    ```json
    {
        "task_id": "task_id"
    }
    ```
### Example Usage with curl

1. **Register a Location**:

    ```bash
    curl -X POST "http://127.0.0.1:8000/location/" -H "Content-Type: application/json" -d '{"name": "New York", "latitude": 40.712776, "longitude": -74.005974}'
    ```


## Testing

To run the tests, use the following command:

```bash
pytest tests/
```
### Included Tests
- Location Registration Test: Verifies that a location can be successfully registered.
- Data Validation Test: Confirms that the system correctly handles incomplete or invalid data.
- Logging Test: Validates that the logging system records registration events accurately.
- Asynchronous Distance Calculation Test: Ensures distance calculations between locations work correctly in background tasks.

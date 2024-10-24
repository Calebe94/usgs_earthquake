# Code Challenge - Counterpart

This system utilizes the USGS Earthquake public dataset to determine the nearest earthquake above a magnitude of 5.0 concerning specific cities within user-defined date ranges. The system provides results in the format:

**Result for Los Angeles between June 1, 2021, and July 5, 2021:**

The closest Earthquake to Los Angeles was a M 5.7 - South of Africa on June 30

Additionally, the application saves the results for future reference and allows quick access to previously saved results. If no relevant earthquakes were found during the specified dates, a message "No results found" is displayed.

## Components

This project is a backend service written in **Django 4** that provides a system to search for earthquake data by city and date range, offering functionality for city management, earthquake data caching, and real-time search processing using Celery and Redis for task queuing and background processing. Below are the key components and routes:

### Core Features

- **City Management**:
  Cities can be added, listed, and managed via the API. Each city has associated latitude and longitude coordinates and is unique by name and location.

- **Earthquake Data Search**:
  Users can search for earthquakes in a specific city within a given date range. The system checks if the data exists in the cache; if not, it triggers an asynchronous search using Celery.

- **Asynchronous Processing with Celery and Redis**:
  Earthquake searches are handled asynchronously. Once a request is made, a task is created, and users can track the progress and retrieve the results when they are ready.

### API Routes

1. **City Endpoints**:
   - `GET /api/cities/`:
     Retrieves a list of all registered cities in JSON format.

   - `POST /api/cities/`:
     Allows the creation of new cities by providing a name, latitude, and longitude. Each city is validated for unique location and correct geographical coordinates (latitude: -90 to 90, longitude: -90 to 90).

2. **Earthquake Search Endpoints**:
   - `GET /api/cities/<int:city_id>/earthquakes/`:
     Starts a search for earthquakes in a given city within the specified start and end dates. The request triggers an asynchronous task, and the response returns a task ID for tracking.
     - **Query Parameters**:
       - `start_date`: The start of the search period (format: YYYY-MM-DD).
       - `end_date`: The end of the search period (format: YYYY-MM-DD).
     - **Response**:
       JSON with the task ID for tracking the progress of the search.

   - `GET /api/cities/results/<str:task_id>/`:
     Retrieves the results of an earthquake search by the task ID. If the task is still in progress, it returns a "Pending" status; otherwise, it returns the cached search results.

3. **Cached Results Endpoint**:
   - `GET /api/results/`:
     Retrieves all cached earthquake results that have been processed and stored. These results are stored in Redis for fast access and include searches that have completed recently.

### Frontend Integration

- The application is integrated with a **Vue.js** frontend (served from a `vue/index.html` template) to allow users to interact with the API and display search results.

### Infrastructure

- **Database**: PostgreSQL is used as the main database for storing city and cached earthquake data.
- **Task Queue**: Celery is used in conjunction with Redis for handling long-running earthquake search tasks asynchronously.
- **Containerized Environment**: Docker and Docker Compose are used for local development and deployment. Key services include:
  - **Postgres**: For persistent data storage.
  - **Redis**: For caching and task queuing.
  - **Celery**: For running background tasks.
  - **Uvicorn**: ASGI server to serve the Django application.
  - **Node.js**: For building the frontend Vue.js app.

## Install dependencies:

Here are the OS level dependencies. This project is developed in a debian-based Linux distro. But since everything runs in Docker containers, it will run in every OS that has `dockerd` in it.

### For Debian-based distros

Follow these steps to set up the project on a Debian-based Linux distribution:

1. Install dependencies:

Ensure you have the following installed:
* Python >= 3.9
* pip
* poetry
* Docker
* docker-compose

To install Python, pip, and Poetry, run:

``` sh
sudo apt update && sudo apt install -y python3 python3-pip python3-poetry
```

And to install docker and Docker compose we can follow [these steps](https://docs.docker.com/engine/install/debian/) in the official Docker documentation:

``` sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
# Install the docker dependency
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### For macOS

1. Install Dependencies

On macOS, you will need the following:

* Python >= 3.9
* pip
* Poetry
* Docker Desktop (includes Docker Compose)

To install Homebrew if you don’t already have it:

``` bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, install the dependencies:

```bash
brew install python@3.9
brew install poetry
brew install --cask docker
```

Ensure that Docker Desktop is running before proceeding to the next steps.

### For Windows

PS: I personally was not able to test this

Follow these steps to set up the project on a Windows operating system.

1. **Install Dependencies**

On Windows, you'll need the following:

- **Python >= 3.9**
- **pip**
- **Poetry**
- **Docker Desktop** (includes Docker Compose)

#### Step-by-step guide:

1. **Install Python and pip**:
   Download and install Python from the official website: [python.org](https://www.python.org/downloads/). Ensure that you check the option to "Add Python to PATH" during installation.

   After installation, open a command prompt and run:
   ```bash
   python --version
   ```

   This should display the installed Python version. Then, verify that `pip` was installed properly:
   ```bash
   pip --version
   ```

2. [Install Poetry](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0):
   To install Poetry, you can follow the official documentation for Windows, but the easiest way is to use the command prompt or PowerShell. Open a terminal and run:

   ```bash
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

   After the installation, make sure Poetry is added to your system’s `PATH` variable, or you may need to restart your terminal. Then check that Poetry is installed:

   ```bash
   poetry --version
   ```

3. **Install Docker Desktop**:
   Download and install Docker Desktop from the official website: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop).

   After installation, start Docker Desktop and ensure it is running. You can check if Docker is correctly installed by running the following command in your terminal or PowerShell:

   ```bash
   docker --version
   ```

4. **Configure WSL 2**:
   For Docker Desktop on Windows, it's recommended to use **WSL 2** (Windows Subsystem for Linux) for better performance.

   - Install WSL 2 by following the instructions from Microsoft: [Install WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
   - Make sure to configure Docker Desktop to use WSL 2. You can do this in the Docker Desktop settings under "General" by checking the box for "Use the WSL 2 based engine."

5. **Verify Docker Compose**:
   Since Docker Desktop includes Docker Compose, you can verify its installation by running:

   ```bash
   docker-compose --version
   ```

After completing these steps, you should have all the necessary dependencies installed to run the project.

## Setup and Execution

1. Clone the repository:

  ``` sh
  git clone git@github.com:Calebe94/usgs_earthquake.git
  cd usgs_earthquake
  cp .env.example .env
  ```
  In fact, you don't need to copy the `.env.example` to the `.env` file if you don't want to. The `make start` target will do it for you.

2. **Starting the Application**:
   Run the following command to build and start the application:
   ```bash
   make start
   ```
   This will initialize the Django application, start Celery workers, build the frontend, and connect to the Postgres and Redis services.
   After that you can access the web page via http://localhost:8000/ route.

3. **Stopping the Application**:
   To stop the application:
   ```bash
   make stop
   ```

3. **Logs**:
   To view the logs for the web container:
   ```bash
   make logs
   ```

## Interacting with the API
Here are some example `curl` requests based on your Django backend project:

### 1. **Get List of All Cities**
This request retrieves all registered cities from the API.

```bash
curl -X GET http://localhost:8000/api/cities/ \
     -H "Content-Type: application/json"
```

### 2. **Create a New City**
To create a new city, use the following request, providing the `name`, `latitude`, and `longitude` in the request body.

```bash
curl -X POST http://localhost:8000/api/cities/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "San Francisco",
           "latitude": 37.7749,
           "longitude": -122.4194
         }'
```

### 3. **Search for Earthquakes in a City (Asynchronous Task)**
This request starts an asynchronous task to search for earthquakes in a specific city using the city ID and date range (replace `<city_id>` with the actual city ID that you can get via `/api/cities/`).

```bash
curl -X GET "http://localhost:8000/api/cities/<city_id>/earthquakes/?start_date=2023-01-01&end_date=2023-01-31" \
     -H "Content-Type: application/json"
```

#### Example:
```bash
curl -X GET "http://localhost:8000/api/cities/1/earthquakes/?start_date=2023-01-01&end_date=2023-01-31" \
     -H "Content-Type: application/json"
```

This will return a task ID:

```json
{
  "id": "some-task-id"
}
```

### 4. **Get Earthquake Search Results by Task ID**
Once you have the task ID from the previous request, use it to check the status or retrieve the result of the earthquake search.

```bash
curl -X GET http://localhost:8000/api/cities/results/<task_id>/ \
     -H "Content-Type: application/json"
```

#### Example:
```bash
curl -X GET http://localhost:8000/api/cities/results/some-task-id/ \
     -H "Content-Type: application/json"
```

### 5. **Get Cached Earthquake Results**
To retrieve all cached earthquake results from previous searches:

```bash
curl -X GET http://localhost:8000/api/results/ \
     -H "Content-Type: application/json"
```

This will return a list of cached results in JSON format.

### Future Improvements

While this project meets the basic requirements, there are several enhancements that could be made to improve scalability, performance, and user experience. Below are some potential areas for future improvements:

1. Connection Pooling: Currently, each database query opens a new connection, which can lead to performance bottlenecks when scaling. Implementing a connection pooler (e.g., `pgbouncer`) would optimize database connections between Django and PostgreSQL, reducing latency.

2. API Rate Limiting: Introduce rate limiting to prevent abuse and ensure fair usage of the earthquake search endpoints.

3. Background Task Scalability: The current implementation offloads earthquake search tasks to Celery workers, but the task queue could be improved for better scalability. We could implement task priorities and monitoring to track worker health and task failures.

4. Frontend Pagination: For the `GET /api/results/` endpoint that retrieves cached results, pagination and filtering would help manage large datasets more efficiently. Adding parameters such as `limit`, `offset`, and filtering by data ranges.

5. Refactor for Cloud-native: Modularize the application to deploy on Kubernetes or similar container orchestration platforms, enhancing scalability and fault tolerance. In other words, would be great to configure some pipelines for dev and prod environments.

6. Extended Test Coverage: Improve unit and integration test coverage, particularly for edge cases and error handling, ensuring higher system reliability.

7. Monitoring and Obeservability: Integrate logging and monitoring tools such as Grafana, Prometheus or even Sentry to track the health of the system, task processing, and API performance.

I think that these improvements would enhance the robustness, scalability, and user experience of the project, making it more suitable for production environments and high-traffic use cases.

# Developer

| <img src="https://github.com/Calebe94.png?size=200" alt="Edimar Calebe Castanho"> |
|:---------------------------------------------------------------------------------:|
| [Edimar Calebe Castanho (Calebe94)](https://github.com/Calebe94)                  |

# License

All software is covered under the [MIT License](https://opensource.org/licenses/MIT).

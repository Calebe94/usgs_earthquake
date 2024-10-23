# Code Challenge - Counterpart

This system utilizes the USGS Earthquake public dataset to determine the nearest earthquake above a magnitude of 5.0 concerning specific cities within user-defined date ranges. The system provides results in the format:

**Result for Los Angeles between June 1, 2021, and July 5, 2021:**

The closest Earthquake to Los Angeles was a M 5.7 - South of Africa on June 30

Additionally, the application saves the results for future reference and allows quick access to previously saved results. If no relevant earthquakes were found during the specified dates, a message "No results found" is displayed.

## Components:

- **City Creation Endpoint:** Allows the addition of new cities.
- **Earthquake Search Endpoint:** Enables searching for earthquakes within specified date ranges.
  - Search parameters include:
    - Start date
    - End date
  - Returns a results JSON detailing the current search results.

This project serves as a foundational example for developing a backend system that handles earthquake data retrieval efficiently, catering to the needs of our team.

## Dependencies:

* poetry
* Docker
* docker-compose

## Running:

Clone the repository:

``` sh
git clone git@github.com:Calebe94/usgs_earthquake.git
cd usgs_earthquake
cp .env.example .env
```

You can run the project inside a Docker container. To do that you have to build the containers every time you change something in the code:

``` sh
docker-compose up -d --build
```

Now you can access the api via `http://localhost:8000/api/`.

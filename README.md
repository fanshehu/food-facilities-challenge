# Mobile Food Facilities Permit Data Application

This application allows users to search for mobile food facilities permit in San Francisco using various criteria.

# Section 1 - Development Runbook
## Features

- Search by name of applicant with optional status filter
- Search by street name (partial or full)
- Find the 5 nearest food trucks to a given location(latitude, longitude) with optional status filter

## Project Structure

```
├── src/
│   ├── main.py                  # Application entry point
│   ├── api/                     # API endpoints
│   ├── models/                  # Data models
│   ├── services/                # Business logic and data services
│   ├── ui/                      # Frontend UI
│   └── data/                    # Data source)
└── test/                        # Unit tests
```

## Setup and Installation

### Prerequisites

- uv (Python package manager): https://docs.astral.sh/uv/getting-started/installation/

### Installation

1. Create a virtual environment and install dependencies:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

### Running the Application

1. Start the API server:
   ```
   python -m src.main
   ```

2. Access the API documentation at:
   ```
   http://localhost:8000/docs
   ```

3. Access the app UI at:
   ```
   http://localhost:8000
   ```

### Running Tests

```
pytest tests/
```

## Technical Stack

- **Backend**: Python with FastAPI
- **Data Processing**: Pandas
- **Geospatial Calculations**: GeoPy
- **Testing**: Pytest
- **Package Management**: uv

# Section 2 - Backend Service Design 

## Requirement
- As a client, I should be able to search food facility permit data by applicant name of permit.
- As a client, I should be able to search food facility permit data by permit status.
- As a client, I should be able to search food facility permit data by address of permit, the address could be full address or partial of address.
- As a client, I should be able to search nearest food facility permit data by location(latitude, longitude).
- As a client, I should be able to receive up to 5 permits in response when search by location(latitude, longitude).
- As a client, I should be able to use more than 1 query parameters in the same search request.
- As a service, it should be able to store data with size up to 100KB.

## Assumption
- When search permit by applicant name, service should support partial match.
- Service should always return at most 5 permits in the response. 
- The data set size will be up to 100KB level, with up to 1000 rows level.

## Proposal

The problem is to build a backend service which can support client to query mobile food facilities permit data in San Francisco. 

It is proposed to build an application with 1 REST API to support different search criteria, and use in memory data service to store and return data to API layer.

client --> REST API -> Data Service -> Data (in memory)

- REST API: Implement by FastAPI, defines the API between client and service, including data models.
- Data Service: A simple data plane service, which is responsible to process the search logic, and read data from memory.
- Data: The csv data set is loaded to memory when service is initialized. 

## Data Storage Options 
This section mainly discuss the different choice for data storage.
Considering the data size(22kb with ~500 rows data) of mobile food facility permit data set, it is proposed to store the data in memory. Other options are overkill considering the scope of this project. 

### Option 1. In memory (Recommended)
Store the data in server memory. 

Pros:
- Easy implementation 
- Fast IO
Cons:
- Limited by server RAM. Not scalable to large data size(GB level).
- Not flexible on search criteria. When there is a new search criteria requirement, need a new implementation.

### Option 2. SQL server 
Store the data in a SQL server. i.e. SQLite, MySQL.

Pros:
- Suitable for large dataset. Server is scalable.  
- Relatively fast IO
- Flexible to support new search criteria.

Cons:
- Moderate implementation. Extra operation burden.
- Highly coupled with data schema.

### Option 3. NoSQL server 
Store the data in a NoSQL server. i.e. AWS DynamoDB

Pros:
- Suitable for large dataset. Server is auto scale.
- Fast IO

Cons:
- Moderate implementation. Extra operation burden.
- Need to build new index to support new search criteria.

### Option 4. Elastic Search server
Store the data in a ElasticSearch server. i.e. Elastic Search, Open Search.

Pros:
- Suitable for large dataset. Server is scalable. 
- Relatively fast IO
- Out of box features for text query and geo query. Flexible to add new search criteria. 

Cons:
- Complex implementation. Extra operation burden.

## Nearest Location Design
The problem is to find the k nearest location for a given location(latitude, longitude).

To find the distance between two locations(latitude, longitude), it is proposed to use python library geopy, which leverage Google GeoCoding API to calculate the geo distance under the hood. https://github.com/geopy/geopy

### Option 1 - Calculate Distance during Runtime (Recommended)

The first option is, when there is a new request coming, the service should iterate all locations and calculate the distance between it and target location. And sort and find the nearest k locations. This is suitable for service with low traffic. 

This option is suitable for small dataset like this mobile food facility permit data, which only has 500 rows. However, when dataset scale up, it will increase the request latency significantly.

### Option 2 - Calculate Distance Asynchronously 

When data set is large, we can take a solution to pre-calculate the K nearest locations for each location in dataset. The K nearest locations can be stored as a new dimension/attribute to database. When there is a search request, service only need to retrieve the top K locations from the nearest location list. This is suitable for high traffic.

However, this solution requires extra storage on nearest location. And when dataset location is updated, or new location is added, the service should have capability to re-calculate the nearest locations.

## Critique

### What would you have done differently with more time?
- Implement a proper database instead of loading CSV data in memory, i.e. SQLite
- Implement a better UI which is more user-friendly
- Add better error handling
- Implement a better performed geo location search feature.

### What are the trade-offs you might have made?
- Use in-memory data storage vs. database. For easy implementation but limited scalability and flexibility.
- Calcuate nearest location during runtime vs. pre-calcuate nearest locations. For easy implementation, but limited latency performance.
- Limited API validation and error handling. The UI hardcoded the use cases for API, which save the effort on implementing API validation and error handling on edge cases.  

### What are the things you left out?
- API authentication and authorization
- API throttling
- API pagination
- Logging and monitoring
- Run application with Docker

### What are the problems with your implementation and how would you solve them if we had to scale the application to a large number of users?
These are discussed above on section **Data Storage Options** and **Nearest Location Design**.
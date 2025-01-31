# Weather Data Management Project

This project addresses weather data management, encompassing key stages from data modeling to analysis and API development.

## Steps Covered in the Project

### 1. **Data Modeling**
A well-defined data model representing weather data records has been implemented. The data model captures important weather attributes such as station ID, date, temperature, humidity, and more.

#### Database & Model Structure:
- Refer to the project for details on the specific database system and schema used.
- The weather data model is designed to store raw data from weather stations.
- The weather statistics model is designed to store aggregated annual data, such as average temperature, total rainfall, and more.

### 2. **Data Ingestion**
Code has been developed to ingest raw weather data from files into the database. The ingestion process includes:

- **Duplicate Record Checks**: Ensures no duplicate records are inserted.
- **Logging**: Logs the start and end times of the ingestion process, as well as record counts.
  
Refer to the project for details on the data ingestion code, file formats, and how to run the ingestion process.

### 3. **Data Analysis**
A new data model has been created to store annual weather statistics per year  per station. Code has been implemented to calculate and store these statistics, including:

- **Calculations**: Average temperature, total rainfall, maximum wind speed, etc.
- **Handling Missing Data**: Missing or incomplete data is handled appropriately, using default values or imputation methods.

Refer to the project for more information on the specific analysis performed and the calculations used for annual weather statistics.

### 4. **REST API Development**
A RESTful API has been created using a suitable framework to provide endpoints for accessing the weather data. The API includes:

- **Endpoints**:
  - `api/weather`: Retrieve raw weather data, with support for filtering by station, date range, etc.
  - `api/weather/stats`: Retrieve aggregated weather statistics for a given station and year.
  
- **Features**:
  - Filtering options (station ID, year, date range).
  - Pagination support for large datasets.

#### API Documentation:
- Detailed descriptions of API endpoints, request parameters, and response formats are included in the project.

### 5. **Extra Credit - Deployment**
While not fully implemented in this phase, the project includes plans for deployment, including:

- **Containerization**: Dockerizing the API for easier deployment and scalability.
- **Scheduling Cron Jobs**: Automating data ingestion or analysis tasks using cron jobs.
- **AWS Deployment Strategy**:
  - **ECS** (Elastic Container Service) for deploying Docker containers.
  - **ECR** (Elastic Container Registry) for storing Docker images.
  - **RDS** (Relational Database Service) for database management.
  - **Lambda** for running serverless functions.
  - **API Gateway** for API management and deployment.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aslamkalam/ctva-coding-challenge.git
   cd ctva-coding-challenge

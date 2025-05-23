# Content Generation Service

## Overview
This service is designed to be a flexible and extensible solution for various content generation use cases. It provides a robust API for generating content based on different strategies and output formats, making it easy to adapt to a wide range of applications with minimal modifications.

## Features
- **Multiple Generation Strategies**: Supports various content generation strategies, including default, claim discovery, and evidence discovery.
- **Flexible Output Formats**: Generates content in JSON or text format, with optional schema validation for structured outputs.
- **Extensible Architecture**: Designed with a modular architecture that allows for easy extension and customization to meet specific use cases.
- **Comprehensive Testing**: Includes a suite of tests to ensure reliability and correctness across different scenarios.

## Getting Started
### Prerequisites
- Python 3.12 or higher
- Docker and Docker Compose (optional, for containerized deployment)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd content-generation-service
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the service:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Deployment
To run the service using Docker:
```bash
docker-compose up
```

## Running Tests
To run the tests, use the following command:
```bash
pytest
```

## Running Without Docker
To run the service without Docker, follow these steps:

1. Ensure you have Python 3.12 or higher installed.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI service:
   ```bash
   uvicorn app.main:app --reload
   ```
4. In a separate terminal, start the Streamlit UI:
   ```bash
   streamlit run ui/app.py
   ```
5. Access the API documentation at `http://localhost:8000/docs` and the Streamlit UI at `http://localhost:8501`.

## API Documentation
The API documentation is available at `/docs` when the service is running.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
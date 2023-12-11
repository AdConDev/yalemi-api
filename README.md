# Yalemi API

Yalemi API is a backend service for a Twitter-like social network. It is built with FastAPI and SQLModel, providing a robust and efficient platform for social interactions.

## Features

- User authentication and authorization with OAuth2.
- CRUD operations for user profiles.
- CRUD operations for posts (referred to as "May").
- Real-time updates with WebSockets (if applicable).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/consdotpy/yalemi-api.git
    ```

2. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up your environment variables in a `.env` file. Refer to `.env.example` for required variables.

4. Run the server:

    ```sh
    uvicorn app.main:app --reload
    ```

### Usage

Visit `http://localhost:8000/docs` for interactive API documentation.

### Running tests

WIP

### Deployment

WIP

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI and SQLModel for providing a great foundation for building robust APIs.
- The open-source community for continuous inspiration and resources.

# E-commerce Web Application

A robust e-commerce web application built with Python (Flask), MySQL, and Redis, following a 3-tier architecture (Presentation, Business Logic, Data Access). The application is containerized with Docker for easy deployment and includes comprehensive documentation, API testing support, and a simple Bootstrap-based interface.

## Features

### Customer
- **Register and Login**: Create accounts and authenticate securely.
- **View Products**: Browse available products with details.
- **Add to Cart**: Add products to a Redis-based shopping cart.
- **Place Orders**: Create orders from cart items.
- **Process Payments**: Mock payment processing for order completion.
- **View Order History**: Access past orders (basic implementation).

### Admin
- **Login**: Secure admin authentication.
- **Manage Products and Categories**: Create, update, and delete products and categories.
- **Disable Customer Accounts**: Restrict access for specific users.

## Prerequisites
- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 or higher)
- [Postman](https://www.postman.com/downloads/) (optional, for API testing)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ecommerce-app.git
   cd ecommerce-app
   ```

2. **Build and Run with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - Web interface: [http://localhost:5000](http://localhost:5000)
   - MySQL: `localhost:3306` (user: `root`, password: `password`, database: `ecommerce`)
   - Redis: `localhost:6379`

## Usage

### Web Interface
- **Home Page**: Displays a list of products with options to add to cart.
- **Register**: Create a new customer account at `/register`.
- **Login**: Authenticate at `/login`.
- **Cart**: View and manage cart at `/cart`.
- **Checkout**: Place orders and process payments at `/checkout`.
- **Admin Panel**: Manage products and categories at `/admin` (admin access only).

### API Endpoints
The application provides RESTful APIs for programmatic access. Below are key endpoints with cURL examples. A Postman collection is included in `postman_collection.json`.

#### Register a User
- **URL**: `/api/register`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "testuser",
    "password": "testpass",
    "role": "customer"
  }
  ```
- **cURL**:
  ```bash
  curl -X POST http://localhost:5000/api/register \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpass", "role": "customer"}'
  ```

#### Login
- **URL**: `/api/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "testuser",
    "password": "testpass"
  }
  ```
- **cURL**:
  ```bash
  curl -X POST http://localhost:5000/api/login \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpass"}'
  ```

#### Get Products
- **URL**: `/api/products`
- **Method**: `GET`
- **cURL**:
  ```bash
  curl http://localhost:5000/api/products
  ```

#### Postman Testing
1. Import `postman_collection.json` into Postman.
2. Set the `baseUrl` variable to `http://localhost:5000`.
3. Test endpoints like `/api/register`, `/api/login`, and `/api/products`.

## Testing
Run unit and integration tests using pytest:
```bash
docker-compose exec web pytest tests/
```
Tests are located in the `tests/` directory, covering API endpoints and core functionalities.

## Project Structure
| Directory/File | Description |
|----------------|-------------|
| `app/` | Core application code |
| `app/__init__.py` | Flask app initialization and blueprint registration |
| `app/models/` | Data access layer (MySQL and Redis operations) |
| `app/services/` | Business logic layer |
| `app/routes/` | Presentation layer with Flask blueprints |
| `app/templates/` | HTML templates using Bootstrap |
| `app/static/` | Static files (CSS, JS) |
| `tests/` | Unit and integration tests |
| `Dockerfile` | Docker configuration for the Flask app |
| `docker-compose.yml` | Orchestrates Flask, MySQL, and Redis services |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes unnecessary files from version control |
| `README.md` | Project documentation |
| `postman_collection.json` | Postman collection for API testing |

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines and includes tests.

## License
[MIT License](LICENSE)

## Acknowledgments
Inspired by professional Flask projects like [Flask-RESTful](https://github.com/flask-restful/flask-restful) and [Flask-Login](https://github.com/maxcountryman/flask-login).
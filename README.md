# Project README

This project implements basic authentication using Nginx, JWT (JSON Web Tokens), and Flask.

## Prerequisites
- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-CORS
- Nginx

## Installation
1. Clone the repository to your local machine.
2. Install the required Python packages by running the following command:
   ```
   pip install -r requirements.txt
   ```
3. Configure Nginx to serve the application. Refer to the Nginx documentation for detailed instructions.

## Configuration
1. Modify the `config.py` file to set the desired configuration parameters for the Flask app.
2. Set the appropriate origins in the `routes.py` file to enable Cross-Origin Resource Sharing (CORS) for your application.

## Database Setup
1. Create the necessary database tables by running the following command:
   ```
   python database/db.py
   ```

## Usage
1. Start the Flask app by running the following command:
   ```
   python app.py
   ```
   The app will run on `http://localhost:5000`.
2. Use the provided API endpoints to interact with the authentication system. Below are the available endpoints:
   - `/login` (POST): User login endpoint.
   - `/` (GET): Login form endpoint.
   - `/who_i_am` (GET): Get current user's information.
   - `/logout` (DELETE or GET): Logout endpoint to invalidate the user's token.
   - `/add_user` (POST): Add a new user to the system.
   - `/add_user` (GET): Add user form endpoint.
   - `/delete_user` (POST): Delete a user from the system.
   - `/delete_user` (GET): Delete user form endpoint.
   - `/get_users` (GET): Get a list of all users in the system.
   - `/favicon.ico` (GET): Endpoint to serve the favicon.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
This project utilizes the following libraries and frameworks:
- Flask: https://flask.palletsprojects.com/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- Flask-CORS: https://flask-cors.readthedocs.io/
- Nginx: https://nginx.org/

## Contributors
- [BetaBlaze](https://github.com/Beta-Blaze/auth)

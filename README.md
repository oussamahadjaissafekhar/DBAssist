# Full Stack Application with Flask and React

This repository contains a full-stack application with a Flask backend and a React frontend. Follow the instructions below to set up and run the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Folder Structure](#folder-structure)
- [Additional Notes](#additional-notes)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (for the Flask backend)
- [Node.js](https://nodejs.org/en/download/) (for the React frontend)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)
- [npm](https://www.npmjs.com/get-npm) (Node package manager)

## Backend Setup

1. **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2. **Create and activate a virtual environment (Optional):**

    - **On Windows:**

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

    - **On macOS/Linux:**

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install the backend dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Backend server:**

    ```bash
    python app.py
    ```

    The Flask backend will be running at `http://localhost:5000`.

4. **Exite the virtual environment:**

    To exite the venv mode execute the following command in the command prompt

    ```bash
     deactivate
    ```
## Frontend Setup

1. **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2. **Install the frontend dependencies:**

    ```bash
    npm install
    ```

3. **Start the React development server:**

    ```bash
    npm start
    ```

    The React frontend will be running at `http://localhost:3000`.

## Running the Application

With both the Flask backend and React frontend running, you can access the full application at `http://localhost:3000`. The React frontend will communicate with the Flask backend via API requests.



# Rippo Backend: AI-Powered GitHub Repository Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## 👤 Author

*   **Jerry Davis** - *Initial work* - [jerry@upscaler.net](mailto:jerry@upscaler.net)


Welcome to the backend repository for Rippo! This project uses AI agents to analyze GitHub repositories, providing insightful reports and data for a frontend dashboard.

**Frontend Repository:** [trainboxai/rippo-frontend](https://github.com/trainboxai/rippo-frontend)

## 🤔 What is Rippo?

Rippo connects to your GitHub account, fetches a repository of your choice, and performs a multi-faceted analysis using AI. It generates reports covering:

*   **Code Audit:** Identifies potential issues, anti-patterns, and areas for improvement in your codebase.
*   **Vulnerability Analysis:** Scans dependencies for known security vulnerabilities.
*   **Code Quality Assessment:** Provides an overall evaluation of code quality based on various metrics.
*   **Refactoring Plan:** Suggests concrete steps to refactor and improve the codebase.

These analyses are presented in user-friendly HTML reports and contribute to a dashboard on the frontend (see link above).

## ✨ Features

*   **FastAPI Server:** Handles API requests for user authentication, project/report management, and initiating analyses.
*   **Celery Task Queue:** Manages long-running analysis tasks in the background using Redis as a broker.
*   **GitHub Integration:** Fetches repository data using GitHub OAuth tokens.
*   **AI-Powered Analysis:** Leverages AI models (via imported modules like `analyser`, `reporter`, `recomender`) for code audit, quality checks, vulnerability reporting, and refactoring recommendations.
*   **Firebase Integration:** Uses Firestore for database storage (user data, project/report metadata, usage) and Firebase Storage for hosting generated HTML reports.
*   **Report Generation:** Consolidates analysis results into comprehensive HTML reports.
*   **Usage Tracking:** Monitors analysis runs and associated credit usage (integration with a payment/credit system seems present).

## 🏗️ Architecture Overview

1.  **Frontend Interaction:** The user interacts with the frontend ([rippo-frontend](https://github.com/trainboxai/rippo-frontend)), authenticates (via Firebase), and selects a repository for analysis.
2.  **API Request:** The frontend sends a request to the FastAPI backend (`main.py`).
3.  **Task Queuing:** The `/master` endpoint in FastAPI validates the request and queues a `generate_report` task in Celery (`celery_app.py`).
4.  **Background Processing (Celery Worker):**
    *   A Celery worker picks up the task.
    *   Fetches the repository code (`flattener.py`).
    *   Analyzes dependencies (`analyser.py`).
    *   Searches for vulnerabilities (`search.py`).
    *   Generates various reports using AI (`reporter.py`, `recomender.py`).
    *   Assembles an HTML report (`update_html_report.py`, `template.html`).
    *   Generates an HTML refactor guide (`get_refactor_guide.py`).
    *   Uploads reports to Firebase Storage (`manage_storage.py`).
    *   Updates Firestore database (status, stats, usage) (`update_*.py` modules).
    *   Cleans up temporary files (`clean_up_report_files.py`).
5.  **Frontend Display:** The frontend polls for status updates or fetches the completed report/dashboard data from Firestore/Firebase Storage via the FastAPI backend.

## 🚀 Getting Started

Setting up the Rippo backend involves running the FastAPI server and at least one Celery worker.

**Prerequisites:**

*   Python 3.x
*   Redis (for Celery broker)
*   Firebase Project (for Auth, Firestore, Storage)

**Setup:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/rippo-backend.git # Replace with actual repo URL
    cd rippo-backend/prod
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # You might need to create this file!
    ```
    *(Note: A `requirements.txt` file is not present in the provided list. You'll need to generate one based on the imports in the Python files, e.g., `pip freeze > requirements.txt`)*
3.  **Configure Environment Variables:** Create a `.env` file in the `prod` directory with the following variables:
    ```dotenv
    MIDDLEWARE_SECRET=your_fastapi_session_middleware_secret
    GITHUB_CLIENT_ID=your_github_oauth_app_client_id
    # Add any other environment variables needed by Firebase or other services
    ```
4.  **Firebase Setup:**
    *   **⚠️ Important Security Note:** The code references a Firebase Admin SDK key file (`rippo-777-firebase-adminsdk.json`). **DO NOT COMMIT THIS FILE** to your public repository.
    *   Download your Firebase Admin SDK key file from your Firebase project settings.
    *   Configure Firebase credentials securely. The recommended way is to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your key file:
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
        ```
    *   Alternatively, modify the code in `shared_resources.py` (and potentially `main.py`) to initialize Firebase Admin using this environment variable instead of the hardcoded filename.
5.  **Redis:** Ensure your Redis server is running (default: `redis://localhost:6379/0`). Modify the `broker` URL in `celery_app.py` if your Redis instance is elsewhere.
6.  **Hardcoded Paths:**
    *   **⚠️ Important:** Several scripts (especially `celery_app.py`) contain hardcoded absolute paths (e.g., `/home/trainboxai/backend/rippo/...`). This **will** cause errors on different systems.
    *   You **must** refactor these scripts to use relative paths or configurable base directories to make the project runnable outside its original environment. Look for paths constructed using `os.path.join` referencing `script_dir` and ensure they correctly point to `outputs` and `reports` directories relative to the script location, or introduce environment variables for base paths.
7.  **Run the FastAPI Server:**
    ```bash
    # From the 'prod' directory
    ./fast_api_server.sh start
    # Or: uvicorn main:app --reload --port 8000 (adjust port if needed)
    ```
8.  **Run the Celery Worker:**
    ```bash
    # From the 'prod' directory
    ./manage_celery.sh start
    # Or: celery -A celery_app.celery_app worker --loglevel=info
    ```
9.  **(Optional) Run Celery Flower (Monitoring):**
    ```bash
    # From the 'prod' directory
    ./start_flower.sh
    # Or: celery -A celery_app.celery_app flower
    ```

## 🤝 Contributing

Contributions are welcome! If you'd like to help improve Rippo, please feel free to:

*   Report bugs or suggest features by opening an issue.
*   Submit pull requests with improvements.



## 📜 License

This project is open source. See `LICENSE` file (MIT License) for more details.


---



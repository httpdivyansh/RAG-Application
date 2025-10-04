RAG Application
===============

Overview
--------
This is a Django-based Retrieval-Augmented Generation (RAG) application designed for querying and interacting with PDF documents. It uses LangChain for orchestration, Hugging Face embeddings (e.g., 'all-MiniLM-L6-v2' model) for vectorizing content, and likely integrates tools like FAISS for vector search and PyPDF for PDF parsing. 

The app allows users to upload PDFs and ask questions, retrieving relevant information augmented by AI models. The project follows a standard Django layout, with a main project folder (myproject) and a custom app (docai) handling the core RAG logic.

Folder Structure
----------------
myproject/: The root Django project directory containing the core configuration files.

- manage.py: Command-line utility for running Django administrative tasks (runserver, migrate, makemigrations).
- myproject/ (inner folder):
    - __init__.py: Marks this as a Python package.
    - settings.py: Project settings (installed apps, database, middleware, environment variables).
    - urls.py: Main URL router including app-specific URLs.
    - wsgi.py / asgi.py: Entry points for WSGI/ASGI servers.

docai/: Custom Django app for RAG logic.

- __init__.py: Marks this as a Python package.
- admin.py: Registers models for Django admin.
- apps.py: App configuration.
- models.py: Database models (e.g., document metadata).
- tests.py: Unit tests.
- views.py: Handles PDF upload, embedding generation, and query processing.
- urls.py: App-specific URL patterns.
- migrations/: Database migration files.
- templates/ (optional): HTML templates.
- static/ (optional): CSS, JS, images.

Other Files:

- requirements.txt: Lists Python dependencies (Django, langchain, sentence-transformers, PyPDF2, faiss-cpu, etc.).
- .env (optional, not committed): Stores sensitive info like API keys.
- README.txt: Project documentation (this file).

Optional folders like media/ (uploaded files) or db.sqlite3 (default database) may appear after setup.

Prerequisites
-------------
- Python 3.8+ (3.11 recommended)
- Git
- Optional: Anaconda or virtualenv
- Hugging Face account for API tokens (if required)

Installation Steps
------------------

1. Clone the repository:
   git clone https://github.com/httpdivyansh/RAG-Application.git
   cd RAG-Application

2. Set up a virtual environment:
   python -m venv venv

   Activate it:
   - Windows: venv\Scripts\activate
   - Linux/macOS: source venv/bin/activate

3. Install dependencies:
   - If requirements.txt exists:
     pip install -r requirements.txt
   - Otherwise, manually:
     pip install django langchain langchain-huggingface sentence-transformers transformers PyPDF2 faiss-cpu torch
     # Optional GPU support:
     # pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

4. Set up environment variables (if required):
   Create a .env file:
   SECRET_KEY=your_django_secret_key
   HUGGINGFACE_API_TOKEN=your_hf_token (optional)
   Load them in settings.py using python-dotenv.

5. Apply database migrations:
   python manage.py makemigrations
   python manage.py migrate

Running the Project
-------------------
Start the development server:
python manage.py runserver

Access the app at http://127.0.0.1:8000/ (or the configured port).

Usage
-----
1. Upload a PDF via the web interface.
2. Ask questions; the app retrieves relevant content using embeddings.
3. Ensure embeddings load correctly in docai/views.py for testing.

Troubleshooting
---------------
- Embedding Errors: Uninstall TensorFlow if DLL issues occur (pip uninstall tensorflow). Use PyTorch backend.
- Missing Modules: Run pip freeze > requirements.txt after installation.
- Database Issues: Default is SQLite; configure settings.py for PostgreSQL/MySQL.
- Production: Use Gunicorn + Nginx, set DEBUG=False.

Contributing
------------
- Fork the repository and submit issues or pull requests.
- Ensure tests pass and follow PEP8 style.


# Text Summarizer & QA API

A FastAPI-based REST API for **text summarization** and **question answering based strictly on a provided context** using an AI model through OpenRouter.

## ✨ Features

- 📝 Summarize long texts into concise, readable summaries
- ❓ Ask questions based on a provided reference text
- 🔒 Context-based question answering without adding external information
- 🚀 RESTful API built with FastAPI
- 🤖 AI integration through OpenRouter
- 🌐 Simple web interface served with FastAPI
- ⚙️ Environment variable support for API key management
- 📖 Automatic interactive API documentation with Swagger UI

## 🛠️ Technologies

- Python
- FastAPI
- Pydantic
- OpenAI Python SDK
- OpenRouter API
- Uvicorn
- python-dotenv

## 📋 Requirements

- Python 3.10 or higher
- An OpenRouter API key
- Internet connection

## 📁 Project Structure

```text
Text-Summarizer-QA-API/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── static/
    └── index.html
```

> The `.env` file is not included in the repository for security reasons.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Text-Summarizer-QA-API
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

This project requires an **OpenRouter API key** to communicate with the AI model.

For security reasons, the API key is not included in this repository.

### Create a `.env` file

Create a file named `.env` in the root directory:

```text
Text-Summarizer-QA-API/
│
├── .env
├── main.py
├── requirements.txt
└── ...
```

Add your own API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your personal OpenRouter API key.

> ⚠️ **Never commit or share your `.env` file or API key.**

The `.env` file is excluded from Git using `.gitignore`.

## ▶️ Running the API

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 🌐 Web Interface

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

The project serves the web interface from:

```text
/static/index.html
```

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI to test the API endpoints without writing additional code.

---

# 🔌 API Endpoints

## 1. Summarize Text

### Endpoint

```http
POST /summarize
```

This endpoint receives a text and returns an AI-generated summary.

### Request Body

```json
{
  "text": "Your text with at least 20 characters..."
}
```

### Example Response

```json
{
  "summary": "A concise summary of the provided text."
}
```

### Validation

The `text` field must contain at least **20 characters**.

---

## 2. Ask a Question

### Endpoint

```http
POST /ask
```

This endpoint answers a question based only on the provided reference text.

### Request Body

```json
{
  "context_text": "Your reference text...",
  "question": "Your question?"
}
```

### Example Response

```json
{
  "answer": "The answer based on the provided context."
}
```

### Behavior

The AI is instructed to:

- Use only the provided context
- Avoid adding external information
- Clearly state when the answer cannot be found in the provided text

### Validation

- `context_text` must contain at least **20 characters**
- `question` must contain at least **5 characters**

---

# 🤖 AI Model

The project uses an AI model through OpenRouter:

```text
nvidia/nemotron-3-ultra-550b-a55b:free
```

The API communicates with OpenRouter through the OpenAI-compatible API interface.

## ⚙️ Configuration

The OpenRouter client is configured using:

```python
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
```

This allows the API key to remain outside the source code.

---

# 🔒 Security

The project follows a basic environment-variable approach for API key management.

The following files should **not** be committed to Git:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
```

A `.env.example` file is provided as a template:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Each user should create their own `.env` file and provide their own API key.

> Never publish your real API key on GitHub or include it directly in the source code.

---

# 🧪 Testing the API

After running the application, open:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test:

```text
POST /summarize
POST /ask
```

No additional API testing tool is required.

---

# 🔖 Version

**Current Version: v1.0.0**

### Version History

| Version | Description |
|---|---|
| v1.0.0 | Initial release with text summarization and context-based question answering |

Future releases may include additional features and improvements.

---

# 📌 Future Improvements

Possible future improvements include:

- Improved error handling
- Additional AI models
- More advanced text processing
- Authentication
- Rate limiting
- Improved web interface
- Conversation history
- Additional API endpoints

---

# 📄 License

This project is provided for educational and development purposes.
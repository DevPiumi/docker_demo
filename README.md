
🧠 Women’s Health Assistant – AI-Powered Wellness Recommender
This project is a FastAPI-based backend that predicts a woman’s menstrual cycle phase and generates personalized lifestyle and wellness recommendations using LangChain, OpenAI, and health profile data.

📌 Features
🔄 Cycle Prediction — Predicts the current menstrual cycle phase (Menstrual, Follicular, Ovulation, Luteal).

💡 Personalized Tips — Generates actionable lifestyle and work-life suggestions tailored to the current phase.

🔗 External API Integration — Fetches real-time user health and behavior data from external sources.

🧠 LLM-Driven Intelligence — Utilizes OpenAI's GPT via LangChain to generate contextual, empathetic, and insightful guidance.

🐳 Docker-Ready — Easily deployable as a containerized microservice.



📂 Project Structure
DOCKER_DEMO/
│
├── women_health/                  # Core module
│   ├── __pycache__/               # Compiled Python files
│   ├── main.py                    # FastAPI app with LangChain logic
│   ├── server_apis.py             # API key config and data fetching utils
│
├── Dockerfile                     # Docker config to run FastAPI app
├── main.ipynb                     # Jupyter notebook (probably for testing)
├── requirements.txt              # Python dependencies
├── README.md                      # Project documentation
└── .venv/                         # Python virtual environment




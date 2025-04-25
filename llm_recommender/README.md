
# 🧠 LLM-Based Product Recommendation System

A FastAPI-powered backend service that leverages a pre-trained T5 language model to generate personalized product recommendations based on user preferences and descriptions. The system includes JWT-based authentication, Redis-backed session management, product search, recommendation, and feedback collection functionalities.

---

## 🚀 Features Implemented

### ✅ User Authentication & Session Management
- **JWT Tokens** for stateless authentication
- **Username/password login & signup** (email-free)
- **Secure logout** that clears session tokens
- **Session tokens stored in Redis** for fast lookup and automatic logout on suspicious activity

### ✅ Product Viewing & Retrieval
- `/products/` endpoint returns available products
- Optimized SQLAlchemy queries
- Embedding-powered semantic retrieval for product matching

### ✅ LLM-Based Recommendations
- Integrated **T5 model** for natural language recommendations
- Embedding comparison with stored product data
- Returns the **closest match** + similar suggestions
- LLM usage is isolated to avoid slow response time

### ✅ Feedback Collection
- Endpoint for users to submit feedback on recommendations
- Stores feedback in database for potential fine-tuning
- Tracks which user submitted which feedback

### ✅ Redis Caching (Partial)
- **JWT token validation and session tracking**
- Ready for expansion to cache recommendations, user history, etc.

---

## 🛠 Tech Stack

| Component          | Technology           |
|-------------------|----------------------|
| Backend Framework | FastAPI              |
| Language Model    | HuggingFace T5       |
| Auth              | Custom JWT + Redis   |
| ORM               | SQLAlchemy (async)   |
| Database          | PostgreSQL (or SQLite in dev) |
| Caching/Session   | Redis                |
| Embedding Store   | Vectorized in-memory or persisted |
| Models/Schema     | Pydantic             |

---

## 🧪 REST API Endpoints

### 🔐 Authentication
| Method | Endpoint           | Description        |
|--------|--------------------|--------------------|
| POST   | `/auth/signup`     | Create a new user  |
| POST   | `/auth/login`      | Get JWT token      |
| POST   | `/auth/logout`     | Revoke token       |

### 📦 Products
| Method | Endpoint           | Description                 |
|--------|--------------------|-----------------------------|
| GET    | `/products/`       | Get list of products        |

### 💡 Recommendations
| Method | Endpoint           | Description                             |
|--------|--------------------|-----------------------------------------|
| POST   | `/recommend/`      | Get recommendation based on user input |

### 📝 Feedback
| Method | Endpoint              | Description                 |
|--------|-----------------------|-----------------------------|
| POST   | `/feedback/submit`    | Submit feedback on results |

---

## 🧩 Project Structure

```
app/
├── api/
│   └── v1/
│       ├── routes/
│       │   ├── products.py
│       │   ├── recommend.py
│       │   ├── feedback.py
│       │   └── auth.py
├── core/
│   ├── config.py
│   ├── security.py
├── db/
│   ├── session.py
│   ├── base.py
│   └── models/
│       ├── user.py
│       ├── product.py
│       └── feedback.py
├── services/
│   ├── recommendation_engine.py
│   ├── auth_service.py
│   └── feedback_service.py
main.py
```

---

## 🧑‍💻 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/product-recommendation-llm.git
cd product-recommendation-llm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run Redis (Docker preferred)
docker run -p 6379:6379 redis

# Start the FastAPI app
uvicorn main:app --reload
```

---

## 📌 What's Next?

- 🔄 **Fine-tune the T5 model** on user-product-feedback data
- 📊 Add **monitoring & performance metrics**
- 🧠 Implement **advanced retrieval with hybrid search**
- 🔐 Add **rate limiting & anomaly detection**
- 📈 Deploy to production with CI/CD

---

## 📬 Contact

For questions, reach out to the project maintainer or drop an issue in the GitHub repo. Contributions welcome!

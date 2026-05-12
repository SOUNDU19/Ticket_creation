# NexoraAI – Interview Questions & Answers

**Project:** AI-Powered Ticket Management System (NexoraAI)
**Stack:** Python Flask · scikit-learn · TF-IDF · SQLite/PostgreSQL · HTML/CSS/Vanilla JS · Vercel · Render

---

## SECTION 1 — Project Introduction

**Q1. Tell me about your project.**

NexoraAI is an AI-powered support ticket management system. When a user describes their problem in plain English, the system automatically classifies it into a category (Technical, Billing, Account, General Inquiry, Fraud), assigns a priority (Critical, High, Medium, Low), and extracts key entities like emails, phone numbers, and error codes. The backend is built with Python Flask, the ML model uses TF-IDF + scikit-learn classifiers, and the frontend is plain HTML/CSS/JavaScript deployed on Vercel.

---

**Q2. Why did you build this project?**

Customer support teams manually categorize hundreds of tickets daily, which is slow and error-prone. I wanted to automate that using machine learning so agents can focus on solving problems instead of sorting them. It also gave me a chance to combine full-stack development with real ML deployment.

---

**Q3. What problem does NexoraAI solve?**

It eliminates manual ticket triage. Instead of a support agent reading each ticket and deciding the category and urgency, the AI does it instantly with a confidence score. This reduces response time and ensures consistent categorization.

---

**Q4. What is the overall architecture of the project?**

- Frontend (Vercel): HTML/CSS/JS pages — landing, login, signup, dashboard, create-ticket, history, profile, admin panel
- Backend (Render): Flask REST API with JWT authentication, SQLite/PostgreSQL database, ML prediction engine
- ML Layer: TF-IDF vectorizer + trained classifier (Logistic Regression / Linear SVM / Random Forest — best one selected automatically)
- Communication: Frontend calls backend via Fetch API using JWT tokens in Authorization headers

---

## SECTION 2 — Machine Learning & NLP

**Q5. Which ML algorithm did you use and why?**

I trained three models — Logistic Regression, Linear SVM, and Random Forest — and automatically selected the best one based on accuracy. In practice, Logistic Regression or Linear SVM wins because they handle high-dimensional sparse TF-IDF vectors well and are fast at inference time.

---

**Q6. What is TF-IDF and why did you use it?**

TF-IDF (Term Frequency–Inverse Document Frequency) converts text into numerical vectors. TF measures how often a word appears in a document; IDF penalizes words that appear in many documents (like "the", "is"). The result is a vector that highlights words unique and important to each ticket. I used it because it's fast, interpretable, and works well for short text classification without needing a GPU.

---

**Q7. Explain your text preprocessing pipeline.**

1. Lowercase the text
2. Replace `!` with "urgent" and `?` with "question" to preserve urgency signals
3. Remove special characters, keep only letters and spaces
4. Remove stopwords (the, a, is, was, etc.)
5. Extract domain keywords (billing_issue, account_issue, technical_issue, etc.) and append them to the text — this boosts classification accuracy
6. Feed the enhanced text into TF-IDF vectorizer with unigrams and bigrams (ngram_range=(1,2))

---

**Q8. How does entity extraction work?**

I use regex patterns to extract:
- Emails: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
- Phone numbers: `\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}...`
- Error codes: patterns like `ERR-500`, `error 404`, `code 123`
- URLs: `https?://[^\s<>...]+`
- Monetary amounts: `\$\d+` or `\d+ dollars`
- Dates: `12/31/2024`, `2024-12-31`, `January 1, 2024`

These are shown to the user in the AI analysis panel as chips.

---

**Q9. How does priority assignment work?**

It's rule-based on top of the ML category prediction:
- Keywords like "critical", "emergency", "outage", "data loss" → Critical
- Fraud category + "unauthorized/breach" → Critical
- Technical + error keywords → High
- Account + "locked/access denied" → High
- Billing + "charged/refund" → High
- General Inquiry → Low (unless urgent keywords present)
- Low confidence prediction → Medium (safe default)

---

**Q10. How did you train the model?**

1. Load CSV dataset (40,000+ customer support tickets)
2. Clean and preprocess text using spaCy (lemmatization, stopword removal)
3. 80/20 train-test split with stratification
4. TF-IDF vectorization with 5000 features, unigrams + bigrams
5. Train Logistic Regression, Linear SVM, Random Forest
6. Evaluate each on accuracy, precision, recall, F1
7. Save best model as `model.pkl` and vectorizer as `vectorizer.pkl` using joblib

---

**Q11. What accuracy did your model achieve?**

Around 90–94% accuracy on the test set. The exact number depends on the dataset. I track it in the admin dashboard under "AI Accuracy" which is set to 94% based on evaluation results.

---

**Q12. What is a confidence score and how do you calculate it?**

Confidence is how sure the model is about its prediction. For models with `predict_proba` (Logistic Regression), it's the max probability across all classes. For models with `decision_function` (SVM), I apply sigmoid: `1 / (1 + exp(-|decision_value|))`. I also boost confidence by 0.1 if the extracted domain keywords match the predicted category.

---

**Q13. What is the difference between your category classifier and priority predictor?**

The category classifier is a trained ML model (TF-IDF + classifier). The priority predictor is a rule-based function that takes the predicted category, confidence score, and description keywords as input. I chose rules for priority because priority depends on urgency signals that are easier to capture with explicit keyword matching than with a separate ML model.

---

**Q14. How would you improve the model?**

- Use BERT or sentence transformers for better semantic understanding
- Add active learning — collect corrections from users and retrain monthly
- Use ensemble methods combining multiple classifiers
- Add more training data from real support tickets
- Implement duplicate detection using cosine similarity between ticket embeddings

---

**Q15. What is overfitting and how did you prevent it?**

Overfitting is when a model memorizes training data and fails on new data. I prevented it by:
- Using 80/20 train-test split
- Stratified sampling to ensure balanced class distribution
- TF-IDF with max_features=5000 to limit feature space
- Evaluating on held-out test set before saving the model

---

## SECTION 3 — Backend & API

**Q16. Why did you choose Flask over Django or FastAPI?**

Flask is lightweight and gives full control over structure. For this project size, Django would be overkill. FastAPI would be faster but Flask has better ecosystem support for ML integration (Flask-JWT-Extended, Flask-SQLAlchemy). Flask was also familiar to me, which helped me move faster.

---

**Q17. Explain your API endpoint structure.**

```
POST /api/signup          — Register new user
POST /api/login           — Login, returns JWT token
POST /api/predict         — AI prediction (requires token)
POST /api/create-ticket   — Create ticket (requires token)
GET  /api/tickets         — Get user's tickets (requires token)
GET  /api/ticket/<id>     — Get single ticket (requires token)
PUT  /api/update-ticket   — Update ticket status (requires token)
GET  /api/analytics       — User analytics (requires token)
GET  /api/admin/tickets   — All tickets (admin only)
GET  /api/admin/users     — All users (admin only)
GET  /api/admin/advanced-analytics — Admin analytics (admin only)
```

---

**Q18. How does JWT authentication work in your project?**

1. User logs in with email + password
2. Backend verifies credentials, creates JWT token with `create_access_token(identity=user.id)`
3. Token returned to frontend, stored in `localStorage`
4. Every API request includes `Authorization: Bearer <token>` header
5. Backend uses `@token_required` decorator which calls `verify_jwt_in_request()` to validate
6. `get_jwt_identity()` extracts the user ID from the token

---

**Q19. What is the `token_required` decorator?**

It's a custom decorator that wraps Flask route functions. It calls `verify_jwt_in_request()` from Flask-JWT-Extended. If the token is missing or invalid, it returns a 401 error. If valid, the route function executes normally. Admin routes use `@admin_required` which additionally checks `user.role == 'admin'`.

---

**Q20. How do you handle CORS?**

Using Flask-CORS with `origins=["*"]` for development. In production, I restrict it to the Vercel frontend domain. CORS is needed because the frontend (Vercel, port 3000) and backend (Render, port 5000) are on different origins, and browsers block cross-origin requests by default.

---

**Q21. How do you handle errors in the API?**

- Try-except blocks in every route
- `db.session.rollback()` on database errors to prevent partial writes
- Specific HTTP status codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error)
- Global error handlers for 404 and 500 registered in `app.py`

---

**Q22. Explain the ticket creation flow end-to-end.**

1. User fills title + description on create-ticket page
2. Clicks "Analyze with AI" → `POST /api/predict` → ML model returns category, priority, confidence, entities
3. Results shown in AI panel with confidence bar and entity chips
4. User reviews and clicks "Confirm & Create" → `POST /api/create-ticket`
5. Backend validates fields, saves ticket to database with user_id from JWT
6. Returns ticket object with 201 status
7. Frontend redirects to history page

---

**Q23. How did you deploy the backend on Render?**

1. Pushed code to GitHub
2. Connected GitHub repo to Render
3. Set environment variables: `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`
4. Render runs `pip install -r requirements.txt` then `gunicorn app:app`
5. Auto-deploys on every git push to main branch
6. Health check endpoint at `/api/health` confirms the server is running

---

**Q24. What is gunicorn and why use it instead of Flask's dev server?**

Gunicorn is a production WSGI server. Flask's built-in server is single-threaded and not safe for production. Gunicorn handles multiple concurrent requests using worker processes, making it suitable for real traffic.

---

## SECTION 4 — Database

**Q25. Explain your database schema.**

Two main tables:

**users:** id (UUID), name, email (unique), mobile, password_hash, role (user/admin), avatar_url, is_active, created_at, last_login

**tickets:** id (UUID), user_id (FK → users), title, description, category, priority, status, ai_confidence, original_ai_category, assigned_to, created_at, resolved_at

Supporting tables: notification_settings, internal_notes, audit_logs, system_settings, admin_notifications

---

**Q26. Why UUID for primary keys instead of integers?**

UUIDs are globally unique, making them safe to generate on the client side without database coordination. They also prevent enumeration attacks (an attacker can't guess `ticket/1`, `ticket/2`). The tradeoff is slightly larger storage and slower index lookups, which is acceptable for this scale.

---

**Q27. Why SQLite for development and PostgreSQL for production?**

SQLite requires zero setup — it's a single file, perfect for local development. PostgreSQL handles concurrent connections, has better performance at scale, and is what Render provides. The switch is seamless because SQLAlchemy abstracts the database layer.

---

**Q28. What is SQLAlchemy and why use it?**

SQLAlchemy is a Python ORM (Object-Relational Mapper). It lets you define database tables as Python classes and write queries in Python instead of raw SQL. Benefits: prevents SQL injection automatically, works with any database, easier to read and maintain.

---

**Q29. How do you prevent SQL injection?**

SQLAlchemy uses parameterized queries internally. When I write `Ticket.query.filter_by(user_id=user_id)`, SQLAlchemy generates `SELECT * FROM tickets WHERE user_id = ?` with the value passed separately, never interpolated into the string. This makes SQL injection impossible.

---

**Q30. What is a database transaction and where do you use it?**

A transaction groups multiple database operations so they either all succeed or all fail. I use `db.session.add()` and `db.session.commit()` for writes, and `db.session.rollback()` in except blocks. For example, when creating a user, I also create their notification settings in the same transaction — if either fails, neither is saved.

---

## SECTION 5 — Frontend

**Q31. Why vanilla JavaScript instead of React or Vue?**

To demonstrate strong JavaScript fundamentals. Many developers rely on frameworks without understanding the DOM, event handling, or async programming. Building without a framework shows I understand the core language. It also keeps the project lightweight with no build step needed.

---

**Q32. How does the frontend communicate with the backend?**

Using the Fetch API with async/await. Every request goes through the `apiRequest()` function in `api.js` which:
1. Gets the JWT token from localStorage
2. Adds `Authorization: Bearer <token>` header
3. Makes the fetch call
4. Checks `response.ok` and throws on errors
5. Returns parsed JSON

---

**Q33. How do you handle authentication state on the frontend?**

`auth.js` provides utility functions:
- `isLoggedIn()` — checks if token exists in localStorage
- `getCurrentUser()` — parses stored user object
- `protectPage()` — redirects to login.html if not logged in
- `protectAdminPage()` — redirects if not admin
- `redirectIfLoggedIn()` — used on login/signup pages to skip if already logged in
- `logout()` — clears localStorage and redirects to login

---

**Q34. How did you make the website responsive?**

CSS media queries in `responsive.css`. Key breakpoints at 768px (tablet) and 480px (mobile). Used Flexbox and CSS Grid for layouts with relative units (%, rem). The navigation collapses on mobile and cards stack vertically.

---

**Q35. What is the glassmorphism design style you used?**

Glassmorphism uses semi-transparent backgrounds with backdrop blur to create a frosted glass effect. In CSS: `background: rgba(31, 31, 31, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1)`. Combined with gradient text and dark backgrounds, it gives a modern SaaS look.

---

## SECTION 6 — Security

**Q36. How do you store passwords securely?**

Using bcrypt hashing. `bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())` generates a salted hash. The salt is random for each password, so two users with the same password have different hashes. Verification uses `bcrypt.checkpw()` — the original password is never stored.

---

**Q37. What security measures did you implement?**

- bcrypt password hashing
- JWT tokens with 24-hour expiration
- Role-based access control (user vs admin)
- CORS restricted to known frontend domains
- Input validation on all API endpoints
- SQL injection prevention via SQLAlchemy ORM
- HTTPS enforced on both Vercel and Render

---

**Q38. What is role-based access control in your project?**

Users have a `role` field: either "user" or "admin". The `@token_required` decorator allows any authenticated user. The `@admin_required` decorator additionally checks `user.role == 'admin'` and returns 403 if not. On the frontend, `protectAdminPage()` redirects non-admins away from the admin dashboard.

---

## SECTION 7 — Deployment & DevOps

**Q39. Explain your deployment setup.**

- Frontend: Vercel — auto-deploys from GitHub on every push to main. Static files served via CDN globally.
- Backend: Render — auto-deploys from GitHub. Runs gunicorn. Free tier spins down after inactivity (cold start ~30 seconds).
- Database: SQLite file on Render's persistent disk (or PostgreSQL if DATABASE_URL is set)
- CI/CD: GitHub → Vercel/Render webhooks trigger automatic deployment

---

**Q40. What is `vercel.json` and what does it do?**

It configures Vercel deployment. In our case:
```json
{
  "outputDirectory": "frontend",
  "routes": [
    { "src": "/", "dest": "/landing.html" },
    { "src": "/(.*)", "dest": "/$1" }
  ]
}
```
It tells Vercel to serve files from the `frontend/` folder and route the root URL to `landing.html`.

---

**Q41. What is `render.yaml`?**

It's the infrastructure-as-code file for Render. It defines the service type (web), build command (`pip install -r requirements.txt`), start command (`gunicorn app:app`), and environment variables. Render reads this file to configure the deployment automatically.

---

## SECTION 8 — Scenario-Based

**Q42. The ML model gives wrong category. How do you handle it?**

Three layers of correction:
1. User can override the category using the dropdown in the AI panel before submitting
2. Admin can override the category from the admin dashboard (tracked in `original_ai_category` field)
3. Corrections are logged in audit logs and can be used to retrain the model

---

**Q43. Your backend is down. What does the user see?**

The frontend's `apiRequest()` catches the `Failed to fetch` network error and throws a user-friendly message: "Cannot connect to server. Please check if the backend is running." This is shown as a toast notification. The page doesn't crash.

---

**Q44. How would you scale this system for 100,000 users?**

- Replace SQLite with PostgreSQL with connection pooling
- Add Redis caching for frequent queries (analytics, ticket lists)
- Use Celery + Redis for async ML predictions (don't block the API)
- Deploy backend on multiple Render instances with a load balancer
- Use CDN for frontend assets (already done via Vercel)
- Add database indexes on user_id, category, status, created_at

---

**Q45. How would you add real-time notifications?**

Use WebSockets via Socket.IO. When a ticket status changes, the server emits an event to the user's socket connection. The frontend listens and shows a toast notification. Alternative: Server-Sent Events (SSE) for one-way server-to-client updates, which is simpler to implement.

---

## SECTION 9 — HR & Behavioral

**Q46. What was the biggest challenge you faced?**

The ML model initially had 70% accuracy. I improved it by adding domain keyword extraction — appending keywords like "billing_issue" or "technical_issue" to the text before vectorization. This gave the model stronger signals and pushed accuracy to 90%+. It taught me that feature engineering matters more than algorithm choice.

---

**Q47. What did you learn from this project?**

Technical: ML pipeline deployment, JWT auth, REST API design, database schema design, CI/CD with GitHub.
Soft skills: Debugging production issues (Render DB connection failure), time management across 12 sprints, writing documentation.

---

**Q48. What would you do differently?**

- Use FastAPI instead of Flask for automatic OpenAPI docs and better async support
- Add unit tests from the start (currently no automated tests)
- Use Docker for consistent environments across development and production
- Implement proper logging with structured logs instead of print statements

---

**Q49. How did you manage the project?**

Agile methodology with 2-week sprints. Maintained a Product Backlog with 25 user stories, Sprint Backlog for each sprint, and Daily Standup tracking. Used GitHub for version control with meaningful commit messages. Deployed continuously — every push to main auto-deploys to Vercel and Render.

---

## SECTION 10 — Tricky Questions

**Q50. Your model has 94% accuracy. What about the 6% wrong predictions?**

The 6% is handled by: (1) showing confidence scores — low confidence predictions are flagged visually, (2) allowing users to override category/priority before submitting, (3) admin can correct tickets after creation, (4) corrections are logged for future retraining. No ML system is 100% accurate, so human oversight is built into the workflow.

---

**Q51. Why not use ChatGPT/GPT-4 for classification instead of training your own model?**

GPT-4 would work but: (1) it costs money per API call, (2) it's slower (network latency), (3) it sends user data to a third party (privacy concern), (4) it's a black box — you can't explain why it made a decision. My TF-IDF model is free, fast (<100ms), runs locally, and is interpretable.

---

**Q52. What happens if someone submits a ticket with just "help"?**

The model will predict with low confidence (around 50%). The priority assignment defaults to "medium" for low-confidence predictions. The confidence bar will show red/orange. The user sees the low confidence score and is encouraged to add more detail. The system still creates the ticket — it doesn't block submission.

---

**Q53. How do you know your model isn't biased toward certain categories?**

I check the confusion matrix and per-class F1 scores in the classification report. If one category has significantly lower recall, it means the model is biased against it. I'd fix this by collecting more training data for that category or using class weights in the classifier (`class_weight='balanced'`).

---

**Q54. Can a regular user access the admin panel?**

No. The admin dashboard has `protectAdminPage()` on the frontend which redirects non-admins to `dashboard.html`. On the backend, all `/api/admin/*` routes use `@admin_required` which checks `user.role == 'admin'` and returns 403 if not. Both layers must be bypassed — which requires a valid admin JWT token.

---

**Q55. What if two users submit the same ticket simultaneously?**

Each ticket gets a unique UUID generated by Python's `uuid.uuid4()`. Database transactions ensure each insert is atomic. SQLAlchemy's session management handles concurrent writes safely. There's no race condition because each ticket is independent — they don't share a counter or sequence that could conflict.

---

*Good luck with your interview! Know your code, be honest about limitations, and show enthusiasm for what you built.*

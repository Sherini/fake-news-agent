# Fake News Detection Agent

This project wraps the already-trained Logistic Regression and Decision Tree models in a Python Flask prediction API, then uses a Java Spring Boot (Maven) service as an agent/API gateway. A simple web UI is served by Spring Boot. Selenium provides a browser smoke test; GitHub Actions builds Java and checks Python syntax; Docker Compose starts both services.

## What was reused

- `ai-service/models/model.pkl`
- `ai-service/models/dt_model.pkl`
- `ai-service/models/vectorizer.pkl`
- `ai-service/models/x_train_text.pkl` (needed for the existing SHAP explanation code)
- `utils.py`, `url_utils.py`, `xai.py`, and training scripts/dataset

The models are loaded from the existing pickle files; this project does not retrain them.

## Run locally on Windows

### 1. Start Python AI service

PowerShell terminal 1:

```powershell
cd ai-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Check `http://localhost:5000/health`. The first run may download NLTK stopwords. If you see a `newspaper` or `lxml_html_clean` import error, install dependencies from `requirements.txt` again.

### 2. Start Maven / Spring Boot agent

PowerShell terminal 2, from the repository root:

```powershell
cd spring-agent
mvn spring-boot:run
```

Open `http://localhost:8081`.

### 3. Test API directly

```powershell
Invoke-RestMethod -Uri "http://localhost:8081/api/predict" -Method POST -ContentType "application/json" -Body '{"text":"Paste a sample news article here.","model":"ml","explain":false}'
```

Use `model` values `ml`, `dt`, or `dl`. The uploaded files did not include `models/distilbert_fake_news/`; therefore `dl` stays unavailable until you copy that complete saved directory into `ai-service/models/distilbert_fake_news/` and install compatible `transformers` and `torch` packages. ML and DT use the supplied pickle models.

### 4. Docker

From the repository root:

```powershell
docker compose up --build
```

Open `http://localhost:8081`. First build can take a while because Python scientific and explainability dependencies are substantial.

### 5. Selenium

Install Selenium and Chrome/ChromeDriver on your machine, start both services, then run from repository root:

```powershell
pip install selenium
python -m unittest discover -s selenium-tests -v
```

### 6. GitHub

```powershell
git init
git add .
git commit -m "Add fake news detection agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fake-news-agent.git
git push -u origin main
```

Create the empty repository on GitHub first and replace the URL with your repository URL.

## Agent workflow

1. Accept text or article URL.
2. Validate input and model choice.
3. Extract article text from URL when provided.
4. Invoke the selected existing classifier.
5. Return prediction and model confidence; include SHAP/LIME output when available for Logistic Regression.
6. Display a disclaimer that model predictions are not independent fact verification.

## Important notes

- Treat predictions as model assessments, not guaranteed truth. Confidence is model probability, not necessarily calibrated real-world accuracy.
- The current `utils.py` downloads NLTK stopwords at import time. For offline environments, preinstall the corpus or adjust this utility.
- The original Flask website used plaintext passwords. This scaffold does not port its registration/login screens or plaintext credential storage; do not expose the old login code publicly without adding password hashing and secure session settings.
- `xai.py` can be memory-intensive. If explanation generation fails, the prediction endpoint still returns the model prediction and logs the explanation error.

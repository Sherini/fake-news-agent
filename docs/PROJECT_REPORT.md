# Project Report: Fake News Detection Agent

## Objective
Integrate existing trained fake-news classifiers into a maintainable application with a Java/Maven API layer, Python inference service, browser automation tests, GitHub CI, and Docker packaging.

## Existing model assets
The project reuses a saved Logistic Regression classifier, a saved Decision Tree classifier, and their TF-IDF vectorizer. The existing DistilBERT inference module is retained conceptually, but its model-weight directory was not part of the uploaded files. No model retraining is performed by the application.

## Architecture
- Frontend: HTML, CSS, JavaScript served by Spring Boot.
- Agent/API gateway: Java 17+, Spring Boot, Maven.
- Inference service: Python Flask and scikit-learn.
- Explainability: SHAP and LIME for the Logistic Regression model when dependencies and runtime resources permit.
- URL extraction: newspaper3k.
- Tests: Selenium browser smoke test and GitHub Actions build checks.
- Deployment: Docker Compose.

## Workflow
The user submits article text or a URL and chooses a model. Spring Boot forwards the request to Flask. Flask validates the request, extracts article text if needed, preprocesses it using the existing utility, runs the selected model, and returns a prediction, confidence score, and optional explanations. The browser renders the response and disclaimer.

## Limitations
The classifier may be wrong, may be sensitive to the dataset and distribution shifts, and is not a replacement for independent source verification. Confidence is not automatically calibrated. URL extraction can fail for paywalled or dynamically rendered sites. DistilBERT is disabled until its saved weights are supplied. The original account system is not included in this scaffold; production use would require authentication, authorization, secure secret management, and password hashing.

## Test plan
1. Check Flask `/health`.
2. Submit text to `/api/predict` using `ml` and `dt`.
3. Verify invalid/empty input is rejected.
4. Submit a URL and verify extraction failure is handled.
5. Open the frontend and run Selenium smoke tests.
6. Run Maven tests and GitHub Actions.
7. Build and run both services using Docker Compose.

# AI Presales Agent

This project is a Dockerized AI Presales Agent application. Follow the steps below to update your system, upgrade pip, install requirements, and run the APIs.

---

## 1. Update & Upgrade the System

Before installing any dependencies, make sure your system is up-to-date.

### For Debian/Ubuntu-based Systems

```bash
sudo apt update && sudo apt upgrade -y
```

### For Other Systems

Please refer to your operating system's documentation on how to update and upgrade your system packages.

---

## 2. Optional: Create and Activate a Virtual Environment

It's recommended to use a virtual environment to isolate your project's dependencies.

1. **Create the Virtual Environment**

   If you haven't created one already, run:

   ```bash
   python -m venv /workspaces/python-ai_presale_agent/venv
   ```

2. **Activate the Virtual Environment**

   On Unix-based systems (Linux, macOS):

   ```bash
   source /workspaces/python-ai_presale_agent/venv/bin/activate
   ```

   On Windows, use:

   ```bash
   /workspaces/python-ai_presale_agent/venv/Scripts/activate
   ```

---

## 3. Upgrade pip

Ensure that you have the latest version of pip installed. Run the following command:

```bash
python -m pip install --upgrade pip
```

---

## 4. Install Python Requirements

Install all required Python packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 5. APIs

Once all dependencies are installed and your app is running, the API endpoints will be available. We're using [FastAPI](https://fastapi.tiangolo.com/), you can access the interactive API documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

These endpoints let you explore and test the API directly from your browser.

---

## 6. Running the Application

If you're running the app locally (without Docker), you can start the server with:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Your API should now be accessible at [http://localhost:8000](http://localhost:8000).

---

## 7. Docker Deployment

If you prefer to use Docker, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker build -t ai_presales_agent .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 ai_presales_agent
   ```

This will make your application available on your local machine at port 8000.

---

## 8. Heroku Deployment via GitHub

To deploy your app to Heroku using GitHub:

1. **Push Your Code to GitHub:**  
   Ensure your repository (including the `Dockerfile` and `heroku.yml`) is pushed to GitHub.

2. **Add a `heroku.yml` File:**  
   Create a file named `heroku.yml` at the root of your repository with the following content:

   ```yaml
   build:
     docker:
       web: Dockerfile
   ```

3. **Connect Your GitHub Repo to Heroku:**  
   - Log into the [Heroku Dashboard](https://dashboard.heroku.com/).  
   - Select your app (**presales-agent**).  
   - Go to the **Deploy** tab and choose GitHub as your deployment method.  
   - Connect your GitHub account and select your repository.

4. **Deploy Your App:**  
   Select the branch you wish to deploy (typically `main`), then click **Deploy Branch**.  
   Heroku will build your Docker image using your `heroku.yml` and deploy your app.

5. **Enable Automatic Deployments (Optional):**  
   You can enable automatic deployments so that every push to the selected branch triggers a new deployment.
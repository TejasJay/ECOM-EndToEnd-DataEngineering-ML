
# 🛍️ ECOM Data Sources Microservice

This microservice generates and streams realistic e-commerce simulation data (POS logs, promotions, user activity, etc.) for downstream analytics pipelines via **batch files** or **real-time Kafka streams**.

It is containerized using **Docker**, automated with **Makefile**, orchestrated with **GitHub Actions**, and intended to be run standalone or integrated into larger ML pipelines

---

## 🌟 Features

- 🧠 Generates synthetic e-commerce user, session, behavior, and order data.
- 🐍 Python-based with asynchronous real-time simulation.
- 🐳 Dockerized for portability and reproducibility.
- 🔁 CI/CD pipeline via GitHub Actions to auto-build & push Docker image.
- 🧪 Smart bootstrapping logic using `start_simulation.sh`:
  - Batch generation if data doesn’t exist.
  - Promotion fetcher auto-start.
  - Realtime simulator launch.
---

## 🧱 Project Structure

```bash
📦 ECOM_PRJ
 ┣━━ 📂 others
 ┣━━ ⚙️ .gitattributes
 ┣━━ ⚙️ .gitignore
 ┣━━ 📝 README.md
 ┣━━ 📂 ecom_data_sources
 ┃   ┣━━ 📂 external_apis
 ┃   ┃   ┣━━ 📝 __init__.py
 ┃   ┃   ┣━━ 📝 promotion_external_api_colab.py
 ┃   ┃   ┗━━ 📝 promotion_fetch_api_request.py
 ┃   ┣━━ 📂 inventory
 ┃   ┃   ┗━━ 📄 product_catalog.csv
 ┃   ┣━━ 📂 json_files
 ┃   ┃   ┗━━ 📝 full_data.json
 ┃   ┣━━ 📂 logs/session_logs
 ┃   ┣━━ 📂 pos_logs
 ┃   ┃   ┣━━ 📂 __pycache__
 ┃   ┃   ┣━━ 📝 __init__.py
 ┃   ┃   ┗━━ 📝 unified_simulator.py
 ┃   ┣━━ 📂 simulation_scripts
 ┃   ┃   ┣━━ 📂 __pycache__
 ┃   ┃   ┣━━ 📝 __init__.py
 ┃   ┃   ┣━━ 📝 behaviour.py
 ┃   ┃   ┣━━ 📝 historic_simulator.py
 ┃   ┃   ┣━━ 📝 match_persona_to_behaviour.py
 ┃   ┃   ┣━━ �� realtime_simulator.py
 ┃   ┃   ┗━━ 📝 simulator_logic.py
 ┃   ┣━━ 📂 user_activity
 ┃   ┃   ┗━━ 📝 __init__.py
 ┃   ┣━━ 📄 .env.secrets
 ┃   ┣━━ 📄 Dockerfile
 ┃   ┣━━ 📄 Makefile
 ┃   ┣━━ 📄 requirements.txt
 ┃   ┗━━ 📄 start_simulation.sh
````

* * *

## ⚙️ Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop)
-   [Make](https://www.gnu.org/software/make/)
-   Python 3.11+ (for local testing)
-   DockerHub account (if pushing to registry)
-   GitHub account (for workflow triggers)
* * *

## 🧪 Running the Microservice Locally

```bash
# Clone the repo
git clone https://github.com/TejasJay/ECOM_EndToEnd_DataEngineering_ML.git
cd ECOM_PRJ/ecom_data_sources

# Login to DockerHub (reads from .env.secrets)
make login

# Build the Docker image
make build

# Run the service (triggers start_simulation.sh inside container)
make run
```

* * *

## 🔐 .env.secrets

Create `ecom_data_sources/.env.secrets` with your DockerHub credentials:

```env
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_PASSWORD=your_dockerhub_password
```

This allows `make login` and `make push` to work securely.

* * *

## 🚀 GitHub Actions (CI/CD)

When you `git push` to the `main` branch, this workflow triggers:

```
.github/workflows/build_simulator.yml
```

It automatically:

1.  Builds the Docker image inside GitHub runner.
2.  Logs in to DockerHub using repository secrets.
3.  Pushes the image to `docker.io/<username>/ecom_data_sources:latest`.

> 🔐 Make sure to store DockerHub credentials as GitHub repository secrets:

-   `DOCKERHUB_USERNAME`
-   `DOCKERHUB_TOKEN`
* * *

## 📜 What `start_simulation.sh` Does

```bash
1. Checks if `json_files/full_data.json` exists:
   - If not, runs unified simulator in batch mode to generate it.
2. Checks if `promotion_fetch_api_request.py` is already running:
   - If not, starts it in the background.
3. Launches the unified simulator in real-time mode.
```

* * *

## 🛠 Makefile Shortcuts

```bash
make build          # Build Docker image
make run            # Run container (runs start_simulation.sh inside)
make login          # DockerHub login
make push           # Push image to DockerHub
make test           # Run batch simulator locally
make check-secrets  # Verify .env.secrets exists
```

* * *

## 📦 Output Data

-   `json_files/full_data.json`: Batch simulated data.
-   `logs/session_logs/core*.log`: Real-time behavior logs.
-   `promotion.log`: Output of background API fetcher.
* * *

## 💡 Future Enhancements

-   Kafka support for real-time stream publishing
-   Visualization dashboard (e.g. Grafana/Kibana)
-   Dataset metrics validation
-   Integration with Airflow or ML pipeline
* * *

## 🧠 Summary

This microservice simulates user and purchase data for e-commerce use cases and is structured to scale via containerization and automation. It can be extended into a full end-to-end AI pipeline for fraud detection, personalization, and forecasting.

* * *

### 📬 Contact

Feel free to open issues or contribute via PRs if you’d like to improve this microservice!




# DevOps Task Tracker

Simple multi-container app (Flask web + PostgreSQL) with a GitHub Actions CI/CD pipeline.

## Run locally
```bash
cp .env.example .env
docker compose up --build
# open http://localhost:5000
```

## Run tests
```bash
pip install -r requirements-dev.txt
pytest -v
```

## CI/CD (GitHub Actions)
commit/push -> Build & Test -> Docker build & push (GHCR) -> Deploy with Docker Compose + smoke test

## Deploy on AWS EC2
1. Launch Ubuntu EC2 instance, open ports 22 and 5000 in the Security Group.
2. Install Docker: `curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker $USER`
3. `git clone <repo-url> ~/devops-task-tracker && cd ~/devops-task-tracker && cp .env.example .env`
4. `docker compose up -d --build` then open `http://<EC2-PUBLIC-IP>:5000`
5. For automatic deployment add repo secrets `EC2_HOST`, `EC2_USER` (ubuntu), `EC2_SSH_KEY` (private key contents).
AWS EC2 deployment test completed.

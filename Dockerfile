# Define python_version argument
ARG PYTHON_VERSION=3.11

# Define base image
FROM python:${PYTHON_VERSION}-slim AS python-base

# Install necessary OS dependencies
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    apt update && apt upgrade -y && apt-get install -y gcc curl git


ADD . /project

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /project

RUN pip install .

RUN pip install -r requirements.txt

EXPOSE 8000


CMD ["uvicorn", "--app-dir", "./src", "baker.app:app", "--host", "0.0.0.0", "--port", "8000"]
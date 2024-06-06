# Base image
FROM python:3.9

# Set the app home directory
ARG APP_HOME=/usr/src/app

# Create app user
RUN groupadd -r app && useradd -d /usr/src/app --no-log-init -r -g app app

# Create app directory and set ownership
RUN mkdir -p $APP_HOME
RUN chown -R app:app $APP_HOME

# Set working directory
WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONUNBUFFERED=True PYTHONPATH=$APP_HOME

# Install dependencies
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy application code
COPY . $APP_HOME/

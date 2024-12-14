FROM nvidia/cuda:12.0.0-base-ubuntu22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y

RUN apt-get install -y python3.9 \
    python3-pip

RUN pip install poetry==1.8.5

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY . /app

# Expose port
EXPOSE 50001

# Run the application
CMD ["poetry", "run", "python", "./app.py"]
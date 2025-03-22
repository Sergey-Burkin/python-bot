FROM python:3.10-alpine

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./src .

# Create a directory for downloaded images
RUN mkdir -p ./data

# Run the bot
CMD ["python", "main.py"] 
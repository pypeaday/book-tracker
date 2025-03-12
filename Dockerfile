FROM python:3.11-slim

# Set environment variables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Create data directory for SQLite database
RUN mkdir /app/data

# Create a non-root user and set permissions
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod 755 /app/data


USER appuser

# Create and activate virtual environment
RUN uv venv $VIRTUAL_ENV

# Copy the rest of the application
COPY . .

# Install dependencies using uv in the virtual environment
RUN uv sync

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

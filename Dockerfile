FROM python:3.10-slim

# Install SQL Server ODBC Driver dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Set workdir and install requirements
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "backend/app.py"]

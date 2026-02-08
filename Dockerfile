FROM python:3.11-slim

# 1. Install system dependencies & mongodump
RUN apt-get update && apt-get install -y wget tar && \
    wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-100.9.4.tgz && \
    tar -zxvf mongodb-database-tools-debian11-x86_64-100.9.4.tgz && \
    cp mongodb-database-tools-debian11-x86_64-100.9.4/bin/mongodump /usr/local/bin/mongodump && \
    rm -rf mongodb-database-tools-debian11-x86_64-100.9.4* && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .

# 2. Install Python requirements 
# We use --user-dir or ensure the path is added
RUN pip install --no-cache-dir -r requirements.txt

# 3. Explicitly call the python module to avoid PATH issues
ENTRYPOINT ["python", "-m", "functions_framework", "--target=entrypoint"]
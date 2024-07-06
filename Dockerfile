# 
FROM python:3.11-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install Alembic
RUN pip install alembic

RUN pip install python-multipart

# 
COPY ./app /code/app

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entry point for the action
ENTRYPOINT ["/entrypoint.sh"]
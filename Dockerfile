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

# 
COPY ./app /code/app

#
EXPOSE 80

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
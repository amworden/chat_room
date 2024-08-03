# Use the official Python base image
FROM python:latest

# Set the working directory in the container
WORKDIR /code/app

COPY . /code

ENV PYTHONPATH=/code

# Install the required dependencies
RUN pip install --no-cache-dir -r requirments.txt

CMD "tail -f /dev/null"
# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /root

COPY . .

RUN pip install -r /root/requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/root

# Define environment variable for the port
ENV PORT=8000
ENV ENV_FOR_DYNACONF=dev-compose

ENV PYTHONUNBUFFERED=1

# Make the port available to the world outside this container
EXPOSE ${PORT}

# Run the application
CMD ["python", "./app/main.py"]
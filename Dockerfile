# Use the official Python base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the main.py file to the working directory
COPY main.py .

#pip install fastapi and uvicorn
RUN pip install fastapi
RUN pip install uvicorn

# Expose port 7995
EXPOSE 7995

# Run the main.py file
CMD ["python", "main.py"]


#q: how to run dockerfile
#A: docker build -t myimage .
#   docker run -p 7995:7995 myimage
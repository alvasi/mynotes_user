FROM python:3.11-slim
ENV PORT 5000
EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]

# # Use an official Python runtime as a parent image
# FROM python:3.8-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY requirements.txt /app

# # # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# COPY app.py /app

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Define environment variable
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Run app.py when the container launches
# CMD ["flask", "run"]
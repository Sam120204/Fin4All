# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app/
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . .

# Make port 8000 available to the world outside this container
ENV PORT 8000
EXPOSE 8000

# Run app.py when the container launches
CMD exec gunicorn Fin4All.wsgi:application --bind :$PORT --workers 1 --threads 8
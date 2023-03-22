FROM python:3.9.13

# Set the working directory
WORKDIR /TSIGNAL

# Copy the required files
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 80

# Run the application
CMD ["/bin/sh", "-c", "cd app && python app.py"]
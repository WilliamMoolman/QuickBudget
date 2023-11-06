FROM python:3.12

# Install deps
RUN pip install flask pymongo python-dotenv pandas mongoengine

# Copy the app
COPY . /app

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 5000

# Run the app
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
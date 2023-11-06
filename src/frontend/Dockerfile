# Build streamlit app with python 3.12
FROM python:3.12

# Install streamlit and st_pages
RUN pip install streamlit st_pages

# Copy the app
COPY . /app

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py"]

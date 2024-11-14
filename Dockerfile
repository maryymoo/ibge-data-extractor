# Use a imagem oficial do Python 3.9
FROM python:3.9-slim

# Define the working directory within the container
WORKDIR /app

# Copy the files from your project to the container
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o script
CMD ["python", "src/main.py"]


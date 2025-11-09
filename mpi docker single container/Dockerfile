# Use a standard Python base image
FROM python:3.10-slim

# Install the MPICH library from the package manager
RUN apt-get update && apt-get install -y mpich && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your MPI Python script into the container
COPY pipeline_mpi.py .

# Set the default command to run when the container starts.
# This single command will start all 5 processes inside this one container.
CMD ["mpiexec", "-np", "5", "python", "/app/pipeline_mpi.py"]

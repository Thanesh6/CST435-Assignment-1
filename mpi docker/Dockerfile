FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    openssh-server openssh-client \
    mpich sshpass python3-pip && apt-get clean

WORKDIR /app

# Copy files
COPY pipeline_mpi.py .
COPY start_master.sh /start_master.sh
COPY start_worker.sh /start_worker.sh

RUN pip install numpy mpi4py

# SSH setup
RUN mkdir -p /var/run/sshd && \
    echo "root:root" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd && \
    chmod +x /start_master.sh /start_worker.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

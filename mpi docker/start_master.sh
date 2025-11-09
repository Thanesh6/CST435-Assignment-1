#!/bin/bash
service ssh start
echo "🔧 Waiting for workers to start SSH..."
sleep 5

echo "🔑 Generating SSH keys..."
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Create hostfile
echo "mpi_master" > /app/hosts
for i in 1 2 3 4; do
    echo "mpi_worker$i" >> /app/hosts
done

# Copy SSH keys to workers
echo "🚀 Copying keys to workers..."
for i in 1 2 3 4; do
    sshpass -p root ssh-copy-id -o StrictHostKeyChecking=no root@mpi_worker$i
done

echo "📜 Hostfile ready:"
cat /app/hosts

# Run MPI Job
echo "🧠 Running MPI job..."
START=$(date +%s)
mpiexec -np 5 -hostfile /app/hosts python /app/pipeline_mpi.py
END=$(date +%s)
echo "✅ MPI job complete in $(($END - $START)) seconds"

# Keep container alive for logs
tail -f /dev/null

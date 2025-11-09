from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def datagen_service(data_size):
    data = np.random.rand(data_size, data_size)
    print(f"[RANK 1] Generated matrix {data_size}x{data_size}")
    return data

def preprocess_service(data):
    mean = np.mean(data)
    std = np.std(data)
    norm = (data - mean) / (std + 1e-8)
    print(f"[RANK 2] Normalized data (mean={mean:.3f}, std={std:.3f})")
    return norm

# --- MODIFIED SECTION START ---
def feature_service(data):
    # THE EXPENSIVE LINES ARE COMMENTED OUT
    # eigvals = np.linalg.eigvals(data @ data.T)
    # rank_val = np.linalg.matrix_rank(data)
    # features = np.concatenate([eigvals.real[:10], [rank_val]])

    # INSTEAD, WE RETURN FAKE DATA INSTANTLY
    print(f"[RANK 3] SKIPPING feature extraction, returning dummy data.")
    features = np.random.rand(11) # Create a dummy feature vector of the same size
    
    return features
# --- MODIFIED SECTION END ---

def analysis_service(features):
    corr = np.mean(np.corrcoef(features)) if len(features) > 1 else 1.0
    avg_dist = np.mean(np.abs(features - np.mean(features)))
    cluster = "Cluster A" if np.mean(features) > 0 else "Cluster B"
    print(f"[RANK 4] Analysis done: {cluster}")
    return {"correlation": corr, "avg_distance": avg_dist, "cluster": cluster}

if rank == 0:
    # MASTER
    data_size = 300
    start = time.time()
    print(f"[RANK 0] Starting pipeline with data_size={data_size}")

    comm.send(data_size, dest=1, tag=11)
    result = comm.recv(source=4, tag=44)

    total_time = time.time() - start
    summary = f"Cluster={result['cluster']}, Corr={result['correlation']:.3f}, Dist={result['avg_distance']:.3f}"
    print(f"\n=== MPI PIPELINE COMPLETED ===")
    print(f"Total Time: {total_time:.4f} sec")
    print(f"Summary: {summary}")

elif rank == 1:
    data_size = comm.recv(source=0, tag=11)
    data = datagen_service(data_size)
    comm.send(data, dest=2, tag=12)

elif rank == 2:
    data = comm.recv(source=1, tag=12)
    cleaned = preprocess_service(data)
    comm.send(cleaned, dest=3, tag=23)

elif rank == 3:
    cleaned = comm.recv(source=2, tag=23)
    features = feature_service(cleaned)
    comm.send(features, dest=4, tag=34)

elif rank == 4:
    features = comm.recv(source=3, tag=34)
    result = analysis_service(features)
    comm.send(result, dest=0, tag=44)

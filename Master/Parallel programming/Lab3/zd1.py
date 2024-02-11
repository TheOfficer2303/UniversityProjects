import sys

import pyopencl as cl
import numpy as np
from time import time

def get_test_data():
  X = np.random.rand(N).astype(np.float32)
  Y = np.random.rand(N).astype(np.float32)
  distances = np.zeros(N, dtype=np.float32)
  
  return X, Y, distances

def setup_CL(X, Y, distances):
  ctx = cl.create_some_context()
  queue = cl.CommandQueue(ctx)

  mf = cl.mem_flags
  X_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=X)
  Y_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=Y)
  distances_buf = cl.Buffer(ctx, mf.WRITE_ONLY, distances.nbytes)

  return ctx, queue, mf, X_buf, Y_buf, distances_buf

def get_distances(N, M):
    X, Y, distances = get_test_data()
    ctx, queue, mf, X_buf, Y_buf, distances_buf = setup_CL(X, Y, distances)

    prg = cl.Program(ctx, """
    __kernel void get_distances(const int N, const __global float* X, const __global float* Y, __global float* distances) {
        int gid = get_global_id(0);
        int size = get_global_size(0);
        int num_iterations = (N + size - 1) / size;

        for (int iter = 0; iter < num_iterations; iter++) {
            int i = gid + iter * size;
            if (i < N) {
                float sum = 0.0f;
                float xi = X[i];
                float yi = Y[i];

                for (int j = 0; j < N; j++) {
                    float dx = xi - X[j];
                    float dy = yi - Y[j];
                    sum += sqrt(dx*dx + dy*dy);
                }

                distances[i] = sum / (N - 1);
            }
        }
    }
    """).build()

    global_size = (N // M, )
    local_size = None
    start = time()
    prg.get_distances(queue, global_size, local_size, np.int32(N), X_buf, Y_buf, distances_buf)
    cl.enqueue_copy(queue, distances, distances_buf)
    print("Elapsed Time: ", time() - start)

    return distances

if __name__ == "__main__":
  N = int(sys.argv[1])
  M = int(sys.argv[2])

  avg_distance = np.mean(get_distances(N, M))
  print(f"Average distance: {avg_distance}")

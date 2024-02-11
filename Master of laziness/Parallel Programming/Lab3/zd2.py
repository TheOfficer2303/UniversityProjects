import time

import pyopencl as cl
import numpy as np
import sys

def calculate_pi_sequentially(n):
  h = 1.0 / float(n)
  total_sum = 0.0

  for i in range(n):
      x = h * (i + 0.5)
      total_sum += 4.0 / (1.0 + x*x)

  return h * total_sum

def setup_CL():
  ctx = cl.create_some_context()
  queue = cl.CommandQueue(ctx)

  mf = cl.mem_flags

  return ctx, queue, mf

def calculate_pi_parallely(n, m, l):
    h = 1.0 / n
    work_groups = int(n / m)
    ctx, queue, mf = setup_CL()
    mf = cl.mem_flags

    sums = np.zeros(work_groups, dtype=np.float64)
    
    sums_buffer = cl.Buffer(ctx, mf.WRITE_ONLY, sums.nbytes)

    program = cl.Program(ctx, """
    __kernel void calculate_pi_parallely(__global double* sums, const double h, const int n, const int m)
    {
        int id = get_global_id(0);
        int start = id * m + 1;
        int end = min(start + m, n + 1);
        double x, sum = 0.0;

        for(int i = start; i < end; i++)
        {
            x = h * ((double)i - 0.5);
            sum += 4.0 / (1.0 + x*x);
        }
        sums[id] = sum;
    }
    """).build()

    time_start = time.time()

    program.calculate_pi_parallely(queue, (work_groups,), (l,), sums_buffer, np.float64(h), np.int32(n), np.int32(m))
    cl.enqueue_copy(queue, sums, sums_buffer).wait()

    duration = time.time() - time_start

    return h * np.sum(sums), duration


if __name__ == "__main__":
    print("Usage: python zd2.py N M L")

    N = int(sys.argv[1])
    M = int(sys.argv[2])
    L = int(sys.argv[3])

    # time_start = time.time()
    # pi = calculate_pi_sequentially(N)
    # print("SEQUENTIAL")
    # print(f"Calculated value of Pi: {pi}")
    # print(f"Elapsed time sequenital: {time.time() - time_start}s")

    pi, duration = calculate_pi_parallely(N, M, L) 
    print("PARALLEL")
    print(f"Calculated value of Pi: {pi}")
    print(f"Elapsed time: {duration}s")

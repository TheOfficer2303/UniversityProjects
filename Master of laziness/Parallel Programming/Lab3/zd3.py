import time
import numpy as np
import pyopencl as cl

kernel_code = """
__kernel void jacobi_step(__global double* psi_temp, __global const double* psi, const int m, const int n) {
    int i = get_global_id(0) + 1;
    int j = get_global_id(1) + 1;
    
    if (i <= m && j <= n) {
        psi_temp[i * (m + 2) + j] = 0.25f * (
                    psi[(i - 1) * (m + 2) + j] + psi[(i + 1) * (m + 2) + j] + psi[i * (m + 2) + j - 1] + psi[i * (m + 2) + j + 1]);
    }
}

 __kernel void boundary_psi(__global double *psi, int m, int n, int b, int h, int w)
{    
    int i,j;
    for (i=b+1;i<=b+w-1;i++)
    {
        psi[i*(m+2)+0] = (double)(i-b);
    }
    for (i=b+w;i<=m;i++)
    {
        psi[i*(m+2)+0] = (double)(w);
    }
    for (j=1; j <= h; j++)
    {
        psi[(m+1)*(m+2)+j] = (double) w;
    }
    for (j=h+1;j<=h+w-1; j++)
    {
        psi[(m+1)*(m+2)+j]=(double)(w-j+h);
    }
}

__kernel void array_copy(__global const double *psi_temp, __global double *psi, const int m, const int n)
{
    int i = get_global_id(0) + 1;
    int j = get_global_id(1) + 1;
    psi[i * (m + 2) + j] = psi_temp[i * (m + 2) + j];
}
"""

def boundary_psi(psi: np.ndarray, m, n, b, h, w):
    for i in range(b + 1, b + w):
        psi[i * (m + 2) + 0] = (i - b)

    for i in range(b + w, m + 1):
        psi[i * (m + 2) + 0] = w

    for i in range(1, h + 1):
        psi[(m + 1) * (m + 2) + i] = w

    for i in range(h + 1, h + w):
        psi[(m + 1) * (m + 2) + i] = w - i + h

def delta_sq(new_list, old_list, m, n):
    d_sq = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            temp = new_list[i * (m + 2) + j] - old_list[i * (m + 2) + j]
            d_sq += temp * temp

    return d_sq


def setup_CL():
  ctx = cl.create_some_context()
  queue = cl.CommandQueue(ctx)

  return ctx, queue


def setup_kernel(ctx, psi, psi_temp):
  program = cl.Program(ctx, kernel_code).build()

  kernel_jacobi_step = program.jacobi_step
  kernel_array_copy = program.array_copy
  kernel_boundary_psi = program.boundary_psi

  psi_temp_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, size=psi_temp.nbytes)
  psi_buffer = cl.Buffer(ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=psi)

  return kernel_jacobi_step, kernel_array_copy, kernel_boundary_psi, psi_temp_buffer, psi_buffer


def main():
  tolerance = 0.0
  scale_factor = 64
  iterations = 1000
  irroational = 1
  checkerr, err = 0, 0

  if not checkerr:
    print(f"Scale Factor = {scale_factor}, iterations = {iterations}")
  
  b_base, h_base, w_base, m_base, n_base = 10, 15, 5, 32, 32
  b, h, w, m, n = (x * scale_factor for x in (b_base, h_base, w_base, m_base, n_base))

  psi = np.zeros((m + 2) * (n + 2))
  psi_temp = np.zeros((m + 2) * (n + 2))

  ctx, queue = setup_CL()
  kernel_jacobi_step, kernel_array_copy, kernel_boundary_psi, psi_temp_buffer, psi_buffer = setup_kernel(ctx, psi, psi_temp)

  njit_boundary_start = time.time()
  boundary_psi(psi, m, n, b, h, w)
  njit_boundary_duration = time.time() - njit_boundary_start
  print(f"boundary_psi: {njit_boundary_duration}s")

  kernel_boundary_start = time.time()
  kernel_boundary_psi(queue, (2,), None, psi_buffer, np.int32(m), np.int32(n), np.int32(b), np.int32(h), np.int32(w))
  cl.enqueue_copy(queue, psi, psi_buffer)
  kernel_boundary_duration = time.time() - kernel_boundary_start
  print(f"boundary_psi: {kernel_boundary_duration}s")

  b_norm = np.sqrt(np.sum(psi ** 2))

  global_size = (m, n)
  local_size = (2, 2)
  print("Starting main loop...\n")
  time_start = time.time()

  
  
  for i in range(1, iterations + 1):
    if i % 100 == 0:
      print(f"Iteration {i}")

    kernel_jacobi_step(queue, global_size, local_size, psi_temp_buffer, psi_buffer, np.int32(m), np.int32(n))

    if i == iterations:
      cl.enqueue_copy(queue, psi_temp, psi_temp_buffer)
      cl.enqueue_copy(queue, psi, psi_buffer)
      err = np.sqrt(delta_sq(psi_temp, psi, m, n)) / b_norm
      break

    kernel_array_copy(queue, global_size, local_size, psi_temp_buffer, psi_buffer, np.int32(m), np.int32(n))

    total_time = time.time() - time_start
    time_for_iteration = total_time / iterations

  print("...finished")
  print(f"Total time for {iterations} iterations: {total_time}s")
  print(f"Time for each iteration: {time_for_iteration}")

  print(f"Error: {err}")


if __name__ == "__main__":
  start = time.time()
  main()
  print(f"Duration: {time.time() - start}s")

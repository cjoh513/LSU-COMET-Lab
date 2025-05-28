# Efficient WRF Simulation for Long-Distance Dust Transport

Running a WRF simulation is straightforward, but doing it **efficiently**—especially when simulating dust transport from Africa to Puerto Rico or other parts of the Americas—is much more complex. These long-distance domains are often **rectangular**, rather than square (which WRF prefers).

---

## Why Processor Decomposition Matters

If you simply select `16` processors, WRF will usually default to a square decomposition:
```text
nproc_x = 4
nproc_y = 4   # Because 4 × 4 = 16
```
However, for **rectangular domains**, this choice is often **inefficient**. You should not blindly assign the same number of processors to X and Y directions.

---

## Example Domain Setup

```fortran
&domains
 max_dom = 3
 e_we    = 221, 65, 57
 e_sn    = 61,  45, 37
```

Let’s assume you must run with a small number of processors, say **4 cores**—this would work but may not be optimal.

---

## Rules for Choosing `nproc_x` and `nproc_y`

1. **Each processor must handle at least 10 grid cells** in each direction:
   ```text
   (e_we - 1) / nproc_x ≥ 10
   (e_sn - 1) / nproc_y ≥ 10
   ```

2. **The same `nproc_x` and `nproc_y` apply to all domains.**

---

## Minimum Grid Sizes → Determine Max Processors

From the third domain:
- `e_we = 57 → 56 cells → 56 / 10 ≈ 5 → nproc_x ≤ 5`
- `e_sn = 37 → 36 cells → 36 / 10 ≈ 3 → nproc_y ≤ 3`

So the safest **maximum** decomposition is:
```text
nproc_x = 5
nproc_y = 3
```
This setup uses `5 × 3 = 15 processors`, which respects both rules above.

---

## Enhancing Efficiency: Adjust Domain Dimensions

You can slightly modify the domains to allow **better parallelism**:

```fortran
&domains
 max_dom = 3
 e_we    = 221, 65, 60
 e_sn    = 61,  45, 40
```

With these rounded values:
- `e_we = 60 → 59 cells → 59 / 6 ≈ 9.8`
- `e_sn = 40 → 39 cells → 39 / 4 ≈ 9.75`

Both are **very close** to the required 10 cells per processor. So you can now use:
```text
nproc_x = 6
nproc_y = 4
```
This setup uses `6 × 4 = 24 processors`, enabling better load balancing and faster simulations.

---

## ✅ Summary

- Always analyze **grid size** before choosing the number of processors.
- Ensure `(e_we - 1) % nproc_x == 0` and `(e_sn - 1) % nproc_y == 0`.
- Make sure each processor gets **at least 10×10 cells**.
- Rectangular domains → **asymmetric processor decomposition**.
- Tweak domain size (if possible) to improve parallel efficiency.

> Efficient domain decomposition can significantly **reduce simulation time** and **maximize HPC resource usage**.

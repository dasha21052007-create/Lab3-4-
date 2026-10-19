import random
import time
import math
import matplotlib.pyplot as plt

def binary_search(a, q):
    lo, hi = 0, len(a) - 1
    cmps = 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        cmps += 1
        if a[mid] == q:
            return mid, cmps
        elif a[mid] < q:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, cmps

def make_uniform_data(n, seed=42):
    rng = random.Random(seed)
    data = rng.sample(range(10 * n), n)
    data.sort()
    return data

def benchmark(func, data, queries):
    start = time.perf_counter()
    all_cmps = []
    for q in queries:
        _, c = func(data, q)
        all_cmps.append(c)
    elapsed = time.perf_counter() - start
    avg_time = elapsed / len(queries)
    return avg_time, all_cmps

if __name__ == "__main__":
    SIZES = [5_000, 50_000, 500_000]
    K = 2000

    rng = random.Random(7)

    times = []
    avg_cmps = []
    all_cmps_per_n = []

    for n in SIZES:
        print(f"\n=== n = {n} ===")
        data = make_uniform_data(n)

        queries = [rng.choice(data) for _ in range(K)]

        t, cmps_list = benchmark(binary_search, data, queries)
        avg_c = sum(cmps_list) / len(cmps_list)

        times.append(t)
        avg_cmps.append(avg_c)
        all_cmps_per_n.append(cmps_list)

        theory = math.log2(n)
        print(f"  Среднее время:      {t*1e6:>8.2f} мкс/запрос")
        print(f"  Среднее сравнений:  {avg_c:>8.2f}")
        print(f"  Теория log2(n):     {theory:>8.2f}")

    plt.figure(figsize=(8, 5))
    plt.plot(SIZES, [t * 1e6 for t in times], marker="o",
             color="tab:blue", label="Двоичный поиск")
    plt.xscale("log")
    plt.xlabel("n (лог. шкала)")
    plt.ylabel("Среднее время запроса, мкс")
    plt.title("Вариант 7: время запроса (двоичный поиск)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("var7_binary_time.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(SIZES, avg_cmps, marker="s",
             color="tab:blue", label="Факт. среднее")
    plt.plot(SIZES, [math.log2(n) for n in SIZES], marker="^",
             color="tab:green", linestyle="--", label="Теория log2(n)")
    plt.xscale("log")
    plt.xlabel("n (лог. шкала)")
    plt.ylabel("Среднее число сравнений")
    plt.title("Вариант 7: сравнения (двоичный поиск)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("var7_binary_cmps.png", dpi=150)
    plt.close()

    n_big_idx = len(SIZES) - 1
    n_big = SIZES[n_big_idx]
    cmps = all_cmps_per_n[n_big_idx]
    emp_mean = sum(cmps) / len(cmps)
    theory = math.log2(n_big)

    plt.figure(figsize=(8, 5))
    plt.hist(cmps, bins=15, edgecolor="black", alpha=0.7, color="tab:blue")
    plt.axvline(emp_mean, color="red", ls="--", linewidth=2,
                label=f"Факт. среднее = {emp_mean:.2f}")
    plt.axvline(theory, color="green", ls=":", linewidth=2,
                label=f"Теория log2(n) ≈ {theory:.2f}")
    plt.xlabel("Число сравнений на запрос")
    plt.ylabel("Частота")
    plt.title(f"Б7: гистограмма сравнений — двоичный поиск, n = {n_big}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("var7_binary_hist.png", dpi=150)
    plt.close()

    print("\nГотово. Сохранены файлы:")
    print("  var7_binary_time.png   — график времени")
    print("  var7_binary_cmps.png   — график сравнений vs теория")
    print("  var7_binary_hist.png   — гистограмма (Б7)")
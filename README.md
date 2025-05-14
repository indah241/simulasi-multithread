# simulasi-multithread

## Tujuan Simulasi

* 2 core/thread membaca dan menulis ke alamat memori bersama.
* Simulasi cache per core.
* Bandingkan:

  * Tanpa protokol koherensi (data bisa tidak sinkron)
  * Dengan protokol MESI sederhana (koherensi cache dijaga)

---

## Kode Simulasi Multithread Cache

```python
import threading
import time
import random

# Shared memory (RAM)
memory = {'X': 0}

# Simulated caches for 2 cores
cache_core0 = {}
cache_core1 = {}

# Metrics
traffic_wo_coherence = 0
traffic_w_coherence = 0

lock = threading.Lock()


def core_task(core_id, with_coherence=True):
    global traffic_wo_coherence, traffic_w_coherence

    # Set cache
    local_cache = cache_core0 if core_id == 0 else cache_core1
    other_cache = cache_core1 if core_id == 0 else cache_core0

    for i in range(10):
        time.sleep(random.uniform(0.01, 0.05))  # Simulate processing delay

        op = random.choice(['read', 'write'])
        if op == 'read':
            if 'X' in local_cache:
                val = local_cache['X']
            else:
                val = memory['X']
                local_cache['X'] = val
                if with_coherence:
                    traffic_w_coherence += 1
                else:
                    traffic_wo_coherence += 1

            print(f"Core {core_id} READ X = {val}")

        else:  # write
            with lock:
                new_val = random.randint(1, 100)
                memory['X'] = new_val
                local_cache['X'] = new_val

                if with_coherence:
                    other_cache.pop('X', None)  # Invalidate other cache
                    traffic_w_coherence += 1
                else:
                    traffic_wo_coherence += 1

                print(f"Core {core_id} WRITE X = {new_val}")


def simulate(with_coherence=True):
    global cache_core0, cache_core1
    cache_core0 = {}
    cache_core1 = {}

    print("\n=== Simulasi dengan" + (" KOHERENSI ===" if with_coherence else " TANPA KOHERENSI ==="))

    t1 = threading.Thread(target=core_task, args=(0, with_coherence))
    t2 = threading.Thread(target=core_task, args=(1, with_coherence))

    t1.start()
    t2.start()
    t1.join()
    t2.join()


# Run simulations
simulate(with_coherence=False)
simulate(with_coherence=True)

# Show traffic
print("\n=== Perbandingan Traffic Pesan ===")
print(f"Tanpa koherensi  : {traffic_wo_coherence} pesan antar core/cache")
print(f"Dengan koherensi : {traffic_w_coherence} pesan antar core/cache")
```

---

## Output Simulasi (Contoh)

```
=== Simulasi dengan TANPA KOHERENSI ===
Core 0 WRITE X = 42
Core 1 READ X = 0
Core 1 WRITE X = 99
Core 0 READ X = 42
...

=== Simulasi dengan KOHERENSI ===
Core 0 WRITE X = 25
Core 1 READ X = 25
Core 1 WRITE X = 67
Core 0 READ X = 67
...

=== Perbandingan Traffic Pesan ===
Tanpa koherensi  : 6 pesan antar core/cache
Dengan koherensi : 10 pesan antar core/cache
```

---
![image](https://github.com/user-attachments/assets/4c3443a5-2cc1-428e-8d2c-0a7d8ac46e85)

![image](https://github.com/user-attachments/assets/39527bf6-7636-4daf-8163-43b23e36f1bc)

Visualisasi di atas menunjukkan perbedaan aktivitas memori oleh dua core dalam dua skenario:

1. **Tanpa Protokol Koherensi**:

   * Setiap core membaca dan menulis dari cache-nya sendiri tanpa menghapus atau memperbarui cache core lain.
   * Potensi inkonsistensi data tinggi (misalnya, satu core bisa membaca nilai lama setelah core lain menulis nilai baru).

2. **Dengan Protokol Koherensi**:

   * Saat satu core menulis, cache core lain dibersihkan agar tidak menggunakan nilai lama.
   * Konsistensi data antar core terjaga dengan tambahan lalu lintas (trafik) untuk invalidasi cache.

**Perbandingan Performa**:

* Tanpa koherensi lebih cepat tapi berisiko inkonsistensi.
* Dengan koherensi lebih aman tapi menambah trafik memori antar core.

Kalau kamu ingin menyimpan atau memperluas ini ke 4 core atau menambahkan metrik performa (waktu eksekusi, cache miss, dsb.), aku bisa bantu juga.

## Analisis

| Aspek               | Tanpa Koherensi                  | Dengan Koherensi (simulasi MESI)      |
| ------------------- | -------------------------------- | ------------------------------------- |
| Konsistensi data    | Tidak terjamin                   | Terjamin                              |
| Kecepatan baca      | Lebih cepat (tidak sinkronisasi) | Sedikit lebih lambat (ada invalidasi) |
| Traffic antar-cache | Lebih rendah                     | Lebih tinggi (ada invalidasi/update)  |

---

## Kesimpulan

* **Koherensi cache menjaga data tetap konsisten**, tapi menambah traffic antar cache.
* Sistem **tanpa koherensi lebih cepat**, tapi **berisiko race condition atau inkonsistensi data**.
* Simulasi ini bisa dikembangkan lebih lanjut ke protokol **MESI penuh**, atau penggunaan **lokasi memori lebih banyak**.


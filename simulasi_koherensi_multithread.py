
import threading
import time

# Memori bersama dan lock
shared_data = {'X': 0}
lock = threading.Lock()

def core1():
    print("[Core 1] Membaca X =", shared_data['X'])
    time.sleep(1)
    with lock:
        shared_data['X'] = 1
        print("[Core 1] Menulis X = 1")

def core2():
    time.sleep(2)
    print("[Core 2] Membaca X =", shared_data['X'])

# Tanpa koherensi (tidak pakai lock di baca)
def run_without_coherence():
    global shared_data
    shared_data = {'X': 0}
    print("=== Simulasi Tanpa Protokol Koherensi ===")
    t1 = threading.Thread(target=core1)
    t2 = threading.Thread(target=core2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# Dengan koherensi (pakai lock)
def core2_coherent():
    time.sleep(2)
    with lock:
        print("[Core 2] Membaca X =", shared_data['X'])

def run_with_coherence():
    global shared_data
    shared_data = {'X': 0}
    print("=== Simulasi Dengan Protokol Koherensi ===")
    t1 = threading.Thread(target=core1)
    t2 = threading.Thread(target=core2_coherent)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    run_without_coherence()
    print("\n")
    run_with_coherence()

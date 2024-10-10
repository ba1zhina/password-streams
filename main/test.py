import hashlib
import itertools
import time
from concurrent.futures import ThreadPoolExecutor

def generate_passwords():
    chars = 'abcdefghijklmnopqrstuvwxyz'
    for password in itertools.product(chars, repeat=5):
        yield ''.join(password)

def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

def brute_force_single_thread(target_hash_md5, target_hash_sha256):
    for password in generate_passwords():
        if hash_md5(password) == target_hash_md5 or hash_sha256(password) == target_hash_sha256:
            return password

def brute_force_multi_thread(target_hash_md5, target_hash_sha256, num_threads):
    def worker(passwords_chunk):
        for password in passwords_chunk:
            if hash_md5(password) == target_hash_md5 or hash_sha256(password) == target_hash_sha256:
                return password

    passwords = list(generate_passwords())
    chunk_size = len(passwords) // num_threads
    chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(worker, chunks)
        for result in results:
            if result:
                return result

def main():
    target_hash_md5 = input("Введите MD5 хеш: ").strip()
    target_hash_sha256 = input("Введите SHA-256 хеш: ").strip()

    print("Однопоточный режим:")
    start_time = time.time()
    password = brute_force_single_thread(target_hash_md5, target_hash_sha256)
    end_time = time.time()
    if password:
        print(f"Найден пароль: {password}")
    else:
        print("Пароль не найден")
    print(f"Время выполнения: {end_time - start_time} секунд")

    num_threads = int(input("\nВведите количество потоков для многопоточного режима: "))
    print(f"\nМногопоточный режим с {num_threads} потоками:")
    start_time = time.time()
    password = brute_force_multi_thread(target_hash_md5, target_hash_sha256, num_threads)
    end_time = time.time()
    if password:
        print(f"Найден пароль: {password}")
    else:
        print("Пароль не найден")
    print(f"Время выполнения: {end_time - start_time} секунд")

if __name__ == "__main__":
    main()

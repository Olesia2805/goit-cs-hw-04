import threading
import time

def build_shift_table(pattern):
    
    table = {}
    length = len(pattern)
    
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
   
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):

    shift_table = build_shift_table(pattern)
    i = 0 

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1

def file_search(file_path, keywords, results, lock):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        for keyword in keywords:
            position = boyer_moore_search(content, keyword)
            if position != -1:
                with lock:
                    if keyword not in results:
                        results[keyword] = []
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"The file could not be processed {file_path}: {e}")


def thread_function(file_list, keywords, results, lock):
    """A thread function to search for keywords in a list of files."""
    for file_path in file_list:
        if isinstance(file_path, str):  # Checking the correctness of the path
            file_search(file_path, keywords, results, lock)


def multi_threaded_search(file_paths, keywords):
    """Basic function for running multi-threaded search."""
    start_time = time.time()
    num_threads = min(4, len(file_paths))
    threads = []
    results = {}
    lock = threading.Lock()

    files_per_thread = len(file_paths) // num_threads
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = start_index + files_per_thread if i != num_threads - 1 else len(file_paths)
        thread_files = file_paths[start_index:end_index]
        thread = threading.Thread(target=thread_function, args=(thread_files, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Search execution time: {end_time - start_time:.6f} seconds")
    print(f"Search Results: {results}")
    return results


if __name__ == '__main__':
    file_paths = ["files/article1.txt", "files/article2.txt"] 
    keywords = ["data", "graph"]  # List of keywords
    multi_threaded_search(file_paths, keywords)
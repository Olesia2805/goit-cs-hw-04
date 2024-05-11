import multiprocessing
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

def file_search(file_path, keywords, results_queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        file_results = {}
        for keyword in keywords:
            position = boyer_moore_search(content, keyword)
            if position != -1:
                if keyword not in file_results:
                    file_results[keyword] = []
                file_results[keyword].append(file_path)
        results_queue.put(file_results)
    except Exception as e:
        print(f"The file could not be processed {file_path}: {e}")

def multi_process_search(file_paths, keywords):
    start_time = time.time()
    num_processes = min(4, len(file_paths))
    results_queue = multiprocessing.Queue()

    processes = []
    for file_path in file_paths:
        process = multiprocessing.Process(target=file_search, args=(file_path, keywords, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collecting results from the queue
    results = {}
    while not results_queue.empty():
        file_results = results_queue.get()
        for keyword, paths in file_results.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(paths)

    end_time = time.time()
    print(f"Search execution time: {end_time - start_time:.6f} seconds")
    print(f"Search Results: {results}")
    return results

if __name__ == '__main__':
    file_paths = ["files/article1.txt", "files/article2.txt"] 
    keywords = ["data", "graph"]  # List of keywords
    multi_process_search(file_paths, keywords)

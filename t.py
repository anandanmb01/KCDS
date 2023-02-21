import multiprocessing

def process_item(item):
    # function to process each item in the loop
    print(item)
    # ...

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # items to process
num_processes = 4  # number of processes to use

with multiprocessing.Pool(num_processes) as pool:
    results = list(pool.map(process_item, items))
    # do something with the results, if needed

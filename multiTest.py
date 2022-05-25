import multiprocessing as mp
import time

start = time.perf_counter()

def do_something(z):
    x, y = z
    return x+y

if __name__ == '__main__':
    with mp.Pool(3) as p:
        z = p.map(do_something, [[1,2],[4,2],[5,3]])
    print(z)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')

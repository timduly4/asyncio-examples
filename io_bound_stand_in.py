import random
import time

random.seed(28)


def io_bound_stand_in(task_number: int) -> None:
    wait_time = random.gauss(2, 0.2)
    print(f"Initialized task number: {task_number}, running 'i/o task' for {wait_time:.2f} seconds")
    time.sleep(wait_time)
    print(f"Done with task number: {task_number}")


def main() -> None:
    for i in range(3):
        io_bound_stand_in(i)


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    elapsed = time.perf_counter() - t0
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

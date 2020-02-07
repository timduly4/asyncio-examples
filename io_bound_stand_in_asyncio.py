import asyncio
import random

random.seed(28)


async def io_bound_stand_in(task_number: int) -> None:
    wait_time = random.gauss(2, 0.2)
    print(f"Initialized task number: {task_number}, running 'i/o task' for {wait_time:.2f} seconds")
    await asyncio.sleep(wait_time)
    print(f"Done with task number: {task_number}")


async def main() -> None:
    tasks = []
    for i in range(3):
        tasks.append(io_bound_stand_in(i))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    import time

    t0 = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - t0
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

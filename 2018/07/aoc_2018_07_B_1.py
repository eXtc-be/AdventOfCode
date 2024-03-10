# aoc_2018_07_B_1.py - Day 7: The Sum of Its Parts - part 2
# How long will it take to complete all the steps?
# https://adventofcode.com/2018/day/7


from aoc_2018_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_steps,
)

from tools import time_it

# other imports

from pprint import pprint


WORKERS = 5
WORKERS_TEST = 2

DELAY = 60
DELAY_TEST = 0


# other functions


@time_it
def main(data_lines: list[str], workers: int = WORKERS, delay: int = DELAY, verbose: bool = False) -> None:
    forward_steps, backward_steps = get_steps(data_lines)
    # pprint(forward_steps)
    # pprint(backward_steps)

    result = ''
    queue = []
    workers = [
        {
            'id': i,
            'step': '.',
            'timer': 0
        }
        for i in range(1, workers+1)
    ]
    second = 0

    done_length = len('Done')
    if verbose:
        steps = set()
        for step, next_steps in forward_steps.items():
            steps.add(step)
            steps.update(next_steps)

        # print(steps)
        done_length = max(len(steps), done_length)

        wks = '   '.join(f'Worker {worker["id"]}' for worker in workers)
        print(f'Second   {wks}   {"Done":{done_length}} Queue')

    for step in forward_steps:
        if step not in backward_steps:
            queue.append(step)

    while queue or any(w['timer'] > 0 for w in workers):
        queue.sort(reverse=True)  # also works without the reverse and a pop(0)

        # assign jobs to all idle workers
        for worker in [w for w in workers if w['timer'] == 0]:
            if not queue:
                break
            step = queue.pop()
            worker['step'] = step
            worker['timer'] = delay + ord(step) - ord('A') + 1

        # show progress
        if verbose:
            wks = '   '.join(f'{worker["step"]:^8}' for worker in workers)
            print(f'{second:4}     {wks}   {result:{done_length}} {"".join(queue)}')

        # advance time
        second += 1
        for worker in [w for w in workers if w['timer'] != 0]:
            worker['timer'] -= 1
            if worker['timer'] == 0:
                result += worker['step']
                # add new steps to queue
                for f in forward_steps[worker['step']]:
                    if all(b in result for b in backward_steps[f]):
                        queue.append(f)
                worker['step'] = '.'

    # show progress
    if verbose:
        wks = '   '.join(f'{worker["step"]:^8}' for worker in workers)
        print(f'{second:4}     {wks}   {result}')

    print(f'End result: {second}')


if __name__ == "__main__":
    # main(test_data, WORKERS_TEST, DELAY_TEST, verbose=True)
    main(load_data(DATA_PATH))

    # using test_data:
    #   End result: 15
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 908
    #   Finished 'main' in 2 milliseconds

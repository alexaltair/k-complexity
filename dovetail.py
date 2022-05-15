import os
import signal
import subprocess
import time


def utm(my_input):
    # return "python3 -u tester.py " + my_input
    # Perl script from https://github.com/tromp/AIT/blob/642452f9/blc.pl
    return "echo " + my_input + " | perl AIT/blc.pl -b"


def int_to_binary_string(integer):
    if integer < 0:
        raise BaseException("Integer should be positive")

    string = ''
    while integer > 0:
        if integer % 2:
            string = '0' + string
            integer = integer - 1
            integer = integer//2
        else:
            string = '1' + string
            integer = integer//2
            integer = integer - 1

    return string


def binary_string_to_int(bin_str):
    l = len(bin_str)
    integer = 2**l
    for i in range(l):
        if bin_str[i] == '1':
            integer += 2**(l - i - 1)
    return integer - 1


shortest_programs = {}

def put_output_in_table(output, my_input):
    if len(output) > len(my_input):
        print("--- We have compressed something! ---")
    if output not in shortest_programs:
        shortest_programs[output] = my_input
    else:
        shortest_programs[output] = min(my_input, shortest_programs[output])

# Each value is a tuple: (
#     my_input, a string representing the program binary
#     proc, a subprocess.Popen instance
#     n, number of times the proc has been tried
# )
running_procs = []

try:
    i = 0
    while True:
        for j, (my_input, proc, runs) in enumerate(running_procs):
            try:
                runs += 1
                running_procs[j] = (my_input, proc, runs)
                print(f"Trying {my_input} run {runs}")
                os.kill(proc.pid, signal.SIGCONT)
                proc.wait(timeout=1/runs)
                outs, errs = proc.communicate()

                if errs:
                    running_procs.pop(j)
                else:
                    output_bytes = outs.strip()
                    try:
                        output = output_bytes.decode("ascii")
                        assert all(char in ['0', '1'] for char in output)
                        print(f"Inserting into the table after run {runs}:")
                        if runs > 1:
                            print("--- This is more than one run! ---")
                        print(f"{output} -> {my_input}")
                        put_output_in_table(output, my_input)
                    except ValueError:
                        print(f"Ignoring program {my_input} run {runs} which output the following value:")
                        print(output_bytes)
                    except AssertionError:
                        print(f"Ignoring program {my_input} run {runs} because it output non-binary:")
                        print(output_bytes)
                    print(f"Done with {my_input} run {runs}")
                    running_procs.pop(j)
            except subprocess.TimeoutExpired:
                os.kill(proc.pid, signal.SIGSTOP)

        my_input = int_to_binary_string(i)
        print(f"Launching {my_input}")
        proc = subprocess.Popen(
            utm(my_input),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        os.kill(proc.pid, signal.SIGSTOP)
        running_procs.append((my_input, proc, 0))
        i += 1
except KeyboardInterrupt:
    [proc.kill() for (_, proc, _) in running_procs]
    print(shortest_programs)

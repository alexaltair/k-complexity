import os
import signal
import subprocess
import time


def utm(my_input):
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


shortest_programs = {}

def put_output_in_table(output, my_input):
    if output not in shortest_programs:
        shortest_programs[output] = my_input
    else:
        shortest_programs[output] = min(my_input, shortest_programs[output])

# Each value is a triple of (my_input, proc, running_output) because programs may
# output bits very slowly.
running_procs = []

try:
    i = 0
    while True:
        for j, (my_input, proc, running_output) in enumerate(running_procs):
            try:
                os.kill(proc.pid, signal.SIGCONT)
                proc.wait(timeout=1)
                outs, errs = proc.communicate()

                if errs:
                    running_procs.pop(j)
                else:
                    put_output_in_table(running_output + outs, my_input)
                    running_procs.pop(j)
            except subprocess.TimeoutExpired:
                # It could have output without finishing, so we ask for that
                # output again here
                # psutil.Process(pid=proc.pid).suspend()
                os.kill(proc.pid, signal.SIGSTOP)
                # outs, errs = proc.communicate()
                # if errs:
                #     proc.kill()
                #     running_procs.pop(j)
                # else:
                #     running_procs[2] += outs

        my_input = int_to_binary_string(i)
        print(my_input)
        proc = subprocess.Popen(
            utm(my_input),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        os.kill(proc.pid, signal.SIGSTOP)
        running_procs.append((my_input, proc, b''))
        i += 1
except KeyboardInterrupt:
    [proc.kill() for (_, proc, _) in running_procs]
    print(shortest_programs)

import math

# import sys
from datetime import datetime
from time import time

import colorama
import tqdm
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

# from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from utils import (
    # ScryptV2Error,
    convert_to_isa_circuit,
    create_qc,
    generate_obeservables,
    run_job,
)

colorama.init(autoreset=True)

# TODO
# if __name__ == "__main__":
#    if str(sys.argv[len(sys.argv) - 1]) == "qpu":
#        BACKEND = QiskitRuntimeService().least_busy(
#            operational=True,
#        )
#    elif str(sys.argv[len(sys.argv) - 1]) == "sim":
#        BACKEND = FakeBelemV2()
#    else:
#        raise ScryptV2Error("No backend provided.")
# else:
#    BACKEND = FakeBelemV2()


def __scrngV2(
    a: int,
    b: int,
    digits: int = 3,
    qubits: int = 5,
    debug: bool = False,
    backend=FakeBelemV2(),
):
    n_qubits = qubits
    print(
        ">>> Creating quantum circuit..." if debug else "",
        end="\n" if debug else "",
        flush=debug,
    )
    qc: QuantumCircuit = create_qc(n=n_qubits)
    print(
        ">>> Creating observables..." if debug else "",
        end="\n" if debug else "",
        flush=debug,
    )
    observables: list[SparsePauliOp] = generate_obeservables(
        n_qubits=n_qubits, n_observables=30
    )
    print(
        ">>> Converting to ISA circuit..." if debug else "",
        end="\n" if debug else "",
        flush=debug,
    )
    isa_circuit = convert_to_isa_circuit(backend=backend, qc=qc)
    print(">>> Running job..." if debug else "", end="\n" if debug else "", flush=debug)
    job = run_job(backend=backend, observables=observables, isa_circuit=isa_circuit)
    values = job.result()[0].data.evs.tolist()
    errors = job.result()[0].data.stds.tolist()
    print(
        ">>> Returning results..." if debug else "",
        end="\n" if debug else "",
        flush=debug,
    )
    return round(
        math.fabs(
            math.fsum(values) / len(values) * math.fsum(errors) * 1000 / 30 * (b - a)
        )
        + a,
        ndigits=digits,
    )


def random_nums(a: int, b: int, n: int, debug: bool = False):
    rn_list = []
    for i in range(n):
        rn_list.append(__scrngV2(a, b, debug=debug))
    return rn_list


def random_nums_pretty(a: int, b: int, n: int, debug: bool = False):
    dt = datetime.now()
    rn_list = []
    start = time()
    for i in tqdm.trange(
        n,
        desc="Generation progress",
        unit="nums",
        dynamic_ncols=True,
        bar_format="{l_bar}{bar}| Generated {n_fmt}/{total_fmt} [Elapsed {elapsed}, Remaining {remaining}]; Rate{rate_fmt}",
        disable=debug,
    ):
        print(
            f"Number {i + 1}" if debug else "", end="\n" if debug else "", flush=debug
        )
        rn_list.append(__scrngV2(a, b, debug=debug))
    end = time()
    print(colorama.Style.BRIGHT + "=========== Results ===========")
    print(
        colorama.Fore.BLUE + "Generated numbers:",
        colorama.Style.DIM + str(rn_list),
    )
    print(
        colorama.Fore.CYAN + "Generation time:",
        colorama.Style.DIM + f"{(end - start):.2f}s",
    )
    print(
        colorama.Fore.RED + "Generation timestamp:",
        colorama.Style.DIM + f"{dt.strftime('Generation on %Y-%m-%d at %I:%M.%S %p')}",
    )
    return rn_list

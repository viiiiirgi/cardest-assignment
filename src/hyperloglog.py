#!/usr/bin/env python3

import argparse
import math
import sys

import randomhash


def estimate_cardinality(dataset: list[str], pow_register: int) -> float:
    """
    Estimate the cardinality (number of distinct elements) of a dataset using the HyperLogLog algorithm.

    Cardinality estimate E with typical relative error ±1.04/sqrt(m).

    References:
        - https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf

    Author:
        - Nicosia Virginia

    Parameters:
    -----------
    dataset : list[str]
        The input data for which the cardinality needs to be estimated.

    pow_register : int (4..16)
        The power value used to determine the number of registers (2 ** pow_register).
        This value controls the accuracy of the estimate; higher values provide more accuracy at the cost of increased memory usage.

    Returns:
    --------
    estimate: float
        An estimate of the number of distinct elements in the dataset.
    """
    if pow_register < 4 or pow_register > 16:
        raise ValueError("pow_register should be in range 4..16")

    n_registers: int = 2**pow_register
    registers = [0] * n_registers

    rhf = randomhash.RandomHashFamily(count=1)

    for element in dataset:
        hash = rhf.hashes(element)

        register_idx, remaining_bits = hash[0] >> (32 - pow_register), hash[0] & int(
            ("0" * pow_register) + ("1" * (32 - pow_register)), 2
        )
        leftmost_1bit = (32 - pow_register) - remaining_bits.bit_length() + 1
        registers[register_idx] = max(registers[register_idx], leftmost_1bit)

    # source: https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf (Figure 3)
    if n_registers == 16:
        bias_correction_alpha = 0.673
    elif n_registers == 32:
        bias_correction_alpha = 0.697
    elif n_registers == 64:
        bias_correction_alpha = 0.709
    elif n_registers >= 128:
        bias_correction_alpha = 0.7213 / (1 + 1.079 / n_registers)
    else:
        raise ValueError("pow_register should be in range 4..16")  # unreachable

    raw_estimate: float = (bias_correction_alpha * n_registers**2) / sum(
        [2**-reg for reg in registers]
    )

    # Bias correction, source: https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf (Figure 3)
    if raw_estimate <= 2.5 * n_registers:
        rz = registers.count(0)

        if rz != 0:
            estimate = n_registers * math.log(
                n_registers / rz
            )  # small range correction
        else:
            estimate = raw_estimate
    elif raw_estimate <= (2**32) / 30:
        estimate = raw_estimate  # intermediate range - no correction
    elif raw_estimate > (2**32) / 30:
        estimate = -(2**32) * math.log(
            1 - raw_estimate / (2**32)
        )  # large range correction
    else:
        raise ValueError("Unreachable")  # unreachable

    return estimate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estimate the cardinality of a dataset using the HyperLogLog algorithm.",
        epilog="The dataset should be a file where each line is one element of data",
    )
    _ = parser.add_argument(
        "dataset",
        type=argparse.FileType("r"),
        help="Path to the input dataset file (text file).",
    )
    _ = parser.add_argument(
        "-b",
        "--pow",
        type=int,
        default=16,
        help="The power value used to determine the number of registers (2 ** pow_register). Must be between 4 and 16 (default: 16).",
    )

    args = parser.parse_args()

    try:
        dataset = [word.strip() for word in args.dataset]
        args.dataset.close()
    except IOError:
        print(f"Error: Could not read file '{args.dataset.name}'.")
        sys.exit(-1)

    try:
        estimate = estimate_cardinality(dataset, args.pow)
        print(f"Estimated cardinality: {estimate}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(-1)

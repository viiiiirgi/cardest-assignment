#!/usr/bin/env python3


import argparse
import heapq
import sys

import randomhash


def estimate_cardinality(dataset: list[str], record_count: int) -> float:
    """
    Estimate the cardinality (number of distinct elements) of a dataset using the RECORDINALITY algorithm.

    References:
        - https://dmtcs.episciences.org/3002/pdf

    Author:
        - Virginia Nicosia

    Parameters:
    -----------
    dataset : list[str]
        The input data for which the cardinality needs to be estimated.

    record_count : int
        The number of top hash values (k-records) to track in the algorithm.
        This value controls the accuracy of the estimate; higher values provide more accuracy at the cost of increased memory usage.

    Returns:
    --------
    float
        An estimate of the number of distinct elements in the dataset.
    """
    rhf = randomhash.RandomHashFamily(count=1)

    records = [float("-inf")] * record_count
    record_change = 0

    for element in dataset:
        hash = rhf.hashes(element)

        if hash[0] not in records and hash[0] > records[0]:
            _ = heapq.heapreplace(records, hash[0])
            record_change += 1

    estimate = (
        record_count * (1 + (1 / record_count)) ** (record_change - record_count + 1)
        - 1
    )

    return estimate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estimate the cardinality of a dataset using the Recordinality algorithm.",
        epilog="The dataset should be a file where each line is one element of data",
    )
    _ = parser.add_argument(
        "dataset",
        type=argparse.FileType("r"),
        help="Path to the input dataset file (text file).",
    )
    _ = parser.add_argument(
        "-k",
        "--records",
        type=int,
        default=16,
        help="The number of top hash values to track. Higher values increase accuracy but require more memory. (Default: 16)",
    )

    args = parser.parse_args()

    try:
        dataset = [word.strip() for word in args.dataset]
        args.dataset.close()
    except IOError:
        print(f"Error: Could not read file '{args.dataset.name}'.")
        sys.exit(-1)

    try:
        estimate = estimate_cardinality(dataset, args.records)
        print(f"Estimated cardinality: {estimate}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(-1)

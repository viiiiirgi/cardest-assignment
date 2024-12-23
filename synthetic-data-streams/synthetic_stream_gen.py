#!/usr/bin/env python3

import argparse
import datetime
import os

import numpy as np


def synthetic_stream_gen(distict_elements: int, stream_elements: int, skewness: float):
    # Compute normalization constant c_n
    ranks = np.arange(1, distict_elements + 1)
    probabilities = ranks**-skewness
    probabilities /= probabilities.sum()  # Normalize to sum to 1

    # Generate stream of length N
    stream = np.random.choice(ranks, size=stream_elements, p=probabilities)
    return stream


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a synthetic data stream using Zipfian's law."
    )

    # Add arguments
    _ = parser.add_argument(
        "distict_elements",
        type=int,
        help="Number of distinct elements.",
    )
    _ = parser.add_argument(
        "elements",
        type=int,
        help="Total length of the data stream.",
    )
    _ = parser.add_argument(
        "skewness",
        type=float,
        help="Zipfian distribution skewness parameter.",
    )
    _ = parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save the output file (default is current directory).",
    )

    # Parse the arguments
    args = parser.parse_args()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"zipfian_{timestamp}.synth_stream"
    output_path = os.path.join(args.output_dir, output_filename)

    with open(output_path, "w") as f:
        for i in synthetic_stream_gen(
            args.distict_elements, args.elements, args.skewness
        ):
            _ = f.write(f"{i}\n")

    print(f"Stream saved to {output_path}")

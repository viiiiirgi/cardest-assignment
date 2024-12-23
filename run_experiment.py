#!/usr/bin/env python3
# pyright: basic


if __name__ == "__main__":
    import argparse

    from src import hyperloglog as hll
    from src import recordinality as rec

    parser = argparse.ArgumentParser(
        description="Run cardinality estimation experiments using HyperLogLog or Recordinality.",
        epilog="The dataset should be a file where each line is one element of data",
    )

    _ = parser.add_argument(
        "dataset",
        type=argparse.FileType("r"),
        help="Path to the input file containing the data to estimate cardinality.",
    )

    _ = parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        help="Path to the output file where results will be written.",
    )

    _ = parser.add_argument(
        "--algorithm",
        choices=["hll", "rec", "all"],
        default="all",
        help="Specify the algorithm to use: 'hll' for HyperLogLog, 'rec' for Recordinality, or 'all' for both. Default is 'all'.",
    )

    _ = parser.add_argument(
        "--simulations",
        type=int,
        default=100,
        help="Number of simulations for the experiment",
    )

    args = parser.parse_args()

    # 16 - 512, 4 - 9 (hll)
    dataset = [word.strip() for word in args.dataset]

    print(
        f"Dataset: {args.dataset.name}, simulations: {args.simulations}",
        file=args.output,
    )

    if args.algorithm == "hll" or args.algorithm == "all":
        print("Estimate for HyperLogLog.", file=args.output)

        hll_estimate: dict[int, float] = {}
        for pow in range(4, 10):
            estimation_sums = 0
            for experiments in range(0, args.simulations):
                estimation_sums += hll.estimate_cardinality(dataset, pow)

            hll_estimate[pow] = estimation_sums / args.simulations

            print(f"k = {2 ** pow}, estimate = {hll_estimate[pow]:.2f}", file=args.output)

    if args.algorithm == "rec" or args.algorithm == "all":
        print("Estimate for Recordinality.", file=args.output)

        rec_estimate: dict[int, float] = {}
        for pow in range(4, 10):
            estimation_sums = 0
            for experiments in range(0, args.simulations):
                estimation_sums += rec.estimate_cardinality(dataset, 2**pow)

            rec_estimate[pow] = estimation_sums / args.simulations

            print(f"k = {2 ** pow}, estimate = {rec_estimate[pow]:.2f}", file=args.output)

    if args.output is not None:
        args.output.close()

    args.dataset.close()

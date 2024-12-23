# RA-MIRI Assignment #3

## How to run the experiment

The program was tested using python 3.13.

Install dependecies using pip (a virtual environment is necessary on some linux distributions)
```sh
$ python -m venv
$ . venv/bin/activate # Source the activate script to activate the virtual environment
$ pip install -r requirements.txt
```

The helper script `run_experiment.py` provides a simple repeatable setup that I used to run my experiments.
```sh
$ ./run_experiment.py --help
usage: run_experiment.py [-h] [-o OUTPUT] [--algorithm {hll,rec,all}] [--simulations SIMULATIONS] dataset

Run cardinality estimation experiments using HyperLogLog or Recordinality.

positional arguments:
  dataset               Path to the input file containing the data to estimate cardinality.

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Path to the output file where results will be written.
  --algorithm {hll,rec,all}
                        Specify the algorithm to use: 'hll' for HyperLogLog, 'rec' for Recordinality, or 'all' for both. Default is 'all'.
  --simulations SIMULATIONS
                        Number of simulations for the experiment

The dataset should be a file where each line is one element of data

```

The `src` directory contains the implementation of HyperLogLog and Recordinality and can be used as a dependency or as standalone executables.
```sh
$ python src/hyperloglog.py --help
usage: hyperloglog.py [-h] [-b POW] dataset

Estimate the cardinality of a dataset using the HyperLogLog algorithm.

positional arguments:
  dataset        Path to the input dataset file (text file).

options:
  -h, --help     show this help message and exit
  -b, --pow POW  The power value used to determine the number of registers (2 ** pow_register). Must be between 4 and 16 (default: 16).

The dataset should be a file where each line is one element of data

$ python src/recordinality.py --help
usage: recordinality.py [-h] [-k RECORDS] dataset

Estimate the cardinality of a dataset using the Recordinality algorithm.

positional arguments:
  dataset               Path to the input dataset file (text file).

options:
  -h, --help            show this help message and exit
  -k, --records RECORDS
                        The number of top hash values to track. Higher values increase accuracy but require more memory. (Default: 16)

The dataset should be a file where each line is one element of data

```

The `synthetic-data-streams/synthetic_stream_gen.py` executable can be used as a dependecy or as a standalone executable to generate a synthetic data stream as described in the assignment.
```sh
$ python synthetic-data-streams/synthetic_stream_gen.py --help
usage: synthetic_stream_gen.py [-h] [--output-dir OUTPUT_DIR] distict_elements elements skewness

Generate a synthetic data stream using Zipfian's law.

positional arguments:
  distict_elements      Number of distinct elements.
  elements              Total length of the data stream.
  skewness              Zipfian distribution skewness parameter.

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Directory to save the output file (default is current directory).

```

## Author
- Nicosia Virginia

## References
- https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
- https://dmtcs.episciences.org/3002/pdf
- https://github.com/cscotta/recordinality

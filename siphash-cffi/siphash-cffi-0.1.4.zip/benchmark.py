import time

# Relevant Module Imports
from siphash import siphash_64, siphash_128, half_siphash_32, half_siphash_64

# Setup and Preparation
ITERATION_NUMERATOR = 800000
ITERATION_ADDITIVE = 100
SIPHASH_VARIANTS = (siphash_64, siphash_128, half_siphash_32, half_siphash_64)
SIPHASH_DATA_SIZES = (8, 31, 32, 63, 64, 128, 256, 512, 1024, 1500, 1024 ** 2)
SIPHASH_DATA_CHUNKS = (b"\0" * size for size in SIPHASH_DATA_SIZES)
SIPHASH_KEY = b"\0" * 8


# Benchmark Definitions
def benchmark_factory(variant, siphash_key, siphash_data, siphash_data_length):
    def benchmark():
        variant(siphash_key, siphash_data)

    return "Algorithm {} - Size {}".format(variant.__name__, siphash_data_length), siphash_data_length, benchmark


benchmarks = []

for data_size, data_chunk in zip(SIPHASH_DATA_SIZES, SIPHASH_DATA_CHUNKS):
    for variant in SIPHASH_VARIANTS:
        benchmarks.append(benchmark_factory(variant, SIPHASH_KEY, data_chunk, data_size))

# Reporting
for benchmark_name, benchmark_weight, benchmark in benchmarks:
    actual_iterations = (ITERATION_NUMERATOR // benchmark_weight) + ITERATION_ADDITIVE
    time_start = time.time()

    for i in range(actual_iterations):
        benchmark()

    time_delta = time.time() - time_start

    print("BENCHMARK:", benchmark_name)
    print("\tCALLS / SEC  ", actual_iterations / time_delta)
    print("\tMICRO / CALL ", time_delta / actual_iterations * 1000 ** 2)

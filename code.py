import subprocess
import re
import matplotlib.pyplot as plt

# Paths to files and configurations
spmf_jar_path = "spmf.jar"  # Path to the spmf.jar
input_files = ["retail1.txt", "retail2.txt"]  # Input files for comparison
output_file = "output.txt"  # Temporary output file; SPMF will write here
algorithms = ["Apriori", "FPGrowth_itemsets", "Eclat"]
min_supports = [0.5, 1, 2, 3, 5, 7]  # Support thresholds in percentage

# Dictionary to store computation times for each file and algorithm
results = {input_file: {alg: [] for alg in algorithms} for input_file in input_files}

# Function to run a command and parse time
def run_spmf_command(algorithm, support, input_file):
    # Build the command with placeholders for algorithm and support threshold
    command = [
        "java", "-jar", spmf_jar_path, "run", algorithm,
        input_file, output_file, f"{support}%"
    ]
    
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    
    # Regex to find total time in milliseconds
    match = re.search(r"Total time ~ (\d+) ms", output)
    if match:
        time = int(match.group(1))
    else:
        time = None
    return time

# Run each algorithm at each minimum support threshold for both files
for input_file in input_files:
    print(f"\nProcessing input file: {input_file}")
    for support in min_supports:
        print(f"Running tests for support = {support}%")
        for algorithm in algorithms:
            time = run_spmf_command(algorithm, support, input_file)
            if time is not None:
                results[input_file][algorithm].append(time)
                print(f"{algorithm} at {support}% support took {time} ms")
            else:
                print(f"Failed to get time for {algorithm} at {support}% support")

# Plotting the results
for input_file in input_files:
    plt.figure(figsize=(10, 6))
    for algorithm, times in results[input_file].items():
        plt.plot(min_supports, times, marker='o', label=algorithm)

    plt.xlabel("Minimum Support (%)")
    plt.ylabel("Computation Time (ms)")
    plt.title(f"Computation Time of Apriori, FP-Growth, and Eclat at Different Support Levels for {input_file}")
    plt.legend()
    plt.grid()
    plt.show()


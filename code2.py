import subprocess
import re

# Paths to files and configurations
spmf_jar_path = "spmf.jar"  # Update with the path to your spmf.jar
input_files = ["retail1.txt", "retail2.txt"]  # List of input files
output_file = "output.txt"  # Temporary output file; SPMF will write here
algorithms = ["FPGrowth_itemsets", "FPClose", "FPMax"]
min_supports = [0.5, 1, 2, 3, 5, 7]  # Support thresholds in percentage

# Dictionary to store computation times and itemset counts for each algorithm and file
results = {file: {alg: {"time": [], "itemsets": []} for alg in algorithms} for file in input_files}

# Function to run a command, parse time, and count itemsets
def run_spmf_command(algorithm, support, input_file):
    # Build the command with placeholders for algorithm, support threshold, and input file
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
    
    # Count the number of lines in the output file for itemset count
    with open(output_file, "r") as f:
        itemset_count = sum(1 for line in f)
    
    return time, itemset_count

# Run each algorithm at each minimum support threshold for each input file
for input_file in input_files:
    print(f"\nRunning tests for input file = {input_file}")
    for support in min_supports:
        print(f"  Support = {support}%")
        for algorithm in algorithms:
            time, itemset_count = run_spmf_command(algorithm, support, input_file)
            if time is not None:
                results[input_file][algorithm]["time"].append(time)
                results[input_file][algorithm]["itemsets"].append(itemset_count)
                print(f"    {algorithm} at {support}% support took {time} ms and generated {itemset_count} itemsets")
            else:
                print(f"    Failed to get time for {algorithm} at {support}% support")

# Displaying the results in a table format for each input file
for input_file in input_files:
    print(f"\nResults Table for {input_file}:\n")
    header = ["Algorithm", "min-sup = 0.5%", "", "min-sup = 1%", "", "min-sup = 2%", "", "min-sup = 3%", "", "min-sup = 5%", "", "min-sup = 7%", ""]
    subheader = ["", "Time", "#itemsets", "Time", "#itemsets", "Time", "#itemsets", "Time", "#itemsets", "Time", "#itemsets", "Time", "#itemsets"]
    print("{:<18} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(*header))
    print("{:<18} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(*subheader))
    
    for algorithm in algorithms:
        row = [algorithm]
        for i in range(len(min_supports)):
            row.extend([results[input_file][algorithm]["time"][i], results[input_file][algorithm]["itemsets"][i]])
        print("{:<18} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(*row))


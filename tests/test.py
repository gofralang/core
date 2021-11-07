# MSPL test source.
# Tests all of the examples/source/test.

# Importing.
import subprocess
import shlex
import typing
import os.path
import time
import os

def cli_execute(commands: typing.List[str]) -> subprocess.CompletedProcess:
    """ Executes CLI command. """

    # Execute.
    return subprocess.run(" ".join(map(shlex.quote, commands)), capture_output=True)


# When we start tests.
test_start_time = time.time()

# Path to the language core.
LANG_PATH = "../src/mspl.py"

# Should we run MyPy.
MYPY_RUN = True

# If we should record new, and not test.
RECORD_NEW = False

# Run Python/Dump/Graph.
RUN_OTHER = False

# Should we clear after?
CLEAR_AFTER = True

# Test records dir.
TEST_RECORDS_DIRECTORY = "./records/"

# Test extension.
TEST_EXTENSION = ".mspl"

# Directories to run test on.
TEST_DIRECTORIS = [
    "../examples/"
]

for test_directory in TEST_DIRECTORIS:
    # Iterate over test directories.
    for test_file in os.listdir(test_directory):
        # Iterate over test files.

        # Continue if not test extension.
        if os.path.splitext(test_file)[1] != TEST_EXTENSION:
            continue

        # Base command for CLI.
        cli_execute_path = test_directory + test_file
        cli_base_command = ["python", LANG_PATH, cli_execute_path]

        # Run commands.
        run_result = cli_execute(cli_base_command + ["run", "-silent"])
        if RUN_OTHER:
            graph_result = cli_execute(cli_base_command + ["graph", "-silent"])
            python_result = cli_execute(cli_base_command + ["python", "-silent"])
            dump_result = cli_execute(cli_base_command + ["dump", "-silent"])

        # Get run result.
        run_result_current = str(run_result.stdout.decode("utf-8"))
        run_result_current = run_result_current.encode().decode("unicode_escape")

        if RECORD_NEW:
            # If we record.

            # Write result.
            record_file_path = TEST_RECORDS_DIRECTORY + os.path.basename(cli_execute_path) + ".txt"
            with open(record_file_path, "w") as record_file:
                record_file.write(run_result_current)
        else:
            record_file_path = TEST_RECORDS_DIRECTORY + os.path.basename(cli_execute_path) + ".txt"
            with open(record_file_path, "r") as record_file:
                run_result_expected = "".join(record_file.readlines())
                run_result_expected = run_result_expected.encode().decode("unicode_escape")

            if run_result_current != run_result_expected:
                # If no same result.

                # Print.
                print(f"[Test][Failed] File {cli_execute_path} expected result {run_result_expected}, but got {run_result_current}!")
        # Clean after.
        if CLEAR_AFTER and RUN_OTHER:
            os.remove(cli_execute_path + ".dot")
            os.remove(cli_execute_path + ".py")

# Run MyPy on the core.
if MYPY_RUN:
    mypy_results = cli_execute(["mypy", LANG_PATH])
    mypy_results = str(mypy_results.stdout.decode("utf-8"))
    if not mypy_results.startswith("Success"):
        print(f"[MyPy][Failed]:\n {mypy_results}")
    else:
        print(f"[MyPy][OK]!")
    if CLEAR_AFTER:
        os.remove(".mypy_cache")
else:
    print(f"[MyPy][Disabled]!")

# Messages.
if RECORD_NEW:
    print("[Test][Records] Test records new recorded OK!")
if CLEAR_AFTER:
    print("[Test][Junk][Cleared]!")

# Print time taken.
test_time_taken = int(time.time() - test_start_time)
print(f"[Test] End! Time taken: {test_time_taken}s")

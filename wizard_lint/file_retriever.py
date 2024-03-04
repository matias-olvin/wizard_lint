import argparse
from typing import List


def obtain_args() -> List[str]:
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Process two files or directories.")

    # Add positional arguments for the paths
    parser.add_argument(
        "file", metavar="file", type=str, help="Give folder/specific path to SQL file"
    )
    parser.add_argument("config", metavar="config", type=str, help="Path to config")

    # Parse the arguments
    args = parser.parse_args()

    # Print the provided paths
    print("File path provided by the user:", args.file)
    print("config.yaml path provided by the user:", args.config)

    return [args.file, args.config]

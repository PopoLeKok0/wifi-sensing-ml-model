import sys
import yaml
import argparse
import importlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"

def load_yaml(filename):
    """Load a YAML configuration file."""

    filepath = CONFIG_DIR / filename

    if not filepath.is_file():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    with filepath.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}

# Load configuration files
config = load_yaml("config.yaml")
model_config = load_yaml("models.yaml")
test_config = load_yaml("tests.yaml")

# Extract configuration
settings = config.get("program", {})
paths = config.get("paths", {})
execution = config.get("execution", {})

models = model_config.get("models", {})
tests = test_config.get("tests", {})

default_model = settings.get("default_model", "1")
default_test = settings.get("default_test", "1")

MODEL_DIR = BASE_DIR / paths.get("model_directory", "models")

# Display available options
def display_options(options, title):

    print(f"\nAvailable {title}:")

    for key, item in options.items():
        print(f"  {key:<10} {item['name']:<20} {item['description']}")

    print("Type 'help' to display options.")
    print("Ctrl+D to exit.")

# Execute selected model
def execute_model(model_id, test_id, filename):

    model = models[model_id]
    test = tests[test_id]

    module_name = model["module"]

    print("\nExecuting:")
    print(f"Model: {model['name']}")
    print(f"Test:  {test['name']}")
    print(f"Data:  {filename}")

    # Add model directory to Python module search path
    if str(MODEL_DIR) not in sys.path:
        sys.path.insert(0, str(MODEL_DIR))

    # Import selected model
    module = importlib.import_module(module_name)

    # Execute model
    # Each model module must implement a run() function.
    module.run(
        data_file=filename,
        test_config=test
    )

    print("\nFinished")


# Main program
def main():

    print(settings.get("name", "Program Start"))

    state = "model"

    selected_model = None
    selected_test = None
    selected_filename = None

    while True:

        try:
            # Select model
            if state == "model":

                choice = input(
                    f"\nEnter your model ID [{default_model}]: "
                ).strip()

                if not choice:
                    choice = default_model

                if choice in ("help", "-h", "--help"):
                    display_options(models, "models")
                    continue

                if choice not in models:
                    print("Invalid model. Type 'help' for options.")
                    continue

                selected_model = choice
                state = "data"

            # Select data file
            elif state == "data":

                filename = input("\nEnter filename/path: ").strip()

                if not filename:
                    print("Filename cannot be empty.")
                    continue

                selected_filename = Path(filename).expanduser()

                if not selected_filename.is_absolute():
                    selected_filename = (
                        BASE_DIR / selected_filename
                    )

                selected_filename = selected_filename.resolve()

                if execution.get("validate_input_file", True):

                    if not selected_filename.is_file():
                        print(
                            "File does not exist or is not a regular file: "
                            f"{selected_filename}"
                        )
                        continue

                state = "test"

            # Select test
            elif state == "test":

                choice = input(
                    f"\nEnter your test ID [{default_test}]: "
                ).strip()

                if not choice:
                    choice = default_test

                if choice in ("help", "-h", "--help"):
                    display_options(tests, "tests")
                    continue

                if choice not in tests:
                    print("Invalid test. Type 'help' for options.")
                    continue

                selected_test = choice
                state = "execute"

            # Execute selected model and test
            elif state == "execute":

                execute_model(
                    model_id=selected_model,
                    test_id=selected_test,
                    filename=selected_filename
                )

                # Reset selections
                selected_model = None
                selected_test = None
                selected_filename = None

                state = "model"

        except EOFError:
            break

        except KeyboardInterrupt:
            print("\nExecution interrupted.")
            break

        except Exception as error:
            print(f"\nExecution error: {error}")

            # Return to model selection
            selected_model = None
            selected_test = None
            selected_filename = None

            state = "model"

    print("\nProgram Finished")


# Program entry point

if __name__ == "__main__":
    main()
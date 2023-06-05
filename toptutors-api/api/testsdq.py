import sys
import os

# Get the directory path of the models directory
models_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', 'models'))

# Add the directory path to the Python path
sys.path.append(models_directory)

print(models_directory)
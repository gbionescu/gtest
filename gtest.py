import argparse
import importlib
import gtest.task as task


parser = argparse.ArgumentParser(description='Run parallel testing.')
parser.add_argument('--file', type=str, help='file to test')

args = parser.parse_args()

to_load = args.file.replace("/", ".").replace(".py", "")
importlib.import_module(to_load)

task.run_tasks()
import os
import emod_malaria.bootstrap as emod_malaria

current_directory = os.path.dirname(os.path.realpath(__file__))

failed_tests = os.path.join(current_directory, "failed_tests")

executables_dir = os.path.join(current_directory, "executables")
schema_path = os.path.join(executables_dir, "schema.json")
schema_file = schema_path  # alias kept for emodpy_malaria internals
eradication_path = os.path.join(executables_dir, "Eradication")

if not os.path.isdir(executables_dir):
    os.mkdir(executables_dir)

if not os.path.isfile(eradication_path):
    emod_malaria.setup(executables_dir)

container_platform_name = "Container"
plat_image = "ghcr.io/emod-hub/emod-ubuntu-runtime:latest"
job_dir = "tutorial_output"  # relative — resolves inside each test's working directory

x_Base_Population_scale = 0.5  # run tutorial tests at half population for speed
n_calibration_samples = 3
n_calibration_iterations = 2
burnin_serialize_years = 5

import os

# Directory containing this manifest file (i.e., the tutorials/ directory)
tutorials_dir = os.path.dirname(__file__)

# === Executables ===
# The bootstrap step (run once at the bottom of each tutorial script) downloads
# the EMOD executable and schema file into this directory.
executables_dir = os.path.join(tutorials_dir, "executables")
schema_path = os.path.join(executables_dir, "schema.json")
schema_file = schema_path  # alias for emodpy_malaria internals
eradication_path = os.path.join(executables_dir, "Eradication")

# === Assets ===
# idmtools uploads files found here as experiment-level assets.
assets_input_dir = "Assets"

# === Container Platform ===
# Docker image used when running simulations locally or in Codespaces.
plat_image = "ghcr.io/emod-hub/emod-ubuntu-runtime:latest"
job_dir = os.path.join(tutorials_dir, "tutorial_output")

# === Scaling ===
# Set to < 1.0 in tests/manifest.py to speed up test runs.
x_Base_Population_scale = 1.0
n_calibration_samples = 10
n_calibration_iterations = 5
burnin_serialize_years = 50

# === COMPS Platform ===
# Path to a file containing the COMPS SIF AssetCollection ID.
# Only needed if using the COMPS platform.
comps_sif_path = os.path.join(tutorials_dir, "comps_sif_file.id")

# === SLURM Platform ===
# Full path to the Singularity Image File on your SLURM cluster.
# Only needed if using the SLURM_LOCAL platform.
slurm_sif_path = "/path/to/emod-malaria.sif"   # UPDATE for your cluster

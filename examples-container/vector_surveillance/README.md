## Demonstrates how to run simulations with vector genetics in the container platform or COMPS platform

### Prerequisites:
- Install docker when running in container platform
- Create a virtual environment
- Activate the virtual environment
- Install emodpy-malaria and dependencies
- Install idmtools_platform_container and dependencies
  ```pip install -r requirements_container.txt```
- Check pip installation with pip list
- 
### Run example in COMPS:
  - ```python example_comps.py```

### Run example in local with container platform: 
 - ```python example_container.py```
- View running status:
  - idmtools container status <experiment_id>
- View the output in the local job directory which you can find in console output while running the example_container.py
- Optionally view the same output in the Docker container:
  - User can find container ID from console output and use the following command to view the output:
  ```bash
      docker exec -it <container_id> bash
      cd /home/container-data/<suite_dir>/<experiment_dir>/<simulation_dir>
  ```
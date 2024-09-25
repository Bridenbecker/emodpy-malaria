## Demonstrates how to create burnin serialized population file and consume it in the container platform or COMPS platform

### Prerequisites:
- Install docker when running in container platform
- Create a virtual environment
- Activate the virtual environment
- Install emodpy-malaria and dependencies
- Install idmtools_platform_container and dependencies
  ```pip install -r requirements_container.txt```
- Check pip installation with pip list
- 
### Example running burnin in COMPS:
- Run burnin case in COMPS:
  - Edit the params.py to set burnin_type=True 
  - ```python example_comps.py```
- Run use burnin from above run result:
  - Edit the params.py to set burnin_type=False
  - copy the burnin experiment id from the above run result to example_comps.py:         
     burnin_exp_id = "744da7b5-d26f-ef11-aa17-9440c9be2c51"
  - ```python example_comps.py```
### Example running burnin in Docker container:
  - Run burnin case in local Docker container:
    - Edit the params.py to set burnin_type=True 
    - ```python example_container.py```
  - Run use burnin from above run result:
    - Edit the params.py to set burnin_type=False
    - copy the burnin experiment id from the above run result to example_container.py:         
       burnin_exp_id = "ab405cf1-0a4e-44d5-b2ba-54242ddfc69d"
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
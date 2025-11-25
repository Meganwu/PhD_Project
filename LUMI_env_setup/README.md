## Environment setup on LUMI

**Note**: Python packages are installed with LUMI container wrapper, see https://docs.lumi-supercomputer.eu/software/installing/container-wrapper/

### Build container

1. Enter the project directory `/project/project_<id>`

2. Create (or update) `requirements.txt` file with the required dependencies for the project

3. Load modules
    ```
    module load LUMI 
    module load lumi-container-wrapper
    ```
4. Build the container
    ```
    pip-containerize new --prefix <install_dir> requirements.txt
    ```

### Run with the container
To use the container environment you need to export its binary:
```
export PATH="/project/project_<id>/<install_dir>/bin:$PATH"
```
You can export the container in the batch job script in the same way.

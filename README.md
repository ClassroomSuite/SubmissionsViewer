# Submissions viewer
View grades and submissions from students in realtime
## Steps
1. Install [Anaconda](https://www.anaconda.com/products/individual)
2. Clone repo
    ```
    git clone https://github.com/ClassroomSuite/SubmissionsViewer.git
    cd SubmissionsViewer
    ```
3. Create conda environment
    ```
    conda env create -f=environment.yml
    ```
4. Activate conda environment
    ```
    conda activate submissions_viewer
    ```
5. Open Jupyter
    ```
   jupyter notebook
   ```
6. Install package
    ```
    python -m pip install --upgrade -e .
    ```
7. Open [submissions_viewer.ipynb](submissions_viewer.ipynb) in Jupyter
8. Go to Kernel and select Restart & Run All

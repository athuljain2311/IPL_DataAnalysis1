![IPL Logo](https://www.iplt20.com/assets/images/ipl-og-image-new.jpg)
# IPL Data Analysis

* All the data used for this project has been scraped from [IPL's official website](https://www.iplt20.com/).
* The raw scraped data, along with the processed, clean data, that has been used for all the analysis can be found [here](https://www.kaggle.com/datasets/athuljain/ipl-data-all-time) in my Kaggle account.

## Steps to run the application

1. Clone the repository by running the command `git clone https://github.com/athuljain2311/IPL_DataAnalysis1.git`
2. Assuming that you have Anaconda distribution installed in your system, run the command `conda create -p venv python=3.7 -y` within the repository, to create a virtual environment within the repository. I have used __Python 3.7__ for building this project.
3. Activate the environment by running the command `conda activate venv`
4. After activating the environment, run the command `pip install -r requirements.txt` to install all the dependencies
5. Finally, run the command `streamlit run app.py` to launch the web application.

## Understanding the code

* Based on the structure of the application, the code to generate the graphs present in each of the four tabs in the application, have been split up into 4 different modules in the `src/components` directory.
* `app.py` houses the entire structure of the web application.
* The notebook based on which the modules have been developed, has been included in the `data` directory.

# Graphical user interface for zeeman 

### Installing the repository
* click on the green code button and copy the URL from there
* run the following command ```git clone https://github.com/EK023/GUI_for_ZEEMAN.git```
* if you don't have git: [tutorial for git installation](https://git-scm.com/install/)


### Setup

* First copy all the necessary files to run the Zeeman into Zeeman folder.
Also add the necessary format files that are need for zeeman_python.py
zmodel_format.dat, inlmam_format.dat, elementdic.dat (all of these go into Zeeman folder)
(didn't add those yet because not sure if I have the right to distribute these)

* Before running the code, open zeeman_python.py and insert your lmau-zuc file into the 9th row```LMAU_ZUC_FILE=""```

* If you forget to add it and run the program then please close it and then change the previous value.
* At the moment zeeman_python.py runs in the terminal where you started the GUI and its results are also shown there. While it runs the GUI is not operatable and you need to wait till the zeeman_python.py finishes its job.

### Running the code 

Using standard Python

* Install all the required dependencies:
```pip install -r requirements.txt```

* Navigate to the folder where the code was installed and run it from the terminal
```python3 GUI_zeeman.py```
* Also you can run it from anywhere so following command works as well
```python3 <path_to_GUI_zeeman.py>```

Using anaconda (Conda)

* Create the environment from the file
```conda env create -f environment.yml```
* Activate the environment 
```conda activate zeeman_gui```
* Run the app
```python GUI_zeeman.py```
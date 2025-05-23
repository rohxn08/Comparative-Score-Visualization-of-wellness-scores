Comparative Score Visualization

This project aims to  visualize the comparative scores of users over time using plotly library in python.

Features:
1. Has both collected data and generated data.
2. Uses plotly to plot both the types of data based on the  file chosen for execution.
3. Has a user-friendly interface where the users can easily identify the trends in the data.
4. Has dynamic features where users can hover over te plot to get the exact trends of each user.
5. Has a legend where users are identfied with seperate colors respectively.
6. Both the outputs of the file can be viewed on a webpage. In order to view a preview of the webpage install live server and liver preview extensions from the VScode.

Structure of the project
1. The file : wellness_visualization.py is used to generate the data and plot the data.
2. The file : wellness_visualization_collected.py is used to plot the collected data (makes use of existing data present in the Datasets folder. Datasets used are activity, sleep and weight data).

Installation

1. Cloning the Repository:
```bash
git clone https://github.com/rohxn08/Comparative-Score-Visualization-of-wellness-scores.git
cd Comparative-Score-Visualization-of-wellness-scores
```
2. Installing the required packages:
```bash 
pip install -r requirements.txt
```
 
3. Executing the files:
> To execute the file with dummy data:
```bash
python wellness_visualization.py
```
> To execute the file with collected data:
```bash
python wellness_visualization_collected.py
```



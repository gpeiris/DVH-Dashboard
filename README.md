# DVH-Dashboard
This is a data visualisation tool for my PhD project. It will show the DVH for a selected Target and Organ at Risk to compare MLC leaf width performance.
The code is built and modified from a tutorial code provided by [Statworx](https://github.com/STATWORX/blog/blob/master/DashApp/app.py). 

## Context
Radiotherapy (RT) is an important tool to alleviate the stress on a cancer care system, especially in Low and Middle Income Countries (LMICs). Unfortunately, in these nations, a RT Linear Accelerator (LINAC), which is used to deliver radiation for cancer control, breaks down far more frequently and stays broken down for longer than in High Income Countries. It is projectected that 75% of cancer related deaths will occur in LMICs and the lack of reliable and robust machinery will only compund this.
One component that is known to be unreliable is called the Multi-Leaf Collimator. This component shapes the x-ray radiation used for treatment by moving tungsten "leaves" in and out of the beam, blocking radiation that would go on to hit healthy cells. Over the years, this component has had its leaves become higher in number and narrower in thickness. If we can reduce the total number of leaves by increases the thickness of the leaves, we should in theory make the leaves more reliable. However, will this come at the expense of treatment plan quality?

This code will show the average Dose-Volume Histogram (DVH) for 5 common cancers in LMICs and the standard deviation as a chaded region surrounding it. The top plot will show the DVH for the tumour and the bottom plot will show the DVH for the Organs At Risk (OAR).

## Requirements
For this code to work, you will need to provide a .csv file matching the format of the template provided. All volumes are provided in [%] and doses for OAR are in [Gy].
Python packages used are dash, plotly, pandas and numpy, listed in requirements.txt .

The folder assests contains a style sheet provided by statworx. Dash will automatically load .css files placed in a folder named "assets".

## How It Works
Run the file app.py and open the development server address printed in the terminal. The left-hand side will have three dropdown menus. Select one or anatomical sites to display on the graphs on the right-hand side. You can also isolate via specific Target type for the top plot and specific Organ At Risk for the bottom plot.

The right-hand side displays the resulting graphs. On top is the DVH for the tumour volumes and on the bottom is the DVH for OAR. To zoom into the graph, simply click and hold the leftmost point for the minimum x value and drag to the maximum x value of your choice. To unzoom, double click or select a new option from the dropdown menu.

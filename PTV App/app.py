import dash
from dash import dcc
from dash import html
from pandas.io.formats import style
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

df  = pd.read_csv("data/DVHPatientFile.csv")
dfO = pd.read_csv("data/OARMetricComp.csv")
leavesArray = ['UoM2.5mm','UoM5mm','UoM10mm']
X       = [1,2,10,20,30,40,50,60,70,80,90,95,98,99,100,101,102,105,107,110,113,115,117,120,123,125,127,130,133,135,137,140,143,145,147,150,153,155]
Y       = np.linspace(5,60,12)
DVH_arr = ['PTV','CTV','GTV','iGTV']
elms = {'Prostate':12,'Lung':10,'Liver':9,'Colorectal':10,'Cervical':10}
#xLabelArray = ['Dose [%]','Dose [%]','Conformity Index','Average Leaf Pair Opening [mm]','MU per Gy [MU/Gy]', 'Homogeneity Index']

# Initialise the app
app = dash.Dash(__name__)

# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_leaf):
        dict_list = []
        for i in list_leaf:
                dict_list.append({'label':i, 'value':i})
        return dict_list

# Define the app
app.layout = html.Div(children=[
	html.Div(className='row', # define the row element
		children=[
			html.Div(className='three columns div-user-controls',
				children=[
					html.H2('Leaf Width Impact on Dose Distribution'),
					html.P('''Pick one or more anatomical site to display'''),
					html.Div(className='div-for-dropdown',
						children=[
							dcc.Dropdown(id='siteselector',
								options=get_options(df['Site'].unique()),
								placeholder="Select an anatomical site",
                                multi=True,
								value=[df['Site'].sort_values()[0]],
								style={'backgroundColor':'#1E1E1E'},
								className='siteselector'
							)
						],
					style={'color':'#1E1E1E'}
					),
                    html.P('''Pick one target to view'''),
                    html.Div(className='div-for-dropdown',
						children=[
							dcc.Dropdown(id='dvhselector',
								options=[],
                                placeholder="Select an anatomical site first",
								multi=False,
								value=DVH_arr[0],
								style={'backgroundColor':'#1E1E1E'},
								className='dvhselector'
							),
						],
					style={'color':'#1E1E1E'}
					),
					html.P('''Pick one or more OAR to view'''),
                    html.Div(className='div-for-dropdown',
						children=[
							dcc.Dropdown(id='oarselector',
								options=[],
								placeholder='Select an anatomical site first',
								multi=False,
								value='Bladder',
								style={'backgroundColor': '#1E1E1E'},
								className='oarselector'
							)

						],
					style={'color':'#1E1E1E'}
					),
				]
			), # Define the left element
			html.Div(className='nine columns div-for-charts bg-grey',
				children=[
					dcc.Graph(id='25mm',
						config={'displayModeBar':False},
						animate=True
					),
                    dcc.Graph(id='volumePlot',
                         config={'displayModeBar':False},
						animate=True
                                        ),
				]
			), # Define the 2.5mm Box Plot 
		]
	)
])

@app.callback(
    Output('oarselector', 'options'),
    Input('siteselector', 'value')
)
def update_oar_options(selected_site):
    oars = dfO[dfO['Site'] == selected_site[0]]['OAR'].unique()
    oar_options = [{'label': oar, 'value': oar} for oar in oars]
    return oar_options

@app.callback(
    Output('dvhselector', 'options'),
    Input('siteselector', 'value')
)
def update_dvh_options(selected_site):
    dvh = df[df['Site'] == selected_site[0]]['Target'].unique()
    dvh_options = [{'label': dvh, 'value': dvh} for dvh in dvh]
    return dvh_options

@app.callback(Output('25mm','figure'),
			[Input('siteselector','value'),
            Input('dvhselector','value')
			]
)
def update_25mm(site_dropdown_val, dose_met):
	trace = []
	for site in site_dropdown_val:
		df_sub = pd.DataFrame([np.zeros(41)],
							  columns=['PlanID', 'Target', 'Site', 'V155', 'V153', 'V150', 'V147', 'V145', 'V143',
									   'V140', 'V137', 'V135', 'V133', 'V130', 'V127', 'V125', 'V123', 'V120', 'V117',
									   'V115', 'V113', 'V110', 'V107', 'V105', 'V102', 'V101', 'V100', 'V99', 'V98',
									   'V95', 'V90', 'V80', 'V70', 'V60', 'V50', 'V40', 'V30', 'V20', 'V10', 'V2',
									   'V1'])

		df_sub = df_sub.append(df[df['Site'] == site])
		for leaf in leavesArray:
			# Calculate means
			means = df_sub[(df_sub['PlanID'] == leaf) & (df_sub['Target'] == dose_met)].mean()
			# Calculate std
			stds = df_sub[(df_sub['PlanID'] == leaf) & (df_sub['Target'] == dose_met)].std() / np.sqrt(elms[site])
			trace_mean = go.Scatter(x=X[::-1],
									y=means,
									mode='lines',
									showlegend=False
			)
			trace_std = go.Scatter(x=np.concatenate([X[::-1], X]),
								   y=np.concatenate([means - stds, (means + stds)[::-1]]),
								   fill='toself',
								   name = site[0:2] + '-' + leaf.split('UoM')[1]
			)
			trace.append(trace_mean)
			trace.append(trace_std)
		traces = [trace]
	data = [val for sublist in traces for val in sublist]
	figure={'data':data,
			'layout':go.Layout(
				colorway=[],
				template='plotly_dark',
				paper_bgcolor='rgba(0,0,0,0)',
				plot_bgcolor='rgba(0,0,0,0)',
				margin={'b':15},
				hovermode='x',
				#autosize=True,
				title={'text': 'DVH for '+site_dropdown_val[0]+' '+dose_met+' per Leaf Width','font':{'color':'white'},'x':0.5},
				yaxis={'title': 'Volume [%]', 'range':[0,100]},
                xaxis={'title': 'Dose [%]','range':[0,155]},
	),
	}
	return figure

@app.callback(Output('volumePlot','figure'),
			[Input('siteselector','value'),
            Input('oarselector','value')
			]
)
def update_volumePlot(site_dropdown_val, oar_met):
	trace = []
	for site in site_dropdown_val:
		df_sub = pd.DataFrame([np.zeros(15)],
							  columns=['PlanID','Site','OAR','V60Gy','V55Gy','V50Gy','V45Gy','V40Gy','V35Gy','V30Gy',
									   'V25Gy','V20Gy','V15Gy','V10Gy','V5Gy'])

		df_sub = df_sub.append(dfO[dfO['Site'] == site])
		for leaf in leavesArray:
			# Calculate means
			means = df_sub[(df_sub['PlanID'] == leaf) & (df_sub['OAR'] == oar_met)].mean()
			# Calculate std
			stds = df_sub[(df_sub['PlanID'] == leaf) & (df_sub['OAR'] == oar_met)].std() / np.sqrt(elms[site])
			trace_mean = go.Scatter(x=Y[::-1],
									y=means,
									mode='lines',
								    showlegend = False
			)
			trace_std = go.Scatter(x=np.concatenate([Y[::-1], Y]),
								   y=np.concatenate([means - stds, (means + stds)[::-1]]),
								   fill='toself',
								   name=site[0:2] + '-' + leaf.split('UoM')[1]
			)
			trace.append(trace_mean)
			trace.append(trace_std)
		traces = [trace]
	data = [val for sublist in traces for val in sublist]
	figure={'data':data,
			'layout':go.Layout(
				colorway=[],
				template='plotly_dark',
				paper_bgcolor='rgba(0,0,0,0)',
				plot_bgcolor='rgba(0,0,0,0)',
				margin={'b':15},
				hovermode='x',
				#autosize=True,
				title={'text': 'DVH for '+site_dropdown_val[0]+' '+oar_met+' per Leaf Width','font':{'color':'white'},'x':0.5},
				yaxis={'title': 'Volume [%]', 'range':[0,100]},
                xaxis={'title': 'Dose [Gy]','range':[0,60]},
	),
	}
	return figure

if __name__ == "__main__":
    app.run_server()

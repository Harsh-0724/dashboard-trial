import dash
from dash import Dash, html,dash_table,dcc,Input,Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")

external_stylesheets = [
    'https://code.getmdl.io/1.3.0/material.indigo-pink.min.css'
]

app = Dash(external_stylesheets=external_stylesheets)


app.layout = [
    
    html.H1('Gapminder Dashboard', style = {
        'textAlign':'center',
        'color' : "darkblue",
        'padding' : '20px'
    }),
    html.Div([
        html.H3("Data Table",style = {'textAlign':'center'}),
        dash_table.DataTable(data = df.to_dict('records'),page_size=10,
        style_table={'overflowY':'auto','height':'400px'},
        style_cell={'textAlign':'left','padding':'5px','minWidth':'100px'})
    ],style = {'width':'48%','display':'inline-block','verticalAlign':'top','paddng':'10px'}),

    html.Div([
        html.Label('Select Year:',style={'fontWeight':'bold'}),
                dcc.Dropdown(options=[{'label':year,'value':year} for year in df['year']],
                             id='year3',
                             value=1952,
                             clearable=False
                ),
        dcc.Graph(id='pi')
],style = {'width':'48%','display':'inline-block','verticalAlign':'top','paddng':'10px'}),

    

    html.Div([
        html.Div([
            html.Label('Select Metric:', style={'fontWeight':'bold'}),
            dcc.RadioItems(
                options=['pop','lifeExp','gdpPercap'],
                value='lifeExp',
                id='Parameter',
                inline = True,
                style={'marginTop':'10px'}
                ),
                html.Label('Select Country:',style={'fontWeight':'bold'}),
                dcc.Dropdown(options=[{'label':country,'value':country} for country in df['country'].unique()],
                             id='dropdown',
                             value='India',
                             clearable=False
                ),
        ],style={'marginTop':'20px'}),
    ]),
    dcc.Graph(id='line_graph'),

    html.Div([
            html.Div([
            html.Label('Select Metric:', style={'fontWeight':'bold'}),
            dcc.RadioItems(
                options=['pop','lifeExp','gdpPercap'],
                value='lifeExp',
                id='Parameter2',
                inline = True,
                style={'marginBottom':'10px'}
                ),
                html.Label('Select Year:',style={'fontWeight':'bold'}),
                dcc.Dropdown(options=[{'label':year,'value':year} for year in df['year']],
                             id='year',
                             value=1952,
                             clearable=False
                ),
        ],style={'marginBottom':'20px'}),
        
        dcc.Graph(id='hist')
    ],style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    html.Div([
        html.Label('Select Year:',style={'fontWeight':'bold'}),
                dcc.Dropdown(options=[{'label':year,'value':year} for year in df['year']],
                             id='year2',
                             value=1952,
                             clearable=False
                ),
        
       
        dcc.Graph(id='sc')
    ])   
]

@app.callback(
        [
        Output('line_graph','figure'),
        Output('hist','figure'),
        Output('sc','figure'),
        Output('pi','figure')
        ],
        [
            Input('dropdown','value'),
            Input('Parameter','value'),
            Input('Parameter2','value'),
            Input('year','value'),
            Input('year2','value'),
            Input('year3','value')

        ]
)

#callback automatically inputs selected values in dropdown and options into the updated_graph function.

def updated_graph(selected_country,selected_metric,selected_metric2,selected_year,selected_year2,selected_year3):
    filtered_df = df[df['country'] == selected_country]
    fig = px.line(filtered_df,x='year',y=selected_metric,title = f'{selected_metric} in {selected_country} over time')

    filtered_df2 = df[df['year'] == selected_year]
    fig2 = px.histogram(filtered_df2,x='country',y=selected_metric2,title = f'{selected_metric2} in {selected_year} for different countries')

    filtered_df3 = df[df['year'] == selected_year2]
    fig3 = px.scatter(filtered_df3,x='gdpPercap',y='lifeExp',size='pop',color='continent',hover_name='country',log_x=True,size_max=60,title = f'Displaying the comparison of all parameters of all countries for the year {selected_year2}') 

    filtered_df4 = df[df['year'] == selected_year3]
    fig4 = px.pie(filtered_df4, names='continent', values='pop',title=f'Population by Continent in {selected_year3}')

    


    return fig,fig2,fig3,fig4

#filtered_df = df[df['country'] == selected_country], this is filtering syntax, it is a boolean condition and returns True only for selected country.

if __name__ == '__main__':
    app.run(debug=True)
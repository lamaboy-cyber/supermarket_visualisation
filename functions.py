import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from classes import Supermarket, Customer

sections_all = ['gone','checkout', 'dairy', 'drinks',  'spices', 'fruit', 'entry']
weekdays = ['monday','tuesday','wednesday','thursday','friday']
df_list = []
visited = []


def first_section(x):

    if x not in visited:
        visited.append(x)
        return 1
    else:
        return 0 


def merge_csvs():

    """"combines the single csvs for each weekday to one csv"""

    for i in weekdays:
        df_list.append(pd.read_csv('data/'+i+'.csv', delimiter =';'))

    df = pd.concat(df_list).reset_index()
    return df


def add_time_features(df):

    """adds features for weekday, hour of day, minute of hour and minute of day."""

    df['weekday'] = df["timestamp"].apply(lambda x: pd.to_datetime(x).weekday()) 
    df['hour'] = df["timestamp"].apply(lambda x: pd.to_datetime(x).hour)
    df['minute'] = df["timestamp"].apply(lambda x: pd.to_datetime(x).minute)
    df['abs_minute'] = df['minute'] + 60 * df['hour']    
    return df


def add_unique_customer_no(df):

    """customer numbers get changed to a unique number for each customer."""

    df['customer_no'] = df['customer_no'] + 10000 * df['weekday'] 
    return df


def add_first_section_feature(df):

    """checks the first section each customer visited"""

    df['first_section'] = df['customer_no'].apply(first_section)  
    return df


def section_to_int(section):

    """"returns an integer for each section. used for plotting"""

    for i, s in enumerate(sections_all):
        if section == s:
            return i


def simulate_supermarket():

    num_cust = 150
    steps = 50
    step_count = []

    s=Supermarket(num_cust)
    s.add_customers()

    x = np.random.random_sample(num_cust)
    y = np.random.random_sample(num_cust)
    color = np.random.random_sample(num_cust)




    for i in range(steps):
        current_states = []
        current_states_count = []
        customer_names = []
        customer_time = []
        customer_values = []
        paid = []
        
        
        if i != 0:
            s.next_minute()

        for customer in s.customers:
            current_states.append(customer.state)
            customer_names.append(customer.name)
            customer_time.append(customer.time)
            customer_values.append(round(customer.value,2))
            step_count.append(i)
            if customer.state == 'checkout':
                paid.append(customer.value)
            else: paid.append(0)
            

        df_current = pd.DataFrame(current_states, customer_names)
        df_current['time'] = customer_time
        df_current['value'] = customer_values
        df_current['sales'] = paid
        df_current['x'] = x
        df_current['y'] = y
        df_current['color'] = color
        
        if i == 0:
            df_steps = df_current
        else:
            df_steps = df_steps.append(df_current)
            
    df_steps['value_plot'] = df_steps['value'] +5
    df_steps['step'] = step_count
    df_steps = df_steps.reset_index()
    df_steps['section_int'] = df_steps[0].apply(section_to_int)
    df_steps = df_steps.sort_values(['time','index'])
    df_steps['sales_sum'] = df_steps['sales'].cumsum()

    return df_steps


def plot(df): 

    fig = px.scatter(df, x = 'x',  y= 'section_int', width = 900, height = 600,
                color = 'y', size = 'value_plot',
            animation_frame = 'time', animation_group = 'index',
                range_y = (-.9,7), range_x = (-.2,1.1), range_color = (-.5,1),
                opacity = .9, template = 'plotly_dark', text="value")

    fig.update_traces(textposition='top center')

    for i, section in enumerate(sections_all):
        fig.add_trace(go.Scatter(
            x=[.5],
            y=[i +.0],
            mode="text",
            name="Lines and Text",
            text= (section.upper()) + 18 * '       -'))
        
        
    fig.update_layout({'xaxis': {'zeroline': False,'showgrid': False, 'visible': False},
                    'yaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                    'showlegend': False,})
        
    fig.show()
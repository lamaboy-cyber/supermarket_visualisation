import pandas as pd
import numpy as np

sections = ['checkout', 'dairy', 'drinks', 'fruit', 'spices']

def get_transition_probs(df):
    
    "returns the probabability of a random customer moving from section a to section b"

    df_transitions = pd.DataFrame()

    for i in df['customer_no'].unique():
        transition = df[(df['customer_no'] == i)][['location']]
        transition['location_after'] = transition['location'].shift(-1)
        transition.dropna(inplace=True)
        transition['customer_no'] = i
        df_transitions = df_transitions.append(transition)

    transition_probs = pd.crosstab(df_transitions['location_after'], df_transitions['location'], normalize=1)
    
    return transition_probs

def get_initial_probs(df):

    "returns probabilities for the first section a customer visits"

    customer_count = df[(df['first_section'] == 1)]['location'].count()
    first_section_count = df[(df['first_section'] == 1)]['location'].value_counts(sort = True, ascending = True)
    initial_probs = first_section_count / customer_count
    return initial_probs




df = pd.read_csv('../data/clean.csv')
transition_probs = get_transition_probs(df)
initial_probs = get_initial_probs(df)


class Customer:
    
    """a single customer that moves through the supermarket in a MCMC simulation"""
   
    def __init__(self, name, duration):
        self.name = name
        self.state = 'entry'
        self.value = 0
        self.time = np.random.randint(duration)


    def __repr__(self):
        return f'<{self.name} time: {self.time} section: {self.state} value: {(round(self.value,2))}€>'


    def next_minute(self):
        
        self.time += 1
        
        if self.state != 'gone':
            
            if self.state == 'checkout':
                self.state = 'gone'
            elif self.state == 'entry':
                 self.state = np.random.choice([ 'drinks', 'spices', 'dairy', 'fruit'], 1, p = initial_probs)[0]
            else:
                if (np.random.choice([0,1],1,[.7,.3])) == 0:
                    self.state = self.state
                    self.value += round(np.random.randint(2000) / 100,2)
                else:
                    self.state = np.random.choice(sections ,1, p = list(transition_probs[self.state]))[0]
                    self.value += round(np.random.randint(1000) / 100,2)


class Supermarket:
    
    """place where the customers interact"""
    
    def __init__(self,num_customers, duration):
        self.num_customers = num_customers
        self.customers = []
        self.duration = duration
    
    def add_customers(self):
        for n in range(self.num_customers):
            # composition
            self.customers.append(Customer(n+1, self.duration))
    def next_minute(self):
        for customer in self.customers:
            customer.next_minute()
# Načtení dat ze souboru agenti.csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Načtení dat ze souboru agenti.csv
@st.cache_data
def load_data():
    return pd.read_csv("agenti.csv", delimiter=',')

data = load_data()
data.columns = data.columns.str.strip()  # Odstranění mezer ze jmen sloupců

# Definování skupin týmů
team_mapping = {
    'Slavia': 'Skupina A', 'Sparta': 'Skupina A',
    'Banik': 'Skupina B', 'Olomouc': 'Skupina B', 'Plzen': 'Skupina B'
}

# Přidání sloupce se skupinami týmů
data['team_group'] = data['team_short'].map(team_mapping).fillna('Skupina C')

# Výpočet procentuálního rozložení podle agenta a skupiny týmu
agent_team_counts = data.groupby(['Agent', 'team_group']).size().unstack(fill_value=0)
agent_team_percent = agent_team_counts.div(agent_team_counts.sum(axis=1), axis=0) * 100

# Seznam agentů pro výběr
agents = agent_team_percent.index.tolist()

# Titul aplikace
st.title("Procentuální rozložení hráčů podle agentů a týmů")

# Výběr agenta
selected_agent = st.selectbox("Vyberte agenta:", agents)

# Koláčový graf pro vybraného agenta
if selected_agent:
    fig, ax = plt.subplots()
    data = agent_team_percent.loc[selected_agent]
    ax.pie(
        data,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#1f77b4', '#ff7f0e', '#2ca02c']
    )
    ax.set_title(f"Procentuální rozložení hráčů agenta {selected_agent}")
    st.pyplot(fig)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Načtení dat ze souboru agenti.csv
@st.cache_data
def load_data():
    return pd.read_csv("agenti12_2024.csv", delimiter=',')

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

# Výpočet celkového počtu hráčů pro každého agenta
agent_total_counts = data['Agent'].value_counts()

# Seznam agentů pro výběr v postranním panelu
agents = agent_team_percent.index.tolist()
selected_agent = st.sidebar.radio("Vyberte agenta:", agents)

# Titul aplikace
st.title("Procentuální rozložení hráčů podle agentů a týmů")

# Koláčový graf pro vybraného agenta
if selected_agent:
    fig, ax = plt.subplots()
    data_percent = agent_team_percent.loc[selected_agent]
    ax.pie(
        data_percent,
        labels=data_percent.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#1f77b4', '#ff7f0e', '#2ca02c']
    )
    ax.set_title(f"Procentuální rozložení hráčů agenta {selected_agent}")
    st.pyplot(fig)

    # Zobrazení celkového počtu hráčů
    st.markdown(f"**Celkový počet hráčů agenta {selected_agent}:** <span style='font-size:30px; font-weight:bold;'>{agent_total_counts[selected_agent]}</span>", unsafe_allow_html=True)

# Legenda ke skupinám
st.markdown("""
### Legenda k týmovým skupinám
- **Skupina A**: Slavia, Sparta
- **Skupina B**: Banik, Olomouc, Plzen
- **Skupina C**: Ostatní kluby
""")

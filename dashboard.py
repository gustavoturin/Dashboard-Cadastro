import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Kanban Cadastro",
    page_icon=":bar_chart:",
    layout="wide"
)

def get_data_from_excel():
    file_path = r"C:\Users\gustavo.alves.RFAA\Downloads\Kanban E-mail(cadastro).xlsx"
    df = pd.read_excel(
        file_path,
        engine="openpyxl",
        sheet_name="query",
        usecols='A:Q',
        nrows=1000
    )
    return df

df = get_data_from_excel()

st.sidebar.header('Por favor, coloque seu filtro aqui:')
responsavel = st.sidebar.multiselect(
    "Selecione o responsável:",
    options=df["Responsável"].unique(),
    default=df["Responsável"].unique()
)
nucleo = st.sidebar.multiselect(
    "Selecione o Núcleo:",
    options=df["Título"].unique(),
    default=df["Título"].unique()
)
status = st.sidebar.multiselect(
    "Selecione o Status:",
    options=df["Status do Card"].unique(),
    default=df["Status do Card"].unique()
)

df_selection = df[
    (df["Responsável"].isin(responsavel)) &
    (df["Título"].isin(nucleo)) &
    (df["Status do Card"].isin(status))
]

st.title(":bar_chart: Cadastro Dashboard")

total_cards = df_selection.shape[0] 
st.subheader(f"Total de Cards: {total_cards:,}")

left_column, right_column = st.columns(2)

if len(responsavel) > 0:
    card_count = df_selection.groupby("Responsável").size().reset_index(name="Quantidade de Cards")
    fig = px.bar(
        card_count,
        x="Responsável",
        y="Quantidade de Cards",
        title="Quantidade de Cards por Responsável",
        color_discrete_sequence=["#1f77b4"] * len(card_count)
    )
    left_column.plotly_chart(fig, use_container_width=True)

status_counts = df_selection["Status do Card"].value_counts()
fig_pie = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title="Status do Card")
right_column.plotly_chart(fig_pie)

st.write(df_selection)

hide_st_style = """
            <style>
            #mainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

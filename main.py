import streamlit as st
import plotly.express as px
import pandas as pd

file_path = 'data/data.xlsx'  # исходный файл
st.set_page_config(page_title='Dashboard', layout='wide')
st.title('Анализ данных о продажах розничной компании')
st.markdown('<style>div.block-container{padding-top:1rem;}<style>', unsafe_allow_html=True)
# считывание данных в датафрейм
df = pd.read_excel(file_path)
returns_df = pd.read_excel(file_path, sheet_name='Returns')
# панель фильтрации
st.sidebar.header("Фильтрация")
# поля фильтрации
ship_mode = st.sidebar.multiselect(
    "Выберите способ доставки:",
    options=df["Ship Mode"].unique(),
)
category = st.sidebar.multiselect(
    "Выберите категорию продуктов:",
    options=df["Category"].unique(),
)
region = st.sidebar.multiselect(
    "Выберите регион:",
    options=df["Region"].unique(),
)
country = st.sidebar.multiselect(
    "Выберите страну:",
    options=df["Country"].unique(),
)
state = st.sidebar.multiselect(
    "Выберите штат:",
    options=df["State"].unique(),
)
city = st.sidebar.multiselect(
    "Выберите город:",
    options=df["City"].unique(),
)
market = st.sidebar.multiselect(
    "Выберите магазин:",
    options=df["Market"].unique(),
)
# формирование строки запроса с учетом фильтров
query_string = "("
if city:
    query_string = query_string + "City == @city and "
if ship_mode:
    query_string = query_string + "`Ship Mode` == @ship_mode and "
if country:
    query_string = query_string + "Country == @country and "
if state:
    query_string = query_string + "State == @state and "
if region:
    query_string = query_string + "Region == @region and "
if market:
    query_string = query_string + "Market == @market and "
if category:
    query_string = query_string + "Category == @category"
query_string = query_string + ")"
if query_string[-5::] == "and )":
    query_string = query_string[:len(query_string) - 5:] + ")"
# применение фильтрации
df_selection = df.query(query_string)

# Если нет фильтров, то выбрать весь датасет
if df_selection.empty:
    df_selection = df
# выбор цветовой палитры
color_palette = px.colors.sequential.RdPu
# Столбчатая диаграмма продаж по подкатегориям
container1 = st.container()
with container1:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.subheader("Продажи по категориям")
        data = df_selection.groupby(by=["Sub-Category"], as_index=False)["Sales"].sum()
        fig_sub_category_sales = px.bar(data, x="Sub-Category", y="Sales", template="plotly_white",
                                        color_discrete_sequence=[color_palette[3]],
                                        labels={"Sub-Category": "Категория товаров", "Sales": "Продажи"})
        st.plotly_chart(fig_sub_category_sales, use_container_width=True)

    with right_column:
        with st.container():
            data_style = data.style.background_gradient(cmap='RdPu')
            st.dataframe(data_style)

# Круговая диаграмма продаж по категориям
container2 = st.container()
with container2:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.subheader("Продажи по категориям")
        fig_category_country = px.pie(df_selection, values="Sales", names="Category",
                                      color_discrete_sequence=color_palette,
                                      labels={"Category": "Категория товаров", "Sales": "Продажи"})
        fig_category_country.update_traces(text=df_selection["Category"], textposition="inside")
        st.plotly_chart(fig_category_country, use_container_width=True)

    with right_column:
        with st.container():
            data_style = data.style.background_gradient(cmap='RdPu')
            st.dataframe(data_style)

# Столбчатая диаграмма продаж по регионам
container3 = st.container()
with container3:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.subheader("Продажи по регионам")
        data = df_selection.groupby(by=["Region"], as_index=False)["Sales"].sum()
        fig_region_sales = px.bar(data, x="Region", y="Sales", template="plotly_white",
                                  color_discrete_sequence=[color_palette[3]],
                                  labels={"Region": "Регион", "Sales": "Продажи"})
        st.plotly_chart(fig_region_sales, use_container_width=True)

    with right_column:
        with st.container():
            data_style = data.style.background_gradient(cmap='RdPu')
            st.dataframe(data_style)

# Столбчатая диаграмма возвратов товаров по регионам
container4 = st.container()
with container4:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        returns_df = pd.read_excel(file_path, sheet_name='Returns')
        st.subheader("Возвраты по регионам")
        df_returned = returns_df.query("(Returned == 'Yes')")
        data = df_returned.groupby(by=["Region"], as_index=False)["Returned"].count()
        fig_region_returned = px.bar(data, x="Region", y="Returned", template="plotly_white",
                                     color_discrete_sequence=[color_palette[3]],
                                     labels={"Region": "Регион", "Returned": "Количество возвратов"})
        st.plotly_chart(fig_region_returned, use_container_width=True, height=200)

    with right_column:
        data_style = data.style.background_gradient(cmap='RdPu')
        st.dataframe(data_style)

# Динамика продаж во времени
container5 = st.container()
with container5:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        df_selection["Date"] = df_selection["Order Date"].dt.to_period("M")
        st.subheader('Динамика продаж')
        linechart = pd.DataFrame(
            df_selection.groupby(df_selection["Date"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
        fig2 = px.line(linechart, x="Date", y="Sales", height=500, width=1000,
                       template="gridon", color_discrete_sequence=[color_palette[3]],
                       labels={"Date": "Дата", "Sales": "Продажи"})
        st.plotly_chart(fig2, use_container_width=True)

    with right_column:
        data_style = linechart.style.background_gradient(cmap='RdPu')
        st.dataframe(data_style)

# Динамика прибыли во времени
container6 = st.container()
with container6:
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.subheader('Динамика прибыли')
        linechart = pd.DataFrame(
            df_selection.groupby(df_selection["Date"].dt.strftime("%Y : %b"))["Profit"].sum()).reset_index()
        fig2 = px.line(linechart, x="Date", y="Profit", height=500, width=1000,
                       template="gridon", color_discrete_sequence=[color_palette[3]],
                       labels={"Date": "Дата", "Profit": "Прибыль"})
        st.plotly_chart(fig2, use_container_width=True)

    with right_column:
        data_style = linechart.style.background_gradient(cmap='RdPu')
        st.dataframe(data_style)

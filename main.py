import matplotlib.pyplot as plt
import seaborn as seaborn
import streamlit as st
import pandas as pd

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
st.title('крутой классный дашборд')
# Загрузим данные из Excel-файла
file_path = 'data/data.xlsx'
# data_load_state = st.text('Мы загружаемся!')
orders_df = pd.read_excel(file_path, sheet_name='Orders')
returns_df = pd.read_excel(file_path, sheet_name='Returns')

#
# data_load_state.text("неЗаполнение пропущенных данных")
# Заполнение пропущенных данных
# orders_df.fillna(0, inplace=True)
# orders_df.fillna(0, inplace=True)

# data_load_state.text('Цифровизация....')
# цифровизация категориальных данных
label_encoder = LabelEncoder()
orders_df['Ship Mode'] = label_encoder.fit_transform(orders_df['Ship Mode'])
orders_df['Segment'] = label_encoder.fit_transform(orders_df['Segment'])
# вот тут под вопросом
orders_df['Postal Code'] = label_encoder.fit_transform(orders_df['Postal Code'])
orders_df['City'] = label_encoder.fit_transform(orders_df['City'])
orders_df['State'] = label_encoder.fit_transform(orders_df['State'])
orders_df['Country'] = label_encoder.fit_transform(orders_df['Country'])
orders_df['Region'] = label_encoder.fit_transform(orders_df['Region'])
orders_df['Market'] = label_encoder.fit_transform(orders_df['Market'])
orders_df['Category'] = label_encoder.fit_transform(orders_df['Category'])
orders_df['Sub-Category'] = label_encoder.fit_transform(orders_df['Sub-Category'])
orders_df['Order Priority'] = label_encoder.fit_transform(orders_df['Order Priority'])

# цифровизация н категориальных данных
# # Инициализация векторизатора
# vectorizer = CountVectorizer()
# # Преобразование текста в мешок слов
# # transform each column individually
# for column in orders_df.columns:
#     orders_df[column] = vectorizer.transform([row[column] for row in orders_df])
#
#
# # Пример: преобразуем столбцы с датами в тип datetime
# orders_df['Order Date'] = pd.to_datetime(orders_df['Order Date'])
# returns_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'])

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.experimental_memo
def load_data():

    data = orders_df
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
# data_load_state.text('Мы загружаем 10 строчек')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.

#
# # Строим столбчатую диаграмму для примера (замените 'Sales' на нужный столбец)
# fig, ax = plt.subplots()
# ax.bar(orders_df['Category'], orders_df['Sales'])
# ax.set_xlabel('Категория')
# ax.set_ylabel('Продажи')
# ax.set_title('Продажи по категориям')
#
# # Отображение диаграммы в Streamlit
# st.pyplot(fig)

# График временного ряда
st.subheader('Динамика продаж во времени')
fig_time_series, ax_time_series = plt.subplots()
ax_time_series.plot(orders_df['Order Date'], orders_df['Sales'])
ax_time_series.set_xlabel('Дата заказа')
ax_time_series.set_ylabel('Продажи')
st.pyplot(fig_time_series)

# График со скользящим средним
st.subheader('Динамика продаж со скользящим средним')
fig_rolling_mean, ax_rolling_mean = plt.subplots()
ax_rolling_mean.plot(orders_df['Order Date'], orders_df['Sales'].rolling(window=7).mean(), label='Скользящее среднее')
ax_rolling_mean.set_xlabel('Дата заказа')
ax_rolling_mean.set_ylabel('Продажи')
ax_rolling_mean.legend()
st.pyplot(fig_rolling_mean)

# Сравнение категорий
st.subheader('Сравнение продаж по категориям')
fig_category_comparison, ax_category_comparison = plt.subplots()
seaborn.barplot(x='Category', y='Sales', data=orders_df, ax=ax_category_comparison)
ax_category_comparison.set_xlabel('Категория')
ax_category_comparison.set_ylabel('Продажи')
st.pyplot(fig_category_comparison)

# Ящик с усами (Boxplot)
st.subheader('Распределение продаж по категориям')
fig_boxplot, ax_boxplot = plt.subplots()
seaborn.boxplot(x='Category', y='Sales', data=orders_df, ax=ax_boxplot)
ax_boxplot.set_xlabel('Категория')
ax_boxplot.set_ylabel('Продажи')
st.pyplot(fig_boxplot)

# Тепловая карта корреляции
st.subheader('Тепловая карта корреляции')
fig_corr_heatmap, ax_corr_heatmap = plt.subplots()
corr_matrix = orders_df.corr()
seaborn.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax_corr_heatmap)
st.pyplot(fig_corr_heatmap)
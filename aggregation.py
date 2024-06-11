import os

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def aggregate_data(dt_from, dt_upto, group_type):
    # Загрузка данных из файла
    data_url = os.getenv('DATA_URL')
    data = pd.read_csv(data_url)

    # Форматирование даты
    data['date'] = pd.to_datetime(data['date'])

    # Фильтрация данных по дате
    data = data[(data['date'] >= dt_from) & (data['date'] <= dt_upto)]

    # Агрегация данных
    if group_type == 'hour':
        data['hour'] = data['date'].dt.hour
        data = data.groupby('hour')['salary'].sum().reset_index()
    elif group_type == 'day':
        data['day'] = data['date'].dt.day
        data = data.groupby('day')['salary'].sum().reset_index()
    elif group_type == 'month':
        data['month'] = data['date'].dt.month
        data = data.groupby('month')['salary'].sum().reset_index()

    # Форматирование ответа
    dataset = data['salary'].tolist()
    labels = data['hour'].tolist() if group_type == 'hour' else data['day'].tolist() if group_type == 'day' else data['month'].tolist()

    return {'dataset': dataset, 'labels': labels}
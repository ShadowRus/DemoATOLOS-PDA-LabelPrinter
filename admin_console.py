import json

import streamlit as st
import requests
import socket
import pandas as pd

from decouple import config
import os
from services.services import extract_ip


SRC_DIR = config('SRC_DIR',default='./src')
SERVER_URL = 'http://'+str(extract_ip())+':'+str(8000)
st.image(os.path.join(SRC_DIR,'Logo_cyrillic_red.png'))
####------
def upload_file(file):
    url = str(SERVER_URL+'/upload')  # Замените на URL вашего сервера
    files = {'file': file}
    headers = {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data',
    }
    response = requests.post(url, headers=headers, files=files)
    return response

###------

with st.sidebar:
    st.selectbox('Выберите действие',['Просмотр','Загрузка','Удаление'],index=1,key='action')
if st.session_state['action'] == 'Удаление':
    st.markdown('### Номенклатура', unsafe_allow_html=True)
    if st.button('Очистить БД Номенклатура'):
        re = requests.get(str(SERVER_URL + '/clear_db/goods'))
        if re.status_code == 200:
            st.success('База Номенклатуры успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')
    st.markdown('### Принтеры', unsafe_allow_html=True)
    if st.button('Очистить БД Принтеры'):
        re = requests.get(str(SERVER_URL + '/clear_db/printers'))
        if re.status_code == 200:
            st.success('База Принтеров успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')

    st.markdown('### Шаблоны', unsafe_allow_html=True)
    if st.button('Очистить БД Шаблоны этикеток'):
        re = requests.get(str(SERVER_URL + '/clear_db/label_templ'))
        if re.status_code == 200:
            st.success('База Шаблонов этикеток успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')

if st.session_state['action'] == 'Просмотр':
    st.markdown('### Номенклатура',unsafe_allow_html=True)
    re = requests.get(str(SERVER_URL+'/goods'))
    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id',inplace=True)
        df = df[['goods_name','attr_1','attr_2','id_1','id_2']]
        df = df.rename(columns={
            'goods_name': 'Наименование',
            'attr_1': 'Атрибут 1',
            'attr_2': 'Атрибут 2',
            'id_1': 'Штрихкод 1',
            'id_2': 'Штрихкод 2'
        })
        st.data_editor(df)

    st.markdown('### Принтеры',unsafe_allow_html=True)

    re = requests.get(str(SERVER_URL + '/printers'))

    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id', inplace=True)
        df = df[['print_name', 'url', 'port']]
        df = df.rename(columns={
            'print_name': 'Принтер',
            'url': 'IP4'
        })
        st.data_editor(df)

    st.markdown('### Шаблоны', unsafe_allow_html=True)

    re = requests.get(str(SERVER_URL + '/template'))

    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id', inplace=True)
        df = df[['templ_name', 'templ_data']]
        df = df.rename(columns={
            'templ_name': 'Название шаблона',
            'templ_data': 'Значение'
        })
        st.data_editor(df)



if st.session_state['action'] == 'Загрузка':
    if st.checkbox('Загрузить номенклатуру из файла', value=False):
        with open(os.path.join(SRC_DIR, 'template_goods.xlsx'), "rb") as file:
            btn = st.download_button(
                label="Загрузить шаблон для добавления",
                data=file,
                file_name="template_goods.xlsx",
                mime="excel/xlsx"
            )

        uploaded_file = st.file_uploader("Загрузите файл с номенклатурой", type=['xlsx'],
                                         help='Для формирования файла воспользуйтесь шаблоном выше')
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            # Удаление столбцов, где нет значений
            df = df.dropna(axis=1, how='all')
            # Отображение таблицы
            st.markdown('Проверьте загруженные данные')
            st.table(df)
            if st.button('Загрузить номенклатуру'):
                with open(os.path.join('./user_data', uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    f.close()
                with open(os.path.join('./user_data', uploaded_file.name), "rb") as file:
                    # Создаем словарь с файлом для отправки
                    files = {
                        "file": (uploaded_file.name, file,
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    }

                    # Выполняем POST-запрос на сервер
                    response = requests.post(str(SERVER_URL + '/upload'), headers={"accept": "application/json"},
                                             files=files)
                    f.close()

                    # Проверяем статус ответа
                if response.status_code == 200:
                    st.success("Файл успешно загружен.")
                    st.rerun()
                    os.remove(os.path.join('./user_data', uploaded_file.name))

                else:
                    st.error(f"Ошибка при загрузке файла: {response.status_code}")

    if st.checkbox('Загрузить шаблон этикетки', value=False):
        st.text_input('Название этикетки',key = 'temlate_name')
        st.text_area('Шаблон этикетки',key ='template_data')
        st.checkbox('Использовать шаблон по-умолчанию',key='is_default')
        data = {"name": st.session_state['temlate_name'], "label": st.session_state['template_data'], "is_default": int(st.session_state['is_default'])}
        if st.button('Загрузить шаблон'):
            re1 = requests.post(str(SERVER_URL + '/template'),data=json.dumps(data),headers={"accept": "application/json"})
            if re1.status_code == 200:
                st.success("Шаблон успешно загружен.")
                st.rerun()
            else:
                st.error(f"Ошибка при загрузке шаблона: {re1.status_code}")

    if st.checkbox('Добавить принтер этикеток', value=False):
        st.text_input('Наименование принтера',key = 'printer_name')
        st.text_input('Ip4 принтера',key = 'url')
        st.text_input('Port принтера', key='port',value=9100)
        st.checkbox('Использовать шаблон по-умолчанию',key='is_default_printer')
        data = {"name": st.session_state['printer_name'],
                "url": st.session_state['url'],
                'port':int(st.session_state['port']),
                'type':1,
                "is_default": int(st.session_state['is_default_printer'])}
        if st.button('Добавить принтер'):
            re1 = requests.post(str(SERVER_URL + '/printer'),data=json.dumps(data),headers={"accept": "application/json"})
            if re1.status_code == 200:
                st.success("Шаблон успешно загружен.")
                st.rerun()
            else:
                st.error(f"Ошибка при загрузке шаблона: {re1.status_code}")






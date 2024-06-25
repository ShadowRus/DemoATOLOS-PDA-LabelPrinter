import base64
import socket
from decouple import config
from services.prename import select_valid_name
from sqlalchemy.inspection import inspect
import requests


SETTIMEOUT = int(config('SETTIMEOUT',default = 2))
RESET_PRINTER = config('RESET_PRINTER',default='reset_printer')
SERIAL_NO = config('SERIAL_NO',default='serial_no')
VENDOR_MODEL = config('VENDOR_MODEL',default='printer_name')
BARCODE_KEY = config('BARCODE_KEY',default = 'B088819170283097847575868632875')
BARCODE_API_TOKEN = config('BARCODE_API_TOKEN',default='http://barcodes.olegon.ru/api/card/billing/0/')
#http://barcodes.olegon.ru/api/card/name/<ШТРИХКОД>/<КЛЮЧ>
BARCODE_API_NAME_GOODS = config('BARCODE_API_NAME_GOODS',default='http://barcodes.olegon.ru/api/card/name/')
BARCODE_API_NAME_CLASS = config('BARCODE_API_NAME_CLASS',default='http://barcodes.olegon.ru/api/card/class/')

def check_goods_server_oleg(url,token):
    re1 = requests.get(url+token)
    j1 = re1.json()
    if re1.status_code == 200:
        if j1['tries'] >= 100:
            return True
    return False

def get_goods_name_oleg(url_1,url_2,token,barcode):
    if check_goods_server_oleg(url_1,token):
        re1 = requests.get(url_2 + barcode + '/'+ token)
        if re1.status_code == 200:
            j1 = re1.json()
            return j1['names']
        else:
            return []
    else:
        return []

def get_goods_class_oleg(url_1,url_2,token,barcode):
    if check_goods_server_oleg(url_1,token):
        re1 = requests.get(url_2 + barcode + '/'+ token)
        if re1.status_code == 200:
            j1 = re1.json()
            return j1['class']
        else:
            return []
    else:
        return []

def get_goods_name(url_1,url_2,token,barcode):
    names = get_goods_name_oleg(url_1,url_2,token,barcode)
    if names != None:
        return {"agg_name": select_valid_name(names),
                "names":names}
    return {}
def is_base64(s):
    try:
        # Попробуем декодировать строку base64
        if isinstance(s, str):
            # Проверяем, возможно ли декодировать строку
            base64_bytes = base64.b64decode(s, validate=True)
            # Проверяем, что декодированная строка может быть закодирована обратно в base64 на случай, если это не текст
            return base64.b64encode(base64_bytes).decode('utf-8') == s
        return False
    except Exception:
        return False

def decode_or_return(input_str):
    # Проверка типа данных перед обработкой
    if isinstance(input_str, str) and is_base64(input_str):
        try:
            return base64.b64decode(input_str).decode('utf-8')
        except UnicodeDecodeError:
            return input_str  # Возвращать исходную строку при ошибке декодирования utf-8
    return input_str

def get_value_or_none(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def sgd_cmd(host, port, sgd):
    import socket
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mysocket.connect((host, port))
        mysocket.settimeout(SETTIMEOUT)
        mysocket.send(sgd)
        a1 = b'\x00'
        a1 = a1.decode('utf-8')
        recv = mysocket.recv(4096).decode('utf-8')
        if recv[-1] == a1:
            return recv[:-1]
        else:
            return recv
    except:
        return None
    finally:
        mysocket.close()

def get_sgd(get_value):
    s1 = f'\x1b\x1c& V1 getval "{get_value}"\r\n'
    return s1.encode()

def set_sgd(key,value):
    s1 = f'\x1b\x1c& V1 setval "{key}" "{value}"\r\n'
    return s1.encode()

def do_sgd(key):
    s1 = f'\x1b\x1c& V1 do "{key}"\r\n'
    return s1.encode()

def zpl_cmd(host, port, zpl):
    import socket
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mysocket.connect((host, port))
        mysocket.settimeout(SETTIMEOUT)
        mysocket.send(zpl.encode())
        return
    except:
        return None
    finally:
        mysocket.close()


def replace_attributes(template, attributes):
    for key, value in attributes.items():
        if key != 'id':
            template = template.replace(key, str(value))
    return template

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
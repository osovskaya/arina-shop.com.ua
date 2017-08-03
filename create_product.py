#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import parameters as p
import headers as h

host = 'arina-shop.com.ua'
admin = '/admin'

login_url = 'https://arina-shop.com.ua/admin/index.php?route=common/login'
product_url = 'https://arina-shop.com.ua/admin/index.php?route=catalog/product/insert&token='

login_parameters = MultipartEncoder(
    fields=(
        ('username', p.login),
        ('password', p.password),
    )
)

h.login_headers.update({
    'Content-Type': login_parameters.content_type,
})

login_response = requests.post(login_url, data=login_parameters, headers=h.login_headers)
# print(login_response.status_code)
# print(login_response.headers)
# print(login_response.history[0].cookies['PHPSESSID'])

try:
    token = login_response.url.split('token=')[1]
except IndexError:
    token = ''

create_product_parameters = MultipartEncoder(
    fields=p.product_parameters
)

h.product_headers.update({
    'Referer': product_url + token,
    'Content-Type': create_product_parameters.content_type,
})

product_cookie = {'PHPSESSID': login_response.history[0].cookies['PHPSESSID']}

response = requests.post(product_url + token, headers=h.product_headers, data=create_product_parameters,
                         cookies=product_cookie)
# print(response.status_code)
# print(response.headers)
# print(response.text)

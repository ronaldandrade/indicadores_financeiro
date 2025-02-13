# '''
# Get Bitcoin Value
# http://api.coindesk.com/v1/bpi/currentprice.json
# '''

# import urllib.request, json
# import streamlit as st
# def obter_valor():
# 	try:
# 		url = "https://cointradermonitor.com/api/pbb/v1/ticker"
# 		with urllib.request.urlopen(url) as url:
# 			response = url.read()
# 			data = json.loads(response)
# 			valor = float(data['last'])
# 			return valor
# 	except urllib.error.HTTPError:
# 		print('URL inexistente!')

# def exibir_valores():
# 	valor = obter_valor()
	
# 	return round(valor)
# exibir_valores()

				
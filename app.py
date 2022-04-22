from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from time import sleep
from pandas import DataFrame

#Parámetros de utilidad
url = 'https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html'
id_tabla = 'tabledatasii'
file_name = 'siidata.json'

#Ejecutar Chrome sin ventana
options = Options()
options.headless = True

#Instanciar navegador
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

#Acceder a URL y esperar a que cargue
driver.get(url)
sleep(1)

#Obtener objetos con información requerida
tabla = driver.find_element(By.ID, id_tabla)
header = tabla.find_elements(By.TAG_NAME, 'th')
filas = tabla.find_elements(By.TAG_NAME, 'tr')

#Crear objetos para información ordenada
columns = [head.text for head in header]
data = []

#Rellenar objetos con información requerida
for fila in filas:
    datos = fila.find_elements(By.TAG_NAME, 'td')
    contenido = [dato.text for dato in datos]
    if contenido != []:
        data.append(contenido)

#Se cierra el navegador ya que no será requerido
driver.quit()

#Se crea un DataFrame con pandas para crear archivo .json
DataFrame(data=data, columns=columns).to_json(path_or_buf=file_name,orient='split', index=False)
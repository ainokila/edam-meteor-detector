
<p align="center">
  <a href="https://github.com/ainokila/tfg/network/members">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/ainokila/tfg?style=for-the-badge">
  </a>
  <a href="https://github.com/ainokila/tfg/stargazers">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/ainokila/tfg?style=for-the-badge">
  </a>
  <a href="https://github.com/ainokila/tfg/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/ainokila/tfg?style=for-the-badge">
  </a>
  <a href="https://github.com/ainokila/tfg/blob/master/LICENSE.txt">
    <img alt="GitHub" src="https://img.shields.io/github/license/ainokila/tfg?style=for-the-badge">
  </a>
  <a href="https://es.linkedin.com/in/cristianvelezruiz">
    <img alt="Linkedin" src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555">
  </a>
</p>

<br>
<p align="center">
  <a href="https://github.com/ainokila">
    <img src="docs/images/logo.png" alt="Logo" width="100" height="100">
  </a>

  <h1 align="center">EDAM - Estación de Detección Automatizada de Meteoros</h1>

  <p align="center">
    EDAM es un sistema de monitorización y análisis de imagenes tomadas mediantes cámaras con el fin de detectar posibles meteoros.
  </p>
</p>

<br>

## 🦟 Introducción

El proyecto EDAM utiliza [INDI(https://indilib.org/) (Instrument Neutral Distributed Interface) para la gestión de la cámara conectada.

Cuenta con los siguientes componentes:
1. Cliente INDI.
2. Clasificador de Imágenes.
3. Controlador de Notificaciones.
4. Servidor web.

## 🦟 Requisitos
<ul>
  <li><a href="https://curl.se/download.html">curl</a></li>
  <li><a href="https://www.python.org/downloads/">Python 3.8</a></li>
</ul>

## 🦗 Instalación

La instalación de la estación esta practicamente automatizada a través del script setup.sh, este script instalará todas las dependencias de INDI y los controladores necesarios para trabajar con él.

Instalación de requisitos de INDI y los controladores:
  ```
  sudo ./setup.sh
  ```

Instalación de requisitos para python:
  ```
  pip install -r requirements 
  ```

Cuando estén correctamente instalados los requisitos anteriores, podemos proceder a la ejecución del cliente y del servidor web.

## ¿Como ejecutarlo?

### ⭐️ Ejecución del cliente de INDI

Todas las dependencias de INDI fueron instaladas a través de la ejecución del script setup, por lo que ahora ejecutaremos el cliente de INDI, que será el encargado
de mantener las comunicaciones con nuestra camara.

  ```
  indiserver -v <indi_client_name>
  ```

Por ejemplo, para una camara QHY5 debemos utilizar:

  ```
  indiserver -v indi_qhy_ccd
  ```

### 💫 Ejecución del Servidor Web

Para ejecutar el servidor web debemos instalar un WSGI, como Gunicorn o Uvicorn. En el siguiente ejemplo se toma de WSGI a Gunicorn.

1. Instalación de Gunicorn:

  ```
  pip install gunicorn
  ```

2. Ejecutar el servidor web a través de Gunicorn:
  ```
  gunicorn -w 4 --bind 0.0.0.0:8080 web/app:app
  ```

3. El servidor estará activo en la url [http://localhost:8080](http://localhost:8080)

### 📨 Configuración de envio de mensajes a través de Telegram

Para poder enviar mensajes a través de telegram debemos crear una nueva aplicación en Telegram siguiendo los siguientes [pasos.](https://core.telegram.org/api/obtaining_api_id-)

Una vez obtenida el api hash y api id, debemos añadirla en el siguiente fichero: config/notification.json

  ```
  {
    "check_hour": "08:05",
    "enabled_notifications": true,
    "telegram_api_hash": "<hash>",
    "telegram_api_id": "<id>",
    "telegram_receivers": "@usuariotelegram"
  }
  ```

Cuando el fichero se encuentre guardado, ya podrémos iniciar el modulo de notificaciones a través del siguiente comando:
  ```
  python source/notification/telegram_notifications.py
  ```

### 🌡 Configuración de la sección del tiempo.
Si se quiere habilitar la sección del tiempo donde se pueden consultar las predicciones de nubosidades, lluvias y fases lunares, debemos crear un API key en [openweathermap.org](openweathermap.org) y configurar el fichero de configuración config/weather.json con el API Key.

  ```
  {
    "latitude": "37.18817",
    "longitude": "-3.60667",
    "location": "Granada, ES",
    "api_key": "<api_key>",
    "units": "metric",
    "language": "en"
  }
  ```

## 🐍 ¿Como contribuir al proyecto?

<p align="justify">
  Para poder contribuir al proyecto solo es necesario crear un issue en esta página de github explicando el posible issue o mejora a incluir en el proyecto.
  Si se desea introducir cualquier cambio de código o documentación se puede realizar creando un pull-request y utilizando el nombrado de ramas a través de git-flow.
</p>

## 🐛 Licencia

Este proyecto está disponible mediante la licencia GPL-3.0 License.
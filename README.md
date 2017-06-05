# PracticaFinalVerificacion
Practica Final Verificacion Rubén Amador, Isabel Díaz

----------


Preparación
-------------

- Dentro de <i class="icon-folder-open"></i> `/PracticaFinalVerificacion/` activar el entorno virtual con `source venv/bin/activate`.
- Instalar las dependencias necesarias con `pip install -r requirements.txt`.

- Dejar abierta una conexión con la base de datos MongoDB con `[sudo] service mongod start` (teniendo MongoDB instalado).
  [link a Guía Instalación MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
- Importar la base de datos con las noticias con `mongoimport --db form --collection words --type json --file 20170603update.json` y a continuación `mongoimport --db analysis --collection words --type json --file initializeAnalysis.json`.

- Dejar abierto el puerto 5000 con Flask, moviéndonos al directorio `/PracticaFinalVerificacion/flask/`.

Ejecución
-------------
- Entrar en el directorio <i class="icon-folder-open"></i> `/PracticaFinalVerificacion/flask/` y ejecutar el comando `python form.py`.
- Abrir en un navegador la direccin `127.0.0.1:5000` que abrirá la página web.

Tests (Jenkins)
-------------
- Entrar en Jenkins a través de la dirección `localhost:8080` en el navegador (teniendo Jenkins instalado).
  [link a Guía Instalación Jenkins](https://jenkins.io/doc/book/getting-started/installing/)
 - Una vez logueados, hacer click en "New Item". Por ahora, crear uno "FreeStyle" con el nombre `PracticaFinalVerificacion`. Añadir el directorio de Github del proyecto. En el apartado "Build" añadir los siguientes comandos:
 
 ```
 cd ~/workspace/PracticaFinalVerificacion/sample_python/
 make test
 
 BUILD_ID=dontKillMeNow nohup Xvfb :99.0 &
 cd ~/workspace/PracticaFinalVerificacion/flask
 python form.py
 cd ~/workspace/PracticaFinalVerificacion/lettuce/tests/
 lettuce
 ```
 
 Ahora, desde el Dashboard, acceder a "Manage Jenkins > Configure System" y en el apartado "Global Variables" añadir la variable `DISPLAY` con el valor `:99.0`.
 
 En la terminal del SO ejecutar `export DISPLAY=:99.0`.
 
 Ahora sí, podemos ejecutar el job en Jenkins pulsando sobre "Build".

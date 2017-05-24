# PracticaFinalVerificacion
Practica Final Verificacion

----------


Preparación
-------------

- Dentro de <i class="icon-folder-open"></i> `/PracticaFinalVerificacion`instalar `virutalenv` con el comando `[sudo] pip install virtualenv`.
- Crear un entorno virtual llamado `pfv` con `virtualenv pfv`.
- Activar el entorno virtual con `source pfv/bin/activate`
- A continuación, dentro de <i class="icon-folder-open"></i> `/pfv` instalar `pymongo` con `pip install pymongo` (hacer esto antes de crear el proyecto `scrapy`).
- Copiar y reemplazar los archivos necesarios (esto es temporal).

Ejecución
-------------
- Entrar en el directorio <i class="icon-folder-open"></i> `/words/words/spiders` y ejecutar `scrapy crawl words` para scrappear la página web y obtener un archivo llamado `items.json` con el resultado.

# LionProj
Entrada para el examen de Lion Dev

Realizado con Django/Python 3 y con una pequeña inclusion de vue.js mediante CDN

# Estructura
LionProj

├─back: contiene configuraciones del proyecto

├─salas: aplicacion principal

  ├─static: elementos estaticos
  
  ├─templates: plantillas html

Ejecutar con el comando python manage.py runserver --noreload, se correra en el localhost:8000

Para los casos de prueba añadir la llave de seguridad enviada en el email en el archivo /back/settings.py en la linea 20

los usuarios se añaden mediante la pestaña de administrador de django (localhost:8000/admin/)
actualmente se encuentra el usuario normal (usr:sad, pwd: qsxwdcefv) y un super_usuario de igual manera enviado por correo

﻿**Nombre del proyecto:** VenVet

**Integrantes:**

- Alejandro Martín Garay Saavedra 
- Cesar Enrique Cabezas Baquerizo
- Diego Sebastian Pacheco Ferrel
- Yago Silva Albarracin

**Descripción del proyecto.**

El proyecto consiste en crear una plataforma que lleve el registro de una Veterinaria, esta contará con opciones de registro de una nueva mascota, entrada/salida de la mascota y la opción de borrar los datos de la base de datos.

**Objetivos principales** 

**Misión**

Brindar una plataforma de registros eficiente y de alta calidad de manera local.

**Visión**

Proyectarnos a tener la plataforma con un host en la nube mejorando el tiempo en la entrega de datos.

**Informacion de librerias/frameworks/plugins**
Hemos hecho uso del framework Bootstrap v5 
Las librerias son:
alembic==1.7.7
click==8.1.3
colorama==0.4.4
Flask==2.1.2
Flask-Login==0.6.1
Flask-Migrate==3.1.0
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
greenlet==1.1.2
importlib-metadata==4.11.3
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.2.0
MarkupSafe==2.1.1
psycopg2==2.9.3
SQLAlchemy==1.4.36
Werkzeug==2.1.2
WTForms==3.0.1
zipp==3.8.0

Estas tambien se pueden enontrar en el archivo requirements.txt.

**Pasos para ejecutar la app**
Ejecutar estos comandos en Bash:

`export DATABASE_URL="postgresql://postgres:123456789@localhost/appointments"`

`export APP_SETTINGS="config.DevelopmentConfig"`

`Luego, python veterinaria.py`

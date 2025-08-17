# Bela Crochet

**Bela Crochet** es un prototipo de tienda en línea desarrollado con Django 4.2. El objetivo es proporcionar una base mínima pero funcional para un e-commerce artesanal sin integración de pasarelas de pago. El flujo de compra culmina en la generación de un comprobante imprimible con instrucciones para pago offline.

## Requisitos

* Python 3.11+
* [pipenv](https://pipenv.pypa.io/) o `virtualenv` para gestionar un entorno virtual.
* Las dependencias se listan en `requirements.txt`.

## Instalación rápida

```bash
# clona el repositorio y entra en la carpeta
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# aplica migraciones y carga datos demo
python manage.py migrate
python manage.py seed_demo

# crea un usuario superusuario adicional si lo deseas
python manage.py createsuperuser

# arranca el servidor de desarrollo
python manage.py runserver

# Antigravity — Setup Guide

## 1. Instalar dependencias
```bash
cd antigravity
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## 2. Variables de entorno
El archivo `.env` ya está creado con valores para desarrollo (SQLite).
Para producción, edita `.env` con tus credenciales de PostgreSQL.

## 3. Migraciones y superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 4. Archivos estáticos (solo producción)
```bash
python manage.py collectstatic
```

## 5. Levantar el servidor de desarrollo
```bash
python manage.py runserver
```
Abre: http://127.0.0.1:8000/

## URLs clave
| Ruta | Descripción |
|------|-------------|
| `/` | Landing page |
| `/users/register/` | Registro (Asistente u Organizador) |
| `/users/login/` | Login |
| `/events/` | Catálogo público de eventos |
| `/events/create/` | Crear evento (solo Organizadores) |
| `/events/manage/` | Panel de mis eventos |
| `/tickets/mis-entradas/` | Mis entradas (Asistentes) |
| `/tickets/checkin/` | Check-In QR (Operadores) |
| `/tickets/dashboard/` | Dashboard analítico (Organizadores) |
| `/admin/` | Panel de administración Django |

## Crear un Operador
Desde el panel de administración (`/admin/`), crea un usuario con rol `OPERADOR`.

## Pago simulado
- Cualquier número de tarjeta funciona ✓  
- Tarjetas que terminan en `9999` → rechazo simulado ✕

## GitFlow (2 computadores)
```bash
# Computador 1 — rama base
git checkout -b develop
git push -u origin develop

# Computador 2 — clonar y trabajar
git checkout -b feature/frontend-events-booking develop

# Al terminar, merge sin fast-forward
git checkout develop
git merge --no-ff feature/frontend-events-booking
```

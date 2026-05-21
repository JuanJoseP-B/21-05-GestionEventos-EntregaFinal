# División de Trabajo — Antigravity · GitFlow 50/50

> **Proyecto:** Sistema de Gestión de Eventos y Entradas  
> **Metodología:** GitFlow con merge `--no-ff` para mantener historial paralelo limpio  
> **Ramas:** `main` → `develop` → `sebastian` / `juan`

---

## Estructura de ramas

```
main
 └── develop
      ├── sebastian   ← Computador 1
      └── juan        ← Computador 2
```

### Reglas obligatorias
- **Nunca** hacer push directo a `main` ni a `develop`
- Cada merge a `develop` usa `git merge --no-ff`
- Un commit por tarea/archivo significativo (no commits tipo "fix" sin contexto)
- Pull de `develop` antes de empezar cada sesión de trabajo

---

## SEBASTIAN — Computador 1

### Responsabilidad general
> Configuración del proyecto · Autenticación y usuarios · Modelos de datos (events) · UI base y Dashboard

### Archivos propios

#### Configuración del proyecto
| Archivo | Descripción |
|---------|-------------|
| `manage.py` | Entry point de Django |
| `requirements.txt` | Dependencias del proyecto |
| `.env.example` | Plantilla de variables de entorno |
| `.gitignore` | Exclusiones de Git |
| `SETUP.md` | Guía de instalación |
| `antigravity/__init__.py` | Paquete principal |
| `antigravity/settings.py` | Configuración Django (DB, apps, media, email) |
| `antigravity/urls.py` | URLs raíz del proyecto |
| `antigravity/wsgi.py` | Interfaz WSGI para producción |

#### App `users/` — Autenticación y Roles
| Archivo | Descripción |
|---------|-------------|
| `users/__init__.py` | Paquete |
| `users/apps.py` | Configuración de la app |
| `users/models.py` | `CustomUser` con roles: ORGANIZADOR, ASISTENTE, OPERADOR |
| `users/admin.py` | Panel admin personalizado para usuarios |
| `users/forms.py` | `LoginForm`, `RegisterForm`, `ProfileUpdateForm` |
| `users/views.py` | Vistas: login, logout, register, profile |
| `users/urls.py` | Rutas `/users/` |
| `users/migrations/` | Migraciones del modelo CustomUser |

#### App `events/` — Modelos y datos
| Archivo | Descripción |
|---------|-------------|
| `events/__init__.py` | Paquete |
| `events/apps.py` | Configuración de la app |
| `events/models.py` | Modelos: `Ubicacion`, `Evento`, `PrecioCategoria` |
| `events/admin.py` | Admin con inline de categorías |
| `events/forms.py` | `UbicacionForm`, `EventoForm`, `PrecioCategoriaFormSet` |
| `events/migrations/` | Migraciones de los 3 modelos |

#### Frontend — Base y Dashboard
| Archivo | Descripción |
|---------|-------------|
| `static/css/antigravity.css` | Sistema de diseño completo (glassmorphism, variables, componentes) |
| `templates/base.html` | Layout base con navbar, messages, footer |
| `templates/home.html` | Landing page con hero y eventos destacados |
| `templates/users/login.html` | Formulario de inicio de sesión glassmorphism |
| `templates/users/register.html` | Registro con selector visual de rol |
| `templates/users/profile.html` | Perfil + cambio de contraseña |
| `templates/dashboard/index.html` | Dashboard analítico con Chart.js (barras + línea) |

### Commits esperados (mínimo 7)

```bash
git commit -m "feat(config): inicializar proyecto Django con environ y whitenoise"
git commit -m "feat(users): modelo CustomUser con roles Organizador, Asistente, Operador"
git commit -m "feat(users): vistas y formularios de autenticación (login, register, profile)"
git commit -m "feat(events): modelos Ubicacion, Evento y PrecioCategoria con FK encadenadas"
git commit -m "feat(events): formularios EventoForm y PrecioCategoriaFormSet inline"
git commit -m "feat(frontend): sistema de diseño glassmorphism en antigravity.css"
git commit -m "feat(frontend): base.html, home.html y templates de autenticación"
git commit -m "feat(dashboard): integración Chart.js con API de ventas y asistencia"
```

### Comandos Git para Computador 1

```bash
# 1. Clonar el nuevo repositorio
git clone <URL-nuevo-repo>
cd <nombre-repo>

# 2. Crear rama develop en el repo (solo la primera vez, el primero que llegue)
git checkout -b develop
git push -u origin develop

# 3. Crear tu rama personal desde develop
git checkout -b sebastian
git push -u origin sebastian

# 4. Trabajar — ciclo de trabajo diario
git pull origin develop          # Traer cambios del compañero
git add <archivos-específicos>
git commit -m "feat(...): descripción"
git push origin sebastian

# 5. Cuando termines una fase, mergear a develop
git checkout develop
git pull origin develop
git merge --no-ff sebastian -m "merge: sebastian → develop (Sprint 1: Auth)"
git push origin develop
git checkout sebastian            # Volver a tu rama
```

---

## JUAN — Computador 2

### Responsabilidad general
> Vistas de eventos · Sistema completo de entradas (compra, QR, validación) · Check-in AJAX · Exportación Excel · API de estadísticas

### Archivos propios

#### App `events/` — Vistas y rutas
| Archivo | Descripción |
|---------|-------------|
| `events/views.py` | `HomeView`, `EventListView`, `EventDetailView`, CRUD views |
| `events/urls.py` | Rutas `/events/` con namespace |

#### App `tickets/` — Sistema completo de entradas
| Archivo | Descripción |
|---------|-------------|
| `tickets/__init__.py` | Paquete |
| `tickets/apps.py` | Configuración de la app |
| `tickets/models.py` | Modelo `Entrada` con UUID, QR, campo `usado`, `fecha_uso` |
| `tickets/admin.py` | Admin de entradas con filtros |
| `tickets/forms.py` | `CheckoutForm` (pasarela simulada), `ValidarEntradaForm` |
| `tickets/views.py` | Checkout, MyTickets, TicketDetail, ValidarQR, CheckIn AJAX, Dashboard API, ExportExcel |
| `tickets/urls.py` | Rutas `/tickets/` con todos los endpoints |
| `tickets/migrations/` | Migraciones del modelo Entrada |

#### Frontend — Eventos y Tickets
| Archivo | Descripción |
|---------|-------------|
| `templates/events/list.html` | Catálogo con búsqueda, filtro por ciudad y paginación |
| `templates/events/detail.html` | Detalle del evento con sidebar de compra |
| `templates/events/form.html` | Formulario crear/editar evento + formset de categorías |
| `templates/events/manage.html` | Panel de gestión de eventos del organizador |
| `templates/tickets/checkout.html` | Checkout con tarjeta simulada y total dinámico |
| `templates/tickets/my_tickets.html` | Lista de entradas compradas con QR thumbnail |
| `templates/tickets/ticket_detail.html` | Entrada individual con QR grande + descarga |
| `templates/tickets/validate.html` | Resultado de validación QR (acceso permitido/denegado) |
| `templates/tickets/checkin.html` | Panel check-in AJAX para Operadores con historial |

### Commits esperados (mínimo 7)

```bash
git commit -m "feat(events): vistas CRUD de eventos con mixins de permisos por rol"
git commit -m "feat(events): templates catálogo con búsqueda, filtros y paginación"
git commit -m "feat(events): template formulario con formset inline de categorías"
git commit -m "feat(tickets): modelo Entrada con UUID, QR generation y campo de uso"
git commit -m "feat(tickets): flujo de checkout con pasarela simulada (9999=rechazo)"
git commit -m "feat(tickets): template checkout con validación JS y total dinámico"
git commit -m "feat(tickets): check-in AJAX en tiempo real con historial de sesión"
git commit -m "feat(tickets): endpoint API JSON + exportación Excel con pandas"
git commit -m "feat(tickets): templates mis-entradas, detalle QR y validación"
```

### Comandos Git para Computador 2

```bash
# 1. Clonar el nuevo repositorio
git clone <URL-nuevo-repo>
cd <nombre-repo>

# 2. Crear tu rama desde develop (develop ya existe, lo creó Sebastian)
git checkout develop
git pull origin develop
git checkout -b juan
git push -u origin juan

# 3. Trabajar — ciclo de trabajo diario
git pull origin develop          # Traer cambios del compañero
git add <archivos-específicos>
git commit -m "feat(...): descripción"
git push origin juan

# 4. Cuando termines una fase, mergear a develop
git checkout develop
git pull origin develop
git merge --no-ff juan -m "merge: juan → develop (Sprint 3: Tickets y QR)"
git push origin develop
git checkout juan                 # Volver a tu rama
```

---

## Cronograma sugerido de merges

| Sesión | Sebastian mergea | Juan mergea |
|--------|-----------------|-------------|
| 1 | Config + Auth (users app) | — |
| 2 | Events models + admin | Events views + URLs |
| 3 | Base templates + CSS | Event templates (list, detail) |
| 4 | — | Tickets models + checkout |
| 5 | Dashboard template | Check-in AJAX + API |
| 6 | Merge final `develop → main` | Merge final `develop → main` |

---

## Merge final a main

Cuando ambas ramas estén integradas en `develop`:

```bash
# Cualquiera de los dos (ponerse de acuerdo)
git checkout main
git pull origin main
git merge --no-ff develop -m "release: v1.0.0 — Antigravity sistema completo"
git tag -a v1.0.0 -m "Entrega final · Sistema de Gestión de Eventos"
git push origin main --tags
```

---

## Resumen de archivos por persona

| | Sebastian | Juan |
|--|-----------|------|
| **Archivos Python** | 16 | 11 |
| **Templates HTML** | 7 | 9 |
| **CSS / Config** | 6 | 0 |
| **Total** | **29** | **20** |
| **Complejidad** | Setup + Auth + Modelos + Dashboard | CRUD views + Tickets completo + AJAX + API |

> La diferencia en cantidad de archivos se compensa con la complejidad técnica de Juan: generación de QR, pasarela simulada, check-in AJAX, API JSON y exportación Excel son las partes más complejas del proyecto.

# División de Trabajo — Antigravity · GitFlow 50/50

> **Proyecto:** Sistema de Gestión de Eventos y Entradas  
> **Ramas:** `main` → `develop` → `sebastian` / `juan`  
> **Regla de oro:** `git merge --no-ff` siempre · nunca push directo a `main`

---

## Leyenda

```
[S] = SEBASTIAN  (Computador 1)
[J] = JUAN       (Computador 2)
[*] = Compartido (lo crea Sebastian, Juan hace pull)
```

---

## Árbol completo del proyecto

```
antigravity/                          [*] raíz del proyecto
│
├── manage.py                         [S] entry point Django
├── requirements.txt                  [S] dependencias pip
├── .env.example                      [S] plantilla de variables de entorno
├── .gitignore                        [S] exclusiones de Git
├── SETUP.md                          [S] guía de instalación
├── DIVISION_TRABAJO.md               [*] este documento
│
├── antigravity/                      [S] paquete de configuración principal
│   ├── __init__.py                   [S]
│   ├── settings.py                   [S] base de datos, apps, media, email, whitenoise
│   ├── urls.py                       [S] enrutador raíz del proyecto
│   └── wsgi.py                       [S] interfaz producción
│
├── users/                            [S] app completa de autenticación
│   ├── __init__.py                   [S]
│   ├── apps.py                       [S] UsersConfig
│   ├── models.py                     [S] CustomUser — roles ORGANIZADOR/ASISTENTE/OPERADOR
│   ├── admin.py                      [S] panel admin con fieldsets personalizados
│   ├── forms.py                      [S] LoginForm · RegisterForm · ProfileUpdateForm
│   ├── views.py                      [S] login · logout · register · profile
│   ├── urls.py                       [S] rutas /users/
│   └── migrations/
│       ├── __init__.py               [S]
│       └── 0001_initial.py           [S] migración CustomUser
│
├── events/                           [S+J] app compartida — datos(S) + vistas(J)
│   ├── __init__.py                   [S]
│   ├── apps.py                       [S] EventsConfig
│   ├── models.py                     [S] Ubicacion · Evento · PrecioCategoria
│   ├── admin.py                      [S] inline de categorías en admin
│   ├── forms.py                      [S] EventoForm · UbicacionForm · PrecioCategoriaFormSet
│   ├── views.py                      [J] HomeView · EventListView · EventDetailView · CRUD
│   ├── urls.py                       [J] rutas /events/ con namespace
│   └── migrations/
│       ├── __init__.py               [S]
│       ├── 0001_initial.py           [S] Ubicacion · Evento · PrecioCategoria base
│       └── 0002_initial.py           [S] foreign keys entre modelos
│
├── tickets/                          [J] app completa de entradas
│   ├── __init__.py                   [J]
│   ├── apps.py                       [J] TicketsConfig
│   ├── models.py                     [J] Entrada — UUID · QR · pagado · usado · fecha_uso
│   ├── admin.py                      [J] admin con filtros por evento y estado
│   ├── forms.py                      [J] CheckoutForm · ValidarEntradaForm
│   ├── views.py                      [J] Checkout · MyTickets · ValidarQR · CheckIn
│   │                                     ApiValidar · DashboardView · ExportExcel
│   ├── urls.py                       [J] /tickets/ — checkout · validar · checkin · dashboard · api
│   └── migrations/
│       ├── __init__.py               [J]
│       ├── 0001_initial.py           [J] Entrada base (sin FK)
│       └── 0002_initial.py           [J] asistente · categoria · evento FK
│
├── templates/
│   ├── base.html                     [S] navbar · messages · footer · glassmorphism base
│   ├── home.html                     [S] landing page con hero y eventos destacados
│   │
│   ├── users/                        [S] todas las vistas de autenticación
│   │   ├── login.html                [S] formulario glass con manejo de errores
│   │   ├── register.html             [S] registro con selector visual de rol (JS)
│   │   └── profile.html              [S] perfil + cambio de contraseña
│   │
│   ├── events/                       [J] todas las vistas de eventos
│   │   ├── list.html                 [J] catálogo con búsqueda · filtro ciudad · paginación
│   │   ├── detail.html               [J] detalle con sidebar de compra por categoría
│   │   ├── form.html                 [J] crear/editar evento con formset inline de precios
│   │   └── manage.html               [J] panel del organizador con stats y acciones
│   │
│   ├── tickets/                      [J] todas las vistas de entradas
│   │   ├── checkout.html             [J] tarjeta simulada · total dinámico · formato JS
│   │   ├── my_tickets.html           [J] lista de entradas con QR thumbnail y estado
│   │   ├── ticket_detail.html        [J] entrada individual · QR grande · descarga
│   │   ├── validate.html             [J] resultado validación QR (OK / ya usada / error)
│   │   └── checkin.html              [J] panel AJAX para operadores con historial sesión
│   │
│   └── dashboard/
│       └── index.html                [S] sidebar · KPIs · Chart.js barras + línea · tabla
│
└── static/
    └── css/
        └── antigravity.css           [S] sistema de diseño completo:
                                          variables · glass · navbar · botones
                                          forms · cards · badges · alertas · animations
```

---

## SEBASTIAN — Computador 1 · Rama `sebastian`

### Módulos a cargo
| Módulo | Qué hace |
|--------|----------|
| **Configuración** | Inicializa Django, environ, whitenoise, base de datos |
| **`users/`** | CustomUser con 3 roles, login, register, perfil, admin |
| **`events/` (datos)** | Modelos Ubicacion, Evento, PrecioCategoria + forms + admin |
| **CSS global** | Sistema glassmorphism completo en `antigravity.css` |
| **Templates base** | `base.html`, `home.html`, `users/` (3 templates) |
| **Dashboard** | `dashboard/index.html` con Chart.js + API calls |

### Commits mínimos esperados

```bash
git commit -m "feat(config): inicializar proyecto Django 5 con environ, whitenoise y SQLite"
git commit -m "feat(users): CustomUser con roles Organizador, Asistente y Operador"
git commit -m "feat(users): vistas login, logout, register y perfil con cambio de contraseña"
git commit -m "feat(users): formularios de autenticación y actualización de perfil"
git commit -m "feat(events): modelos Ubicacion, Evento y PrecioCategoria con ForeignKey"
git commit -m "feat(events): admin con inline de categorías y formularios validados"
git commit -m "feat(frontend): sistema de diseño glassmorphism completo en antigravity.css"
git commit -m "feat(frontend): base.html con navbar por rol, messages y footer"
git commit -m "feat(frontend): home.html landing page y templates de autenticación"
git commit -m "feat(dashboard): index.html con Chart.js — gráfica barras y línea + KPIs"
```

### Flujo Git

```bash
# Configuración inicial (tú primero)
git clone <URL-nuevo-repo>
cd <nombre-repo>
git checkout -b develop
git push -u origin develop
git checkout -b sebastian
git push -u origin sebastian

# Ciclo diario
git pull origin develop              # integrar trabajo de Juan
git add <mis-archivos>
git commit -m "feat(...): descripción"
git push origin sebastian

# Al terminar una fase → merge a develop
git checkout develop
git pull origin develop
git merge --no-ff sebastian -m "merge(sebastian → develop): Sprint 1 — Config y Auth"
git push origin develop
git checkout sebastian
```

---

## JUAN — Computador 2 · Rama `juan`

### Módulos a cargo
| Módulo | Qué hace |
|--------|----------|
| **`events/views.py`** | Todas las vistas: lista pública, detalle, CRUD organizador |
| **`events/urls.py`** | Enrutamiento de eventos con namespace |
| **`tickets/`** | App completa: Entrada, checkout, QR, validación, check-in AJAX |
| **API JSON** | Endpoints de ventas por categoría y asistencia por día |
| **Exportación** | Excel con pandas/openpyxl |
| **Templates events** | `list`, `detail`, `form`, `manage` — 4 templates |
| **Templates tickets** | `checkout`, `my_tickets`, `detail`, `validate`, `checkin` — 5 templates |

### Commits mínimos esperados

```bash
git commit -m "feat(events): vistas HomeView, EventListView y EventDetailView con permisos"
git commit -m "feat(events): CRUD organizador con OrganizerRequiredMixin"
git commit -m "feat(events): URLs de events con namespace y rutas de gestión"
git commit -m "feat(tickets): modelo Entrada con UUID, generación QR y campos de control"
git commit -m "feat(tickets): CheckoutForm con validación de tarjeta simulada (9999=rechazo)"
git commit -m "feat(tickets): flujo de checkout — stock, pago, QR y correo de confirmación"
git commit -m "feat(tickets): ValidarQRView y ApiValidarView con lógica de acceso"
git commit -m "feat(tickets): CheckInView — panel AJAX en tiempo real para operadores"
git commit -m "feat(tickets): DashboardView con API JSON de ventas y asistencia por día"
git commit -m "feat(tickets): ExportExcelView con pandas — reporte completo de asistentes"
git commit -m "feat(frontend): templates events — list, detail, form y manage"
git commit -m "feat(frontend): templates tickets — checkout, my_tickets y ticket_detail"
git commit -m "feat(frontend): checkin.html AJAX con historial y validate.html de resultado"
```

### Flujo Git

```bash
# Configuración inicial (Sebastian ya creó develop)
git clone <URL-nuevo-repo>
cd <nombre-repo>
git checkout develop
git pull origin develop
git checkout -b juan
git push -u origin juan

# Ciclo diario
git pull origin develop              # integrar trabajo de Sebastian
git add <mis-archivos>
git commit -m "feat(...): descripción"
git push origin juan

# Al terminar una fase → merge a develop
git checkout develop
git pull origin develop
git merge --no-ff juan -m "merge(juan → develop): Sprint 3 — Tickets y QR"
git push origin develop
git checkout juan
```

---

## Cronograma de merges a develop

```
Sesión 1 ──► Sebastian: Config + users/ completo
Sesión 2 ──► Sebastian: events/ modelos + forms + admin
             Juan:      events/ views.py + urls.py
Sesión 3 ──► Sebastian: antigravity.css + base.html + home.html + users/ templates
             Juan:      events/ templates (list, detail, form, manage)
Sesión 4 ──► Juan:      tickets/ models + migrations + forms
Sesión 5 ──► Juan:      tickets/ views (checkout, QR, validación, check-in, API, Excel)
             Juan:      tickets/ templates (5 archivos)
Sesión 6 ──► Sebastian: dashboard/index.html + Chart.js
Sesión 7 ──► MERGE FINAL: develop ──► main + tag v1.0.0
```

---

## Merge final — Release v1.0.0

```bash
# Ambos deben tener develop actualizado antes de este paso
git checkout main
git pull origin main
git merge --no-ff develop -m "release: v1.0.0 — Antigravity sistema completo de eventos"
git tag -a v1.0.0 -m "Entrega final del proyecto · Sistema de Gestión de Eventos"
git push origin main --tags
```

---

## Resumen visual

```
┌─────────────────────────────────┬─────────────────────────────────┐
│        SEBASTIAN  [S]           │           JUAN  [J]             │
├─────────────────────────────────┼─────────────────────────────────┤
│  manage.py                      │  events/views.py                │
│  requirements.txt               │  events/urls.py                 │
│  .env.example / .gitignore      │                                 │
│  antigravity/settings.py        │  tickets/__init__.py            │
│  antigravity/urls.py            │  tickets/apps.py                │
│  antigravity/wsgi.py            │  tickets/models.py              │
│                                 │  tickets/admin.py               │
│  users/__init__.py              │  tickets/forms.py               │
│  users/apps.py                  │  tickets/views.py               │
│  users/models.py                │  tickets/urls.py                │
│  users/admin.py                 │  tickets/migrations/            │
│  users/forms.py                 │                                 │
│  users/views.py                 │  templates/events/list.html     │
│  users/urls.py                  │  templates/events/detail.html   │
│  users/migrations/              │  templates/events/form.html     │
│                                 │  templates/events/manage.html   │
│  events/__init__.py             │                                 │
│  events/apps.py                 │  templates/tickets/             │
│  events/models.py               │    checkout.html                │
│  events/admin.py                │    my_tickets.html              │
│  events/forms.py                │    ticket_detail.html           │
│  events/migrations/             │    validate.html                │
│                                 │    checkin.html                 │
│  static/css/antigravity.css     │                                 │
│  templates/base.html            │                                 │
│  templates/home.html            │                                 │
│  templates/users/login.html     │                                 │
│  templates/users/register.html  │                                 │
│  templates/users/profile.html   │                                 │
│  templates/dashboard/index.html │                                 │
├─────────────────────────────────┼─────────────────────────────────┤
│  29 archivos                    │  20 archivos                    │
│  Config + Auth + Modelos        │  Vistas + Tickets + AJAX + API  │
│  + CSS + UI Base + Dashboard    │  + Templates events/tickets     │
└─────────────────────────────────┴─────────────────────────────────┘
```

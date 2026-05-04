# LegalLens AI

Sistema SaaS para la auditoría automática de contratos legales (arrendamiento y NDA) mediante inteligencia artificial. Desarrollado para el despacho **García & Asociados**.

---

## Guía de inicio rápido

### Requisitos previos

- Docker Desktop instalado y en ejecución
- Una API key de Google Gemini ([console.cloud.google.com](https://console.cloud.google.com))

### 1. Clonar el repositorio y entrar en la carpeta

```bash
git clone https://github.com/rodrigogabela/CE-Python-OOP.git
cd CE-Python-OOP/legal_lens_ai
```

### 2. Crear el archivo de entorno

```bash
cp .env.example .env
```

Edita `.env` y añade tu clave de Google:

```
GOOGLE_API_KEY=AIzaSy...tu_clave_aqui
```

### 3. Levantar todos los servicios

```bash
docker compose up --build
```

La primera vez tarda unos minutos (descarga imágenes y construye los contenedores). Cuando veas `legallens-nginx` en estado `healthy`, la aplicación está lista.

### 4. Acceder

| URL | Descripción |
|-----|-------------|
| http://localhost:8080 | Aplicación principal |
| http://localhost:8080/admin/ | Panel de administración Django |

**Credenciales por defecto:**
- Admin → usuario: `admin` / contraseña: `admin`
- Abogados → regístrarse en `/accounts/register/`

### 5. Parar los servicios

```bash
docker compose down
```

Para eliminar también los volúmenes de base de datos:

```bash
docker compose down -v
```

---

## Variables de entorno

Copia `.env.example` a `.env` y rellena los valores:

```env
# Django
DJANGO_SECRET_KEY=cambia-esto-en-produccion-con-django-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend-django

# PostgreSQL
POSTGRES_DB=legallens
POSTGRES_USER=legallens
POSTGRES_PASSWORD=legallens_dev_password
POSTGRES_HOST=db-legal
POSTGRES_PORT=5432

# Microservicio FastAPI
FASTAPI_URL=http://ai-engine:8001

# Google Gemini (obligatorio para la auditoría IA)
GOOGLE_API_KEY=tu_api_key_aqui
```

> **Nota:** Nunca subas el `.env` real al repositorio. El archivo `.env.example` contiene solo los nombres de las variables, sin valores sensibles.

---

## Arquitectura de contenedores

```
Navegador
    │
    ▼ :8080
┌─────────────┐
│  nginx-proxy │  ← único puerto expuesto al exterior
└──────┬──────┘
       │ /static/, /media/ → sirve directamente desde volúmenes
       │ resto              → proxy_pass
       ▼
┌──────────────────┐      ┌─────────────────┐
│  backend-django  │ ───► │   ai-engine     │
│  (Django 5)      │      │   (FastAPI)     │
└──────────────────┘      └─────────────────┘
       │
       ▼
┌──────────────────┐
│    db-legal      │
│  (PostgreSQL 16) │
└──────────────────┘
```

Todos los servicios se comunican por la red interna `legallens-net`. Solo Nginx tiene puerto abierto al host.

---

## Esquema de clases — Aplicación de la POO

La lógica de auditoría aplica el **patrón Template Method**: una clase abstracta define el esqueleto del proceso de auditoría y cada subclase concreta aporta el conocimiento legal específico del tipo de contrato.

```
BaseContract  (abstracta)
│
│  Atributos de clase (sobreescriben las subclases):
│    CONTRACT_TYPE       → identificador del tipo ("RENTAL" / "NDA")
│    LEGAL_FRAMEWORK     → marco legal aplicable
│    TYPICAL_RED_FLAGS   → lista de cláusulas abusivas conocidas
│    KEY_DATA_FIELDS     → campos que el agente debe extraer
│
│  Métodos:
│    build_audit_prompt() → Template Method: construye el system prompt
│                           para el LLM combinando todos los atributos
│    set_text(text)       → almacena el texto extraído del PDF
│
├── RentalContract
│     CONTRACT_TYPE    = "RENTAL"
│     LEGAL_FRAMEWORK  = "LAU, art. 9/18/21/36 + RDL 7/2019"
│     TYPICAL_RED_FLAGS = [duración < 5 años, fianza > 1 mes,
│                          subida > IPC, jurisdicción extranjera, ...]
│     KEY_DATA_FIELDS   = [propietario, inquilino, renta_mensual,
│                          fianza, duración, jurisdicción]
│
└── NDAContract
      CONTRACT_TYPE    = "NDA"
      LEGAL_FRAMEWORK  = "Ley 1/2019, ET art. 21, RGPD, LOPJ art. 22"
      TYPICAL_RED_FLAGS = [confidencialidad perpetua,
                           no-compete > 2 años,
                           penalización > 2M€ sin moderación,
                           jurisdicción offshore, ...]
      KEY_DATA_FIELDS   = [divulgante, receptor, objeto,
                           duración_confidencialidad, penalización]
```

### Flujo completo de una auditoría

```
PDF subido
    │
    ▼
FastAPI /audit
    │
    ├─ _extract_pymupdf()      → extrae texto página a página (PyMuPDF)
    │   └─ fallback pdfplumber si PyMuPDF falla o extrae vacío
    │
    ├─ get_contract(type, text) → instancia RentalContract o NDAContract
    │                             y llama a set_text(text)
    │
    ├─ contract.build_audit_prompt()  → Template Method genera el prompt
    │                                   con el marco legal y red flags conocidas
    │
    ├─ LangChain + Gemini 2.5 Flash Lite
    │   └─ llm.with_structured_output(AuditResult)
    │       → devuelve directamente un objeto Pydantic validado
    │
    └─ AuditResult {
           contract_type,
           summary,
           key_data: dict,
           red_flags: list[RedFlag],   ← severidad: ALTA / MEDIA / BAJA
           is_clean: bool
       }
```

### Modelos Pydantic (schemas)

| Clase | Ubicación | Descripción |
|-------|-----------|-------------|
| `RedFlag` | `fastapi_engine/contracts/base.py` | Cláusula problemática con clausula, problema, artículo legal y severidad |
| `AuditResult` | `fastapi_engine/contracts/base.py` | Resultado completo de la auditoría |
| `ExtractResponse` | `fastapi_engine/main.py` | Respuesta del endpoint `/extract` |
| `AuditResponse` | `fastapi_engine/main.py` | Respuesta del endpoint `/audit` |

---

## Estructura del proyecto

```
legal_lens_ai/
├── dataset/                        ← Contratos de prueba
│   ├── alquiler_contrato_legal.pdf
│   ├── alquiler_contrato_trampa.pdf
│   ├── nda_contrato_legal.pdf
│   └── nda_contrato_trampa.pdf
│
├── django_backend/                 ← Backend principal
│   ├── accounts/                   ← Registro y login de abogados
│   ├── contracts/                  ← Modelos, vistas, cliente FastAPI
│   │   ├── models.py               ← Contract + AuditReport
│   │   ├── views.py                ← Upload, dashboard, detail
│   │   └── ai_client.py            ← HTTP client hacia FastAPI
│   └── templates/
│
├── fastapi_engine/                 ← Microservicio de IA
│   ├── main.py                     ← Endpoints /health /extract /audit
│   ├── contracts/
│   │   ├── base.py                 ← BaseContract + AuditResult (POO)
│   │   ├── rental.py               ← RentalContract
│   │   └── nda.py                  ← NDAContract
│   └── agent/
│       └── auditor.py              ← Agente LangChain + Gemini
│
├── nginx/
│   └── nginx.conf                  ← Reverse proxy
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Dataset de pruebas

Los contratos de la carpeta `dataset/` han sido redactados específicamente para validar el sistema:

### Contratos de arrendamiento

**`alquiler_contrato_legal.pdf`** — Cumple íntegramente la LAU:
- Duración 5 años (art. 9.1 LAU)
- Actualización por IGC con límite del 3 % (RDL 7/2019)
- Fianza de 1 mensualidad (art. 36.1 LAU)
- Jurisdicción en Madrid (art. 52.1.7.º LEC)

**`alquiler_contrato_trampa.pdf`** — Contiene 4 cláusulas abusivas:
- Duración de **2 años** (viola art. 9 LAU — mínimo 5)
- Subida fija del **8 % anual** (viola RDL 7/2019)
- Fianza de **4 mensualidades** (viola art. 36 LAU — máximo 1)
- Jurisdicción en **Gibraltar** (fuero extranjero inaplicable)

### Acuerdos de confidencialidad (NDA)

**`nda_contrato_legal.pdf`** — Dentro de los límites legales:
- Confidencialidad de 3 años (plazo razonable)
- Penalización de 15.000 € con moderación judicial (art. 1154 CC)
- No-competencia de 1 año en España (art. 21.4 ET)
- Jurisdicción en Madrid (Ley 1/2019 y art. 22 LOPJ)

**`nda_contrato_trampa.pdf`** — Contiene 4 cláusulas problemáticas:
- Confidencialidad **perpetua** (viola Ley 1/2019)
- Penalización de **5.000.000 €** sin moderación judicial (viola art. 1154 CC)
- No-competencia de **5 años en toda la UE** (viola ET art. 21)
- Jurisdicción en **Islas Caimán** (fuero inaccesible)

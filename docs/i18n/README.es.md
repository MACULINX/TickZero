# TickZero

**TickZero: Extracción de momentos destacados impulsada por IA para CS2. Transforma tu gameplay de Counter-Strike 2 en clips virales de TikTok/Reels automáticamente usando IA GRATUITA.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **Leer en otros idiomas:** [English](../../README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [简体中文](README.zh.md)

## 🎯 Características

- **🎮 Registro de Eventos en Vivo** - Captura kills, headshots y eventos de ronda en tiempo real vía CS2 Game State Integration
- **⏱️ Sincronización con OBS** - Alineación precisa de marcas de tiempo entre eventos del juego y grabación de video
- **🤖 Análisis Potenciado por IA** - Usa Google Gemini (nivel GRATUITO) para identificar momentos destacables
- **✂️ Edición de Video Automática** - Conversión basada en FFmpeg a formato vertical (9:16) con fondo desenfocado
- **⚡ Aceleración por Hardware** - Soporta NVIDIA NVENC con respaldo automático a CPU

## 📋 Requisitos

### Software
- **Python** 3.10 o superior
- **OBS Studio** con plugin WebSocket habilitado
- **FFmpeg** (soporte de codificación por hardware opcional)
- **Counter-Strike 2**
- **Clave API de Google** para Gemini (nivel GRATUITO disponible - ¡no se requiere tarjeta de crédito!)

### Dependencias de Python
```bash
pip install -r requirements.txt
```

**Dependencias:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 Inicio Rápido

### 1. Clonar e Instalar

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. Configurar WebSocket de OBS

1. Abrir **OBS Studio**
2. Ir a **Herramientas → Configuración del Servidor WebSocket**
3. Habilitar el servidor WebSocket
4. Anotar el puerto (predeterminado: `4455`) y la contraseña (si está configurada)
5. Actualizar `config` en `main.py`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # Puerto OBS WebSocket
    'obs_password': '',            # Contraseña OBS WebSocket
    'gsi_port': 3000,              # Puerto servidor GSI
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True,               # Habilitar aceleración GPU
    'continuous_mode': True,       # Auto-procesar tras cada partida
    'auto_process': True,          # Habilitar procesamiento automático
    'auto_min_priority': 6         # Prioridad mínima (1-10)
}
```

### Aceleración por GPU

TickZero detecta y usa automáticamente el mejor codificador GPU disponible:

1. **NVIDIA NVENC** (h264_nvenc) - Requiere GPU NVIDIA con drivers
2. **AMD AMF** (h264_amf) - Requiere GPU AMD Radeon
3. **Intel QuickSync** (h264_qsv) - Requiere CPU Intel con gráficos integrados
4. **CPU Fallback** (libx264) - Funciona en cualquier sistema

### Modo de Grabación Continua

Con `continuous_mode: True`, TickZero:
- Detecta automáticamente el fin de la partida (evento "gameover")
- Procesa los destacados en segundo plano
- Continúa grabando para la siguiente partida
- ¡No es necesario reiniciar entre partidas!

### 3. Habilitar Game State Integration de CS2

Copiar `gamestate_integration_highlights.cfg` a tu carpeta de configuración de CS2:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. Obtener Clave API de Google Gemini (¡GRATIS!)

1. Visitar [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Iniciar sesión con tu cuenta de Google
3. Hacer clic en **"Create API Key"**
4. Copiar tu clave (comienza con `AIzaSy...`)
5. Configurarla como variable de entorno:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "tu-clave-api-aqui"

# Hacerla permanente:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'tu-clave-api-aqui', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="tu-clave-api-aqui"

# Hacerla permanente (agregar a ~/.bashrc o ~/.zshrc):
echo 'export GOOGLE_API_KEY="tu-clave-api-aqui"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **Nota:** Gemini 2.5 Flash es GRATUITO con 1500 solicitudes/día. ¡Suficiente para ~50 partidas por día!

## 📖 Uso

La pipeline funciona en **dos fases**:

### Fase 1: Registro en Vivo (Durante la Partida)

Ejecutar esto **ANTES** de comenzar tu partida de CS2:

```bash
python main.py live
```

**Lo que sucede:**
1. ✅ Se conecta a OBS WebSocket
2. ✅ Inicia la grabación automáticamente
3. ✅ Inicia el servidor GSI en el puerto 3000
4. ✅ Registra todos los eventos del juego con marcas de tiempo de video precisas

Juega tu partida normalmente. Cuando termines, presiona `Ctrl+C` para detener el registro.

Los eventos se guardan en `match_log.json`.

### Fase 2: Post-Procesamiento (Después de la Partida)

Ejecutar esto **DESPUÉS** de la partida para crear clips destacados:

```bash
python main.py process <ruta_grabacion.mp4> [clave_api] [prioridad_min]
```

**Ejemplo:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**Parámetros:**
- `<ruta_grabacion.mp4>` - Ruta a tu grabación de OBS (requerido)
- `[clave_api]` - Clave API de Google (opcional si la variable de entorno `GOOGLE_API_KEY` está configurada)
- `[prioridad_min]` - Prioridad mínima del clip 1-10 (predeterminado: 6)

**Lo que sucede:**
1. 🤖 La IA analiza `match_log.json`
2. 🎯 Identifica momentos destacados (multi-kills, clutches, headshots)
3. ✂️ Crea clips de video verticales en el directorio `highlights/`

## 🎬 Formato de Salida

**Especificaciones de Video Vertical:**
- **Resolución:** 1080×1920 (relación de aspecto 9:16)
- **Formato:** MP4 (H.264)
- **Audio:** AAC estéreo
- **Estilo Visual:** Fondo desenfocado + gameplay centrado

**Convención de Nombres de Archivo:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🐛 Solución de Problemas

### Problemas de Conexión OBS
- ✅ Asegúrate de que OBS Studio se esté ejecutando
- ✅ Verifica que WebSocket esté habilitado: **Herramientas → Configuración del Servidor WebSocket**
- ✅ Verifica que el puerto y la contraseña coincidan con tu configuración

### No se Registran Eventos
- ✅ Verifica que `gamestate_integration_highlights.cfg` esté en la carpeta CS2 correcta
- ✅ Comprueba que el servidor GSI se esté ejecutando (debería mostrar "Listening on port 3000")
- ✅ Inicia CS2 y revisa la consola para ver mensajes de conexión GSI

### Errores de FFmpeg
- ✅ Asegúrate de tener FFmpeg instalado: `ffmpeg -version`
- ✅ Verifica que la ruta del video fuente sea correcta
- ✅ Intenta configurar `use_gpu: False` si encuentras errores de NVENC

### IA No Devuelve Destacados
- ✅ Verifica que `match_log.json` contenga eventos de asesinatos
- ✅ Reduce el umbral `min_priority` (intenta con 4 o 5)
- ✅ Verifica que tu clave API de Google sea válida: ejecuta `python examples/test_gemini_api.py`
- ✅ Comprueba no haber excedido la cuota diaria (1500 solicitudes)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Siéntete libre de enviar un Pull Request. Para cambios importantes, abre primero un issue para discutir lo que te gustaría cambiar.

Ver [CONTRIBUTING.md](../../CONTRIBUTING.md) para detalles.

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](../../LICENSE) para detalles.

**Resumen:** Puedes usar, modificar y distribuir libremente este código, pero debes incluir el aviso de copyright original y no puedes responsabilizar a los autores.

## 🙏 Reconocimientos

### Construido Con
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - Cliente Python para OBS WebSocket
- [Google Gemini API](https://ai.google.dev/) - Análisis de destacados potenciado por IA
- [FFmpeg](https://ffmpeg.org/) - Motor de procesamiento de video

### Asistencia de IA
Partes de la base de código de este proyecto fueron creadas con la asistencia de modelos de lenguaje de IA (Google Gemini, Claude) para acelerar el desarrollo y mejorar la calidad del código. Todo el código generado por IA ha sido revisado, probado y adaptado para este caso de uso específico.

---

**Hecho con ❤️ por gamers, para gamers.**

**¡Dale una estrella ⭐ a este repo si lo encontraste útil!**

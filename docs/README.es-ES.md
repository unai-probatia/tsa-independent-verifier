# Verificador Independiente de Sellos de Tiempo TSA

🔐 **Verifique sellos de tiempo de forma independiente - ¡No se requiere confianza!**

[English](README.en-US.md) | [Español](README.es-ES.md)

Esta herramienta permite a cualquier persona verificar criptográficamente sellos de tiempo RFC 3161 sin depender del servicio de sellado original. Perfecta para auditores, responsables de cumplimiento normativo y cualquier persona que necesite verificar sellos de tiempo de documentos.

## Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)
- [Qué Necesita](#qué-necesita)
- [Referencia de Comandos](#referencia-de-comandos)
- [Proveedores Soportados](#proveedores-soportados)
- [Biblioteca Python](#biblioteca-python)
- [Ejemplo Práctico](#ejemplo-práctico)
- [Por Qué la Verificación Independiente](#por-qué-la-verificación-independiente)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## Inicio Rápido

### Instalación
```bash
git clone https://github.com/unai-probatia/tsa-independent-verifier.git
cd tsa-independent-verifier
pip install -r requirements.txt
```

### Uso Básico

Ha recibido tres elementos:
- Un archivo `.tsr` (token de sello de tiempo)
- El hash del documento (SHA-256)
- El nombre del proveedor (ej., "SSL", "FreeTSA")
```bash
python verify_timestamp.py \
  --tsr documento.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL
```

### Salida Esperada
```
================================================================================
              RESULTADO DE VERIFICACIÓN INDEPENDIENTE DE SELLO DE TIEMPO
================================================================================

✓✓✓ ESTADO: VERIFICADO Y AUTÉNTICO ✓✓✓

  Fecha/Hora:       2025-09-13 05:02:15 UTC
  Autoridad TSA:    DigiCert SHA512 RSA4096
  Número de Serie:  169790533997128162934813285611086882
  Proveedor:        SSL

────────────────────────────────────────────────────────────────────────────────
  RESULTADO DE LA VERIFICACIÓN:
  ✓ Este sello de tiempo ha sido verificado independientemente
  ✓ El documento existía en la fecha indicada
  ✓ El documento no ha sido alterado desde el sellado
  ✓ La firma criptográfica es válida
────────────────────────────────────────────────────────────────────────────────
================================================================================
```

## Qué Necesita

### Elementos Requeridos para la Verificación

1. **Archivo de Token de Sello de Tiempo (.tsr)**
   - Archivo binario que contiene el token de sello de tiempo RFC 3161
   - Proporcionado por el servicio de sellado de tiempo
   - Extensión de archivo: `.tsr` o `.timestamp`
   - Tamaño: Típicamente 3-10 KB

2. **Hash del Documento (SHA-256)**
   - Cadena hexadecimal de 64 caracteres
   - Representa la huella digital del documento sellado
   - Ejemplo: `2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656`
   - Para calcular: `sha256sum su_documento.pdf`

3. **Nombre del Proveedor**
   - Nombre de la TSA (Autoridad de Sellado de Tiempo)
   - Ejemplos: SSL, FreeTSA, Sectigo, GlobalSign, Apple, Microsoft
   - Sensible a mayúsculas (use los nombres exactos de la lista de proveedores)
   - Ver todos los proveedores: `python verify_timestamp.py --list-providers`

## Referencia de Comandos

### Listar Todos los Proveedores Soportados
```bash
python verify_timestamp.py --list-providers
```

Muestra todos los proveedores TSA conocidos con sus URLs y prioridades.

### Verificar con Salida Detallada

Obtener información detallada sobre el proceso de verificación:
```bash
python verify_timestamp.py \
  --tsr documento.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --verbose
```

El modo detallado muestra:
- OID de política
- Precisión del sello de tiempo
- Algoritmo de hash
- Tamaño del token en bytes
- Hash completo del documento
- Detalles del proveedor (URL, descripción)

### Comparar con el Sistema Original

Verificar que la verificación independiente coincide con el sistema original:
```bash
python verify_timestamp.py \
  --tsr documento.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --compare true
```

Use `--compare false` si el sistema original reportó el sello de tiempo como inválido.

### Verificar desde Archivo JSON

Si tiene los datos de verificación en formato JSON:
```bash
python verify_timestamp.py --json datos_verificacion.json
```

**Formato JSON:**
```json
{
  "hash": "2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656",
  "timestamp_token": {
    "$binary": {
      "base64": "MIIXxgYJKoZIhvcNAQcCoIIX...",
      "subType": "00"
    }
  },
  "provider": "SSL"
}
```

### Modo Silencioso (para Scripts)

Salida mínima - solo muestra si es válido o inválido:
```bash
python verify_timestamp.py \
  --tsr documento.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --quiet
```

**Salida:** `✓ VÁLIDO` o `✗ INVÁLIDO`

**Uso en scripts:**
```bash
if python verify_timestamp.py --tsr doc.tsr --hash abc123... --provider SSL --quiet; then
    echo "Sello de tiempo válido - documento auténtico"
    # Continuar con el procesamiento
else
    echo "ADVERTENCIA: ¡Sello de tiempo inválido!"
    # Manejar fallo de verificación
fi
```

### Habilitar Modo de Depuración

Para solución de problemas:
```bash
python verify_timestamp.py \
  --tsr documento.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --debug
```

## Proveedores Soportados

Esta herramienta soporta todos los principales proveedores TSA compatibles con RFC 3161:

| Prioridad | Proveedor      | URL                                          | Región      |
|-----------|----------------|----------------------------------------------|-------------|
| 1         | FreeTSA        | https://freetsa.org/tsr                      | Global      |
| 2         | SafeCreative   | https://tsa.safecreative.org                 | España      |
| 3         | OpenTimestamps | https://alice.btc.calendar.opentimestamps.org | Blockchain  |
| 4         | Sectigo        | http://timestamp.sectigo.com/qualified       | Reino Unido |
| 5         | SSL (DigiCert) | http://timestamp.digicert.com                | EE.UU.      |
| 6         | GlobalSign     | http://timestamp.globalsign.com/tsa/v3       | Global      |
| 7         | Apple          | http://timestamp.apple.com/ts01              | EE.UU.      |
| 8         | Microsoft      | http://timestamp.microsoft.com/scripts/timstamp.dll | EE.UU. |
| 9         | CEV            | https://tsa.cev.be/tsawebservice             | Bélgica     |
| 10        | Intesi         | http://tsa.time4mind.com/timestamp           | Italia      |
| 11        | TrueTimestamp  | https://truetimestamp.org/timestamp          | Global      |
| 12        | Sigstore       | https://timestamp.sigstore.dev/timestamp     | Código Abierto |
| 13        | Identrust      | http://timestamp.identrust.com               | EE.UU.      |

**Nota:** La herramienta funciona con CUALQUIER TSA compatible con RFC 3161, no solo las listadas arriba.

## Biblioteca Python

### Uso Básico
```python
from tsa_verifier import IndependentTSAVerifier

# Inicializar verificador
verifier = IndependentTSAVerifier()

# Verificar desde archivo .tsr
result = verifier.verify_from_tsr_file(
    tsr_file_path="documento.tsr",
    original_hash="2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656",
    provider_name="SSL"
)

# Comprobar resultado
if result['valid']:
    print(f"✓ ¡Verificado!")
    print(f"  Fecha/Hora: {result['timestamp']}")
    print(f"  TSA: {result['tsa_authority']}")
    print(f"  Serie: {result['serial_number']}")
else:
    print(f"✗ Verificación fallida: {result['error']}")
```

### Verificar desde Diccionario
```python
data = {
    "hash": "2f94444c1fe84c7f...",
    "timestamp_token": "token_codificado_base64",
    "provider": "SSL"
}

result = verifier.verify_from_dict(data)
```

### Comparar con el Sistema Original
```python
# Verificar independientemente
result = verifier.verify_from_tsr_file(
    tsr_file_path="documento.tsr",
    original_hash="2f94444c1fe84c7f...",
    provider_name="SSL"
)

# Comparar con la verificación del sistema original
comparison = verifier.compare_with_original_verification(
    verification_data=result,
    original_verified=True  # Estado del sistema original
)

if comparison['results_match']:
    print("✓ La verificación independiente confirma el sistema original")
    print(f"  Nivel de Confianza: {comparison['trust_level']}")
else:
    print("⚠ ADVERTENCIA: ¡Discrepancia de verificación detectada!")
    print(f"  Independiente: {comparison['independent_verification']}")
    print(f"  Original: {comparison['original_verification']}")
```

### Listar Proveedores Programáticamente
```python
verifier = IndependentTSAVerifier()
providers = verifier.list_providers()

for provider in providers:
    print(f"{provider['name']}: {provider['url']}")
```

## Ejemplo Práctico

### Escenario: Verificar un Contrato Sellado

Ha recibido un contrato (`contrato.pdf`) con un sello de tiempo. El remitente proporcionó:
- Archivo de sello: `contrato_timestamp.tsr`
- Hash del documento: (lo calculará usted)
- Proveedor: "SSL" (DigiCert)

**Paso 1: Calcular el hash del documento**
```bash
# En Linux/Mac:
sha256sum contrato.pdf

# En Windows (PowerShell):
Get-FileHash contrato.pdf -Algorithm SHA256

# Salida de ejemplo:
# 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656  contrato.pdf
```

**Paso 2: Verificar el sello de tiempo**
```bash
python verify_timestamp.py \
  --tsr contrato_timestamp.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --verbose
```

**Paso 3: Interpretar el resultado**

✓ **Si la verificación tiene éxito:**
- El contrato existía en la fecha indicada
- El contrato no ha sido modificado desde entonces
- El sello de tiempo es criptográficamente válido
- Tiene prueba independiente que no depende del servicio de sellado

✗ **Si la verificación falla:**
- El hash no coincide (documento incorrecto o modificado)
- El archivo .tsr está corrupto
- El nombre del proveedor es incorrecto
- El token de sello de tiempo es inválido

## Por Qué la Verificación Independiente

### Confianza a Través de la Transparencia

La verificación tradicional requiere confiar en el servicio de sellado:
```
Usuario → Envía hash al servicio → Servicio dice "sí, es válido" → Usuario confía en el servicio
```

La verificación independiente elimina este requisito de confianza:
```
Usuario → Verifica localmente con herramienta de código abierto → Prueba criptográfica → No se necesita confianza
```

### Beneficios Principales

✓ **No Se Requiere Confianza**
- No necesita confiar en el servicio de sellado original
- La verificación se realiza localmente en su ordenador
- Basada en estándares criptográficos abiertos (RFC 3161)

✓ **Transparente y Auditable**
- Todo el código es de código abierto
- Cualquiera puede revisar la lógica de verificación
- Los resultados son reproducibles por cualquier persona

✓ **Legalmente Sólido**
- Proporciona prueba criptográfica independiente
- Adecuado para procedimientos legales
- Cumple con estándares internacionales de sellado de tiempo

✓ **Permanentemente Válido**
- Mientras tenga el archivo .tsr y el hash
- No depende de la disponibilidad del servicio
- Puede verificarse décadas después

### Casos de Uso

**Legal y Cumplimiento Normativo**
- Sellado de contratos
- Protección de propiedad intelectual
- Cumplimiento normativo (RGPD, LOPD, SOX)
- Preservación de evidencia legal

**Técnico y Seguridad**
- Verificación de firma de código
- Informática forense digital
- Validación de pista de auditoría
- Verificación de integridad de documentos

**Operaciones Empresariales**
- Sellado de facturas
- Confirmación de pedidos
- Registro de transacciones
- Archivo de correo electrónico

## Códigos de Salida

La herramienta devuelve códigos de salida estándar para uso en scripts:

- `0` - Verificación exitosa (sello de tiempo válido)
- `1` - Verificación fallida (sello de tiempo inválido o error ocurrido)
- `130` - Operación cancelada por el usuario (Ctrl+C)

**Ejemplo de uso en bash:**
```bash
#!/bin/bash

if python verify_timestamp.py --tsr "$ARCHIVO_TSR" --hash "$HASH" --provider "$PROVEEDOR" --quiet; then
    echo "✓ Sello de tiempo verificado exitosamente"
    # Continuar con el procesamiento normal
    procesar_documento.sh
else
    echo "✗ Verificación de sello de tiempo fallida"
    # Manejar fallo de verificación
    registrar_error.sh "Sello de tiempo inválido detectado"
    exit 1
fi
```

## Preguntas Frecuentes

### Preguntas Generales

**P: ¿Qué es un token de sello de tiempo?**  
R: Un token de sello de tiempo (RFC 3161) es una prueba criptográfica de que un documento existía en un momento específico. Es como un sello de notario digital que puede verificarse independientemente.

**P: ¿Por qué se necesita el archivo .tsr?**  
R: El archivo .tsr contiene la prueba criptográfica (token de sello de tiempo). Sin él, la verificación es imposible. Es como un certificado firmado que prueba cuándo sucedió algo.

**P: ¿Qué hago si no tengo el archivo .tsr?**  
R: Debe obtenerlo de quien selló el documento. Sin el archivo .tsr, no puede verificar el sello de tiempo.

**P: ¿Puedo verificar sellos de tiempo de cualquier proveedor TSA?**  
R: ¡Sí! Esta herramienta funciona con cualquier TSA compatible con RFC 3161, no solo con los 13 proveedores listados. La lista de proveedores es por comodidad, pero cualquier TSA compatible funcionará.

### Preguntas Técnicas

**P: ¿Cómo funciona la verificación independiente?**  
R: La herramienta:
1. Lee el token de sello de tiempo del archivo .tsr
2. Extrae el hash incrustado del token
3. Lo compara con el hash de su documento
4. Verifica la firma criptográfica de la TSA
5. Valida la estructura del sello de tiempo (RFC 3161)

**P: ¿Esta herramienta se conecta a Internet?**  
R: ¡No! Toda la verificación se realiza localmente usando algoritmos criptográficos. Sus documentos nunca salen de su ordenador.

**P: ¿Qué algoritmos criptográficos se utilizan?**  
R: La herramienta soporta algoritmos estándar de la industria:
- Hash: SHA-256, SHA-384, SHA-512
- Firma: RSA (2048-4096 bit), ECDSA
- Estándar: RFC 3161 (Protocolo de Sello de Tiempo PKI X.509 de Internet)

**P: ¿Puede la herramienta ser engañada o evitada?**  
R: No. La verificación se basa en pruebas criptográficas. Si alguien modifica:
- El documento → El hash no coincidirá
- El sello de tiempo → La verificación de firma fallará
- El archivo .tsr → La estructura criptográfica será inválida

### Solución de Problemas

**P: La verificación falló - ¿qué debo comprobar?**  
R:
1. Asegúrese de que el hash coincide exactamente con el documento
2. Verifique que el archivo .tsr no esté corrupto (compruebe tamaño > 0)
3. Confirme que el nombre del proveedor es correcto (sensible a mayúsculas)
4. Pruebe con la bandera `--debug` para información detallada del error

**P: Obtengo error "Archivo no encontrado"**  
R: Compruebe que las rutas de archivo son correctas. Use rutas absolutas si es necesario:
```bash
python verify_timestamp.py \
  --tsr /ruta/completa/al/documento.tsr \
  --hash abc123... \
  --provider SSL
```

**P: La herramienta dice "Proveedor desconocido"**  
R: El nombre del proveedor debe coincidir exactamente (sensible a mayúsculas). Use `--list-providers` para ver los nombres exactos. Errores comunes:
- ❌ "ssl" → ✓ "SSL"
- ❌ "DigiCert" → ✓ "SSL"
- ❌ "freetsa" → ✓ "FreeTSA"

### Preguntas de Seguridad

**P: ¿Cómo sé que esta herramienta no está manipulada?**  
R: 
1. El código es de código abierto - audítelo usted mismo
2. Haga que un experto en seguridad lo revise
3. Compare resultados con otras herramientas de verificación RFC 3161
4. Consulte el historial de commits del repositorio de GitHub

**P: ¿Qué pasa si el servicio de sellado fue hackeado?**  
R: ¡La verificación independiente le protege! Incluso si el servicio está comprometido:
- Los sellos antiguos siguen siendo válidos (prueba criptográfica)
- Puede verificar sin contactar con el servicio
- La verificación no depende de la integridad del servicio

**P: ¿Puede esto usarse como evidencia legal?**  
R: ¡Sí! La herramienta proporciona prueba criptográfica que cumple con estándares internacionales. Sin embargo, siempre consulte con expertos legales para su jurisdicción específica.

## Soporte y Contribución

### Obtener Ayuda

- 📖 **Documentación**: [https://docs.probatia.com/](https://docs.probatia.com/)
- 🐛 **Reportar Problemas**: [GitHub Issues](https://github.com/unai-probatia/tsa-independent-verifier.git/issues)
- 📧 **Correo Electrónico**: hello@probatia.com

### Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haga un fork del repositorio
2. Cree una rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Haga commit de sus cambios (`git commit -m 'Añadir característica increíble'`)
4. Push a la rama (`git push origin feature/caracteristica-increible`)
5. Abra un Pull Request

### Vulnerabilidades de Seguridad

Si descubre una vulnerabilidad de seguridad:
- 🔒 **NO** abra un issue público
- 📧 Correo electrónico: security@yourcompany.com
- 🔐 Use PGP si es posible (clave en el sitio web)

Tomamos la seguridad en serio y responderemos con prontitud.

## Licencia

Licencia MIT

Copyright (c) 2025 Nombre de Su Empresa

Se concede permiso, libre de cargos, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados (el "Software"),
para utilizar el Software sin restricción, incluyendo sin limitación los derechos
a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender
copias del Software, y a permitir a las personas a las que se les proporcione el
Software a hacer lo mismo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las
copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "COMO ESTÁ", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
AUTORES O PROPIETARIOS DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE NINGUNA
RECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN DE CONTRATO,
AGRAVIO O CUALQUIER OTRO MOTIVO, DERIVADAS DE, FUERA DE O EN CONEXIÓN CON EL
SOFTWARE O SU USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.

---

**Versión:** 1.0.0  
**Última Actualización:** 21 de enero de 2025  
**Hecho con ❤️ para la transparencia en el sellado de tiempo digital**
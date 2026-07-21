# Victory AI - Agente Inteligente de Soporte Ecommerce

## Descripción del proyecto

Victory AI es un agente inteligente de soporte desarrollado para una tienda ecommerce ficticia llamada **Victory**.

El sistema utiliza una arquitectura **RAG (Retrieval Augmented Generation)** para responder consultas de usuarios utilizando información contenida en documentos internos de la empresa, como:

- Política de privacidad
- Política de reembolso y devoluciones
- Guía de envíos y entregas
- Preguntas frecuentes
- Términos y condiciones


Además, se implementó un flujo de decisión mediante **LangGraph**, permitiendo que el agente clasifique las consultas y determine si debe:

- Responder automáticamente.
- Solicitar información adicional.
- Generar un ticket de soporte.


## Arquitectura del proyecto
En cuanto a arquitectura: esto se dividio en 
-Lang.py : Estado y nodos del agente LangGraph
-main.py: Interfaz de interacción con el usuario
-llm.py:Configuración del modelo Gemini
-rag.py:Carga de documentos, embeddings y recuperación
-prompt.py:Prompts del sistema y del agente
-workflow.py:Construcción del flujo del agente
-documentos: Archivos PDF utilizados como base de conocimiento
-env: Variables de entorno

## Flujo principal:

Usuario → Triaje → Decisión:
- Responder mediante RAG.
- Solicitar más información.
- Generar ticket de soporte.


# Uso del proyecto

## Requisitos previos

Antes de ejecutar el proyecto es necesario contar con:

- Python 3.10 o superior.
- Ollama instalado y ejecutándose.
- Modelo de embeddings BGE-M3 descargado en Ollama.
- Una API Key válida de Google Gemini.

## Instalación

## Instrucciones de uso

### Paso 1: Clonar el repositorio

Descargar el proyecto desde el repositorio utilizando el siguiente comando:

```bash
git clone <https://github.com/Fede-Giithub/Trabajo-Alura.git>
```

Luego ingresar a la carpeta del proyecto:

```bash
cd Proyecto-Alura
```

### Paso 2: Crear el entorno virtual

Crear un entorno virtual de Python para instalar las dependencias aisladas del proyecto:

```bash
python -m venv .venv
```

Activar el entorno virtual:

**Windows:**

```bash
.venv\Scripts\activate
```

### Paso 3: Instalar las dependencias

Instalar todas las librerías necesarias para ejecutar el proyecto:

```bash
pip install -r requirements.txt


### Paso 4: Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto.
Dentro del archivo agregar la API Key de Google Gemini:

```env
GEMINI_API_KEY=tu_api_key_de_google_gemini
```

### Paso 5: Configurar Ollama

Instalar Ollama y descargar el modelo de embeddings utilizado por el sistema:

```bash
ollama pull bge-m3
```

Verificar que el modelo se encuentre correctamente instalado:

```bash
ollama list
```
### Paso 6: Ejecutar la aplicación

Iniciar el asistente ejecutando:

```bash
python main.py
```

### Preguntas y respuestas realizadas:
===== Victory AI =====
Escribí tu consulta. Para salir escribí 'salir'.

 Usuario: ¿Cuánto tarda un envío?

--------------- Agente Victory ----------------
¡Hola! Con gusto te cuento sobre los tiempos de envío.

Primero, tené en cuenta que preparamos tu pedido para el despacho, lo que nos lleva entre **1 y 3 días hábiles**. En épocas de promociones o mucha demanda, este plazo podría extenderse un poquito.

Una vez que tu paquete sale de nuestro depósito, los tiempos de entrega estimados son:

*   **Capital y grandes ciudades:** entre 2 y 5 días hábiles.
*   **Ciudades del interior:** entre 3 y 10 días hábiles.
*   **Zonas alejadas o de difícil acceso:** el plazo puede ser de hasta 15 días hábiles.

Estos plazos son estimativos y pueden variar por causas ajenas a Victory.

¡Espero que esta información te sea útil! Si tenés alguna otra pregunta, no dudes en consultarme.

 Usuario: Quiero devolver mi producto.

--------------- Agente Victory ----------------
¡Hola! Con gusto te ayudo con tu devolución.

Para que podamos aceptar la devolución de tu producto, es importante que cumpla con estas condiciones:

*   Debe estar sin uso.
*   Debe conservar su embalaje original.
*   Debe incluir todas las etiquetas, accesorios y manuales, si los traía.
*   No debe presentar daños ocasionados por el cliente.
*   Necesitamos el comprobante de compra o el número de pedido.
*   La devolución debe solicitarse dentro del plazo establecido en nuestra Política de Reembolso y Devoluciones.

Ten en cuenta que hay algunos productos que no podemos aceptar para devolución, como:

*   Productos de uso personal que ya hayan sido utilizados.
*   Artículos personalizados o hechos a pedido.
*   Productos dañados por un mal uso del cliente.
*   Productos comprados en liquidación o con descuento especial, a menos que tengan alguna falla de fabricación.

Si tu producto cumple con las condiciones, ¡adelante! Si necesitas más detalles o tienes alguna otra pregunta, no dudes en consultarme.

 Usuario: Mi pedido nunca llegó y necesito hablar con un asesor.

--------------- Agente Victory ----------------
Se generó un ticket de soporte.

Usuario: ¿Quién ganó el Mundial 2022?

--------------- Agente Victory ----------------
Hola,

No encontré información sobre quién ganó el Mundial 2022 en los documentos que tengo.

¿Hay algo más en lo que pueda ayudarte con respecto a Victory?

 Usuario: salir

 Victory: ¡Hasta luego!


### Evidencia
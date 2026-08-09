# Urban Routes - Pruebas automatizadas

## Descripción del proyecto

Este proyecto contiene pruebas automatizadas para la aplicación web Urban Routes.

El objetivo es comprobar el flujo principal de solicitud de un taxi, incluyendo la configuración de la ruta, selección de la tarifa Comfort, confirmación del número de teléfono, vinculación de una tarjeta bancaria, configuración de opciones adicionales y solicitud del taxi.

## Tecnologías utilizadas

- Python
- Selenium WebDriver
- Pytest
- Google Chrome
- Git y GitHub

## Técnicas utilizadas

Durante las pruebas automatizadas se utilizaron las siguientes técnicas:

- Localización de elementos mediante ID y XPath.
- Esperas explícitas con `WebDriverWait`.
- Validación de datos mediante `assert`.
- Automatización de formularios.
- Selección de opciones de la aplicación.
- Obtención del código de confirmación telefónica mediante los registros de rendimiento del navegador.
- Automatización de la vinculación de una tarjeta bancaria.
- Ejecución de pruebas mediante Pytest.

## Flujo probado

La prueba automatizada realiza las siguientes acciones:

1. Abrir Urban Routes.
2. Introducir la dirección de origen.
3. Introducir la dirección de destino.
4. Seleccionar la tarifa Comfort.
5. Introducir el número de teléfono.
6. Obtener y confirmar el código SMS.
7. Agregar una tarjeta bancaria.
8. Introducir un mensaje para el conductor.
9. Seleccionar la opción "Manta y pañuelos".
10. Agregar dos helados.
11. Solicitar el taxi.

## Cómo ejecutar las pruebas

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
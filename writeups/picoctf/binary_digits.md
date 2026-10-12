# Binary Digits
**PicoCTF / Forensics / Fácil / 12 de octubre de 2026**

## Resumen
El desafío proporciona un archivo sin extensión que aparenta ser ruido binario (solo 1s y 0s). El objetivo fue identificar la verdadera naturaleza del archivo y decodificar su contenido para revelar una imagen oculta con la flag.

## Reconocimiento
Al descargar el archivo `digits.bin`, evité asumir su formato y utilicé la terminal de Kali para analizarlo:
- Ejecuté `file digits.bin`, lo que arrojó: `ASCII text, with very long lines (65536), with no line terminators`.
- Esto confirmó que no era un binario compilado, sino un archivo de texto plano de 8192 bytes (65536 bits) codificado en caracteres '0' y '1'.

## Proceso de resolución
1. Con la certeza de que era texto binario, utilicé **CyberChef**.
2. Cargué un fragmento inicial del texto y apliqué la receta **"From Binary"**.
3. El output reveló una cadena con la cabecera `ÿØÿà JFIF`, lo que corresponde a los "Magic Bytes" (firma de archivo) de una imagen JPEG (`FF D8 FF E0` en formato hexadecimal).
4. Sabiendo esto, cargué el archivo completo en CyberChef con la misma receta.
5. Exporté el resultado (Save to file) asignándole manualmente la extensión correcta `.jpg`.

## Solución
Al abrir la imagen resultante en el entorno de Kali, se visualiza directamente la bandera del desafío.
- **Flag:** academy{h1dd3n_1n_th3_b1n4ry_1b150ee9}

## Qué aprendí
- **Nunca confiar en las extensiones de los archivos.** La herramienta `file` es el primer paso obligatorio en Forense.
- **Identificación de Magic Bytes:** Reconocer cabeceras comunes como `JFIF` es vital para saber qué estamos decodificando realmente.
- **CyberChef** es extremadamente rápido para transformar data en crudo a archivos funcionales sin necesidad de escribir un script en Python para la conversión.

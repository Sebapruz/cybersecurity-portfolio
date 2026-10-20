# Caesar Reloaded
**Hack4u CTF / Criptografía / Fácil / Abril 2026**

## Resumen
Durante el CTF de Hack4u, se presentó un desafío de criptografía básica. El objetivo era descifrar un mensaje interceptado que utilizaba una variante del clásico cifrado César. Se nos entregó el texto cifrado y se nos indicó que la bandera (flag) seguía el formato estándar de la plataforma (`H4U{...}`).

## Reconocimiento
El mensaje cifrado interceptado fue el siguiente:
`O4B{jhlzhy_uv_lz_zbmpjplualtlual_zlnbyv}`

Al inspeccionar la cadena, el primer paso en cualquier incidente o desafío de criptografía es buscar patrones estandarizados conocidos. Dado que sabemos que todas las flags de este CTF comienzan con el prefijo `H4U{`, podemos deducir que la cadena inicial `O4B` corresponde directamente a `H4U` tras haber sido sometida al algoritmo de cifrado. 

## Proceso de resolución
Para resolver este reto sin recurrir a la fuerza bruta a ciegas, apliqué un **Ataque de Texto Plano Conocido (Known-Plaintext Attack - KPA)**. Esta técnica de criptoanálisis es muy efectiva cuando el analista conoce o puede predecir una parte del mensaje original (el texto plano), lo que permite aplicar ingeniería inversa para descubrir la clave de desplazamiento.

1. **Cálculo del desplazamiento (Shift):** 
   - Comparamos la primera letra del texto cifrado (`O`) con la primera letra esperada (`H`). En el alfabeto inglés, la distancia entre 'O' y 'H' representa un desplazamiento de 19 posiciones hacia adelante (o 7 posiciones hacia atrás).
   - Para validar nuestra hipótesis matemática, comparamos la tercera letra (`B`) con la esperada (`U`). Nuevamente, de la 'B' a la 'U' existe un desplazamiento exacto de 19 posiciones. (El número '4' se mantiene intacto, lo cual es común en cifrados César básicos que solo procesan caracteres alfabéticos).
    
2. **Automatización de la decodificación:**
   - En lugar de hacer el proceso de mapeo manualmente para toda la cadena, utilicé [CyberChef](https://gchq.github.io/CyberChef/) para automatizar la tarea.
   - Apliqué la operación `ROT13` (Rotación) y modifiqué el valor de rotación ("Amount") específicamente a `19`.
   - Al ingresar el texto cifrado completo, la herramienta aplicó el desplazamiento exacto a cada carácter alfabético de la cadena de forma automática.

## Solución
Tras aplicar el desplazamiento de 19 posiciones a toda la cadena, la bandera obtenida fue:
`H4U{...}` *(oculta intencionalmente)*

## Qué aprendí
- **Cifrado César:** Reforcé el concepto de algoritmos de sustitución monoalfabética por desplazamiento, uno de los métodos de cifrado más antiguos.
- **Ataque de Texto Plano Conocido (KPA):** Puse en práctica cómo la predicción de metadatos o formatos estandarizados (como el prefijo de una flag) compromete por completo la seguridad de cifrados simples, permitiendo deducir la clave matemática sin necesidad de fuerza bruta iterativa.
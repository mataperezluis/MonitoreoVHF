## Monitoreo y Registro de una red VHF con python

### Etapa 1: 
Construir el sistema de acondicionamiento de la señal de audio y decodificación de tonos
El sistema se diseñó para un radio Motorola GM300 el cual posee un conector de 16 pines para conexión de accesorios:
	
![](/imagenes_informe/pin_radio.jpg)

	Fig 1. Conector de accesorios visto desde la parte trasera del radio

![](/imagenes_informe/pin_radio2.png)

	Fig 2. Pines utilizados del conector de accesorios

Pin 2: Audio Tx proveniente del micrófono
Pin 3: PTT del Microfono
Pin 7: GND
Pin 11: Audio Rx proveniente del Receptor
	A través de los Pines 2 y 11 se obtiene la señal de audio a grabar, el valor de voltaje del Pin 3 permite saber si el radio se encuentra transmitiendo o recibiendo audio, si el voltaje del Pin 3 es 5 [V], el radio se encuentra recibiendo y la señal de audio se obtendrá por el Pin 11, si el voltaje del Pin 3 es 0 [V], el radio se encuentra transmitiendo y la señal de audio se obtendrá por el Pin 2.
	El circuito desarrollado consiste en un conmutador que selecciona la entrada de audio habilitada, un filtro pasa-banda de 300[Hz] a 3000[Hz]  y un buffer para acoplamiento de impedancias.
	Para el circuito conmutador se utilizo el CI 4066, que es un multiplexor analógico. Este circuito contiene 4 interruptores los cuales se cierran cuando el voltaje en el pin de control es un uno lógico.
	
	

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/mataperezluis/MonitoreoVHF/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

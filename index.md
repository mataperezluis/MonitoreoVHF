## Monitoreo y Registro de una red VHF con python

### Etapa 1: 
Construir el sistema de acondicionamiento de la señal de audio y decodificación de tonos
El sistema se diseñó para un radio **Motorola GM300** el cual posee un conector de 16 pines para conexión de accesorios:
	
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
 
 ![](/imagenes_informe/pin_4066.png)
 
 	Fig.3 Circuito Integrado 4066

Este circuito permite seleccionar la entrada de audio de acuerdo al siguiente diagrama:

 ![](/imagenes_informe/diagrama_circuito.png)

	Fig. 4  Diagrama de Conexión circuito conmutador
	
	

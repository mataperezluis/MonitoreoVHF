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
	

Se configuro un transistor bipolar en corte y saturación para que sirva como control de los interruptores permitiendo el paso de la señal de audio deseada. El circuito cuenta con un regulador de voltaje 7805 por lo que puede ser alimentado con voltajes de 5[V] a 17[V].

**Diseño del Filtro Pasa-Banda**
	El espectro de frecuencias de la voz humana va desde los 300[Hz] a los 3000[Hz], en esta rango también se encuentran los tonos DTMF así que se decidió, diseñar un filtro que solo deje pasar los sonidos en esta banda de frecuencias.
	Este filtro se diseño utilizando filtros activos con ayuda del software FilterPro Desktop de la compañía Texas Instruments, este software es proporcionado de manera gratuita por la compañía a través de su pagina web http://focus.ti.com/docs/toolsw/folders/print/filterpro.html
	
 ![](/imagenes_informe/filtro_1.png)
 
 	Fig. 5 FilterPro Desktop
	
 Al proporcionarle alguna información como tipo de filtro, frecuencias de corte, ganancia, entre otros, el software genera el circuito del filtro con valores comerciales de resistencias y capacitores, además de realizar una simulación de la respuesta en frecuencia del filtro. 
 Para la alimentación del circuito era necesario que se utilizara una sola fuente por cuestiones de espacio y economía, lo que llevo a diseñar los amplificadores operacionales para que trabajaran con alimentación  simple. Para lograr esto se realizaron algunos cambios al circuito original del filtro, sustituyendo la tierra del circuito por una tierra virtual, y aplicando un nivel DC de Vcc/2 a la señal de entrada.
 
![](/imagenes_informe/filtro_2.png)
  
  	Fig.6  Reporte del filtro generado por FilterPro Desktop

![](/imagenes_informe/filtro_4.png)
  
  	Fig.7  Simulación del Filtro Generada por FilterPro Desktop
	
	
	
	

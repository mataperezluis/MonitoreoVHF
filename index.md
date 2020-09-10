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
	

La conexión entre el radio y el circuito de control se realizo a través de un cable de red, a continuación se muestra el diagrama de conexión entre el radio y el circuito de control

![](/imagenes_informe/diagrama_conn.png)
	
	Fig.8  Diagrama de conexión 

La conexión entre el circuito y la tarjeta de sonido de la computadora se realizo con un conector  Jack de 3.5mm.

**Sistema de Decodificación de tonos DTMF**
 Se tomo la decisión de realizar la detección de los tonos DTMF por medio de software, para de esta manera ahorrar espacio y dinero, el software se desarrollo en software libre, utilizando el lenguaje de programación Python, esta basado en una implementación del algoritmo de Goertzel.
 El código DTMF puede estar al principio, al final o en ambos lugares de una radiocomunicación, dependiendo de la programación del radio, por lo tanto solo se analizan los primeros, y los últimos segundos, de la radio comunicación, no se analiza todo el audio para evitar la aparición de falsos positivos y reducir el tiempo de procesamiento.
 Esta decodificación aunque es muy rápida no se hace en tiempo real, se hace  con archivos .WAV de 16-bits, un canal y 8000[Hz] de frecuencia de muestreo. El software de grabación de audio debe adaptarse a esto y guardar el principio y el final de cada radiocomunicación para que pueda ser analizada.
El software toma el archivo de audio a ser analizado lo divide en muestras de 16 bits cada una y las procesa con el algoritmo de Goertzel, luego realiza una limpieza para eliminar falsos positivos, antes de retornar el código detectado. 
 La clase DTMFdetector realiza el análisis del audio el método getDTMFfromWAV() abre el archivo a analizar, el método goertzel() realiza la detección de los tonos.
 
![](/imagenes_informe/diagrama_conn.png)
 
	Fig.9  Diagrama de conexión
	
	
## Etapa 2: 
 Desarrollar una aplicación basada en software libre que permita la grabación del audio y los datos de identificación de cada radiocomunicación (Id, hora fecha) 
 Para el desarrollo de esta aplicación se utilizó el lenguaje de programación Python, la versión elegida fue la 2.6 la cual es completamente compatible con la licencia GPL, la interfaz grafica se desarrollo utilizando el software Qt4 Designer también software libre.
 El sistema operativo elegido fue la distribución de GNU/Linux Debian 6 Squeeze, la cual brinda gran seguridad, estabilidad, es rápido y ligero en memoria, capaz de realizar varios procesos al mismo tiempo y con gran rapidez esencial en el procesamiento de audio.
 El software permite monitorear varias entradas de audio al mismo tiempo, el control de la grabación se realiza por volumen, la grabación del audio se realiza en formato .ogg.
 
**Base de Datos**
 Se diseño una base de datos en MySQL para almacenar todos los datos de cada radio comunicación, tono DTMF identificador del radio que realiza la llamada, hora, fecha, ruta en donde se encuentra el archivo de audio y el radio base desde el cual se realizo la grabación.

 ![](/imagenes_informe/diagram_base.png)
 
	Fig.10  Modulo Grabador – Modelo Entidad Relación
	

## Etapa 3: 
 Desarrollar una interfaz gráfica basada en software libre que permita el monitoreo de la información
 
 Esta aplicación se desarrollo utilizando el lenguaje de programación Python  permite consultar los datos guardados, por fecha, cargo del usuario, código del radio, y nombre del radio base, puede reproducir el audio almacenado y revisar las estadísticas de uso de cada radio base por año o por mes, esta aplicación genera un grafico de barras indicando la cantidad de llamadas realiza en un periodo de tiempo determinado, también genera una imagen en formato .png de este grafico para que pueda ser utilizado en otras aplicaciones.
 
## Manual de usuario

primero hay que crear la base de datos con el archivo creaBasesDatos.txt

Modulo Grabador este programa permite la grabación de audio controlada por volumen y la detección de tonos DTMF.

Para ejecutar el programa desde la terminal se debe acceder a la carpeta donde se encuentran los archivos y escribir  >>python2.6 __init__.py

![](/imagenes_informe/pant_grabador.png)
 
	Fig.11  Pantalla Principal
	

La pantalla principal contiene el menú de usuario y permite ver si se encuentra realizando una grabación y también los tonos DTMF detectados. 

Lo primero que se debe hacer antes de empezar a realizar grabaciones es ingresar un radio a la base de datos esto permitirá asociar las grabaciones realizadas a un radio-base, para hacerlo se va al menú Herramientas>Ingresar Radio.

![](/imagenes_informe/pant_usr.png)
 
	Fig.12  Ingresar Radio

En Nombre se coloca un nombre que permita identificar al radio.

En ubicación se selecciona la ubicación del radio geográfica del radio estas deberán ser cargadas a la base de datos manualmente por el administrador del programa.

En Modelo y serial se ingresan el modelo y el número de serial del radio-base.

Para comenzar a monitorear una entrada de audio, se crea una conexión nueva, en el menú Acciones>Nueva Conexión esto abrirá la pantalla propiedades que permite fijar la propiedades de la nueva conexión.

![](/imagenes_informe/pant_main.png)
 
	Fig.13  Pantalla Propiedades

En esta pantalla se puede elegir el dispositivo por el cual se realizara la adquisición de datos, en Lista de Dispositivos aparecerá una lista con todos los dispositivos disponibles.  
En Ruta se coloca la ruta de la carpeta del sistema donde se guardara, los archivos de audio, el botón [+] abre una ventana que permite elegir o crear una carpeta de manera grafica.
La barra nivel de inicio indica la nivel de volumen que debe superar el audio para que se empiece a realizar una grabación 
La barra nivel final indica el nivel mínimo de volumen  que debe tener el audio de entrada para que la grabación continúe, si el volumen baja de este punto la grabación se detendrá y se realizara el proceso de detección de tono DTMF.
En la opción Radio se desplegara una lista con todos los radio-base disponibles, debe haber al menos un radio base cargado en la base de datos para que se realice la grabación.

Para agregar usuarios a la base de datos se utiliza el menú Herramientas>Agregar Usuario esto permitirá asociar un radio y su tono DTMF a una persona. 

En Código se agrega el código DTMF que identifica al radio asignado.
En Nombre, Apellido y Cargo van los datos de la persona a la cual se le asigno el radio.
En Modelo y serial se ingresan el modelo y el número de serial del radio.
Modulo Monitoreo este programa permite consultar los datos guardados y reproducir el audio de las grabaciones, además permite saber las estadísticas de uso de un determinado radio-base en un periodo de tiempo.


![](/imagenes_informe/pant_monitor.png)
 
	Fig.14  Pantalla Monitoreo

 En esta pantalla se visualizan todos los datos de una radio comunicación se puede consultar por Radio: Nombre del radio base a través del cual se realizo la grabación, Código el código DTMF identificador del radio, Cargo el cargo del usuario que realizo la llamada, se pude consultar por fecha o no, solo con marcar o desmarcar el botón consultar por fecha, si estos campos se dejan en blanco el programa mostrara todas las llamadas realizadas.

 Al presionar el botón buscar aparecerán todas las llamadas almacenadas en la base de datos que coincidan con la búsqueda realizada, el botón reproducir abrirá un reproductor de audio que permite escuchar la grabación.

![](/imagenes_informe/pant_grabador_f.png)
 
	Fig.15  Pantalla Monitoreo Funcionando


La pestaña estadísticas permite consultar las estadísticas de uso de un radio-base en un tiempo determinado, puede consultar la información por años, o meses de un año, el sistema mostrara un grafico de barras con el número de llamadas grabadas a través del radio-base determinado, el programa guardara una imagen en formato .png del grafico para que pueda ser utilizado en otras aplicaciones.

el informe completo sobre éste sistema se puede descargar desde [informe](https://drive.google.com/file/d/1d-Ca0kUcSWiV4yGMPNNpxaiM6wOeb7YQ/view?usp=sharing)


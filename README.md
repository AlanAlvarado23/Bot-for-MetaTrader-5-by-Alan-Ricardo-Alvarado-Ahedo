# Bot for MetaTrader 5 by Alan Ricardo Alvarado Ahedo
**About**: Autonomous bot for trading in Python: trades in the stock market by MetaTrader 5 platform

## English
**Code autor**: Alan Ricardo Alvarado Ahedo

**Estrategy author**: Laura Gabriela Ahedo Lugo


### Problem analysis
There's a few ways to trade into stock market. The easiest way is to trade manually and at
the moment, but it have three important disadvantages:
1. You have to spend your time making an analysis and watching how is the market going,so, it can take a lot of time and it can be very tiring.
2. This one, we consideer that is the most important because it can cause a negative result. The thing is, when you're making an analysis, it can be scary because you have the risk to loose your money, so it can make influence your decision and make a bad game; in less words, trade manually can be subjective.
3. The last problem, you can only trade when your time allow it; so it can be only less than 8 hours if we consideer 16 hours for basic needs and personal things, including that you don't have job.

That's why we made this bot, it follow a strategy and algorithm step by step and its objective, and the most comfortable feature, it's autonomous, so you can take a great cup of coffee while you are making money and all the time, even 24 hours a day every day of the whole year.


### Code description
It's an autonomous bot that trades in the stock market by MetaTrader 5 platform; this one make a conection to the platform via "MetaTrader5" Python library developed by themselves; this library can be installed by "pip". It have different classes, functions and methods which return a lot of data, many of these, helps to trade automatically and realize a make a own and customized strategy or analysis.

#### Trading strategy
This method have 3 important sections: the crossing, distance and operation:

1. **Crossing**: In this station, it makes an analysis at real-time of the stock market. In this case, it gets the candles of a section, then, calculates two indicators of mooving average, the first is an exponential mooving average of 5 periods and the second one is simple mooving average of 20 periods. This functions is calculated with the closes of each candle, and it's executed with Pandas library. This indicators smooth the path of the market. Finally, it search for a cross of the indicator of 5 periods cross the 20 periods, depending on the direction if this, is where it will go into operation.
2. **Distance**: The target of this part is that the distances of each indicator be more or equal than the distance specified on the strategy file named ``config.txt``, if and only if the indicator doesn't make another cross to the other direction. Finally, when this conditional are true, it send an order (operation).
3. **Operation**: In this stage, only watch the order at real-time, keeping the profit between the stop loss and take profit, when it's not, the bot close the order.

The first step of the bot is synchronize itself to the market temporality, then, obtains the data to be processed in order to detect that the 3 sections are fullfill. Then, it send the order to be monitored until get an estimated profit, either in profit or loss. Finally, it saves data like local and broker start and finish date, maximums and minimums, etcetera. It's important to recall that this is only an abstract of the whole code.

Thanks to the automatization and the absence of the human interpretation, we conclude that this strategy doesn't profitable, because the relation win/loss operations are very big. however, we're finding and searching better strategies and methods to be profitable; even using Deep Learning models if it improves the results.


## Español
**Autor de código**: Alan Ricardo Alvarado Ahedo

**Autora de estrategia**: Laura Gabriela Ahedo Lugo


### Análisis del problema
Existen diferentes maneras de operar en la bolsa de valores. La más fácil es manualmente, sin embargo, tiene tres importantes desventajas:
1. Tienes qué gastar tiempo para hacer un analisis y observar cómo se mueve el mercado a tiempo real, por lo tanto puede ser cansado y tomar mucho tiempo.
2. Esta desventaja la considero de las más importantes, pues puede ser perjudicial. Y es que cuando estás haciendo un análisis, puede resultar aterrador operar, ya que es nuestro dinero el que está en riesgo. Esto puede provocar que nos dejemos llevar por este miedo y tomar decisiones negativas o no las más óptimas para el objetivo que queremos; en pocas palabras, puede haber error humano.
3. La última desventaja es que solo podemos operar cuando nuestro tiempo nos lo permite; lo cual puede ser menos de 8 horas, si consideramos 16 horas para necesidades básicas y las personales, incluyendo el factor de que no contamos con un trabajo.

Es por eso que realizamos este bot, sigue una estrategia y un algoritmo paso y es objetivo; sin error humano, y la mejor parte, es que es autónomo, por lo cual podemos tomar una taza de café mientras generas ganancias todo el tiempo las 24 horas del día todos los días del año.


### Descripción del código
Es un bot autónomo que opera en la bolsa de valores mediante la plataforma de MetaTrader 5; este se conecta a la plataforma mediante la consola instalada del software de dicha plataforma. Esta conenxión se realiza mediante la librería "MetaTrader5", desarrollada por ellos mismos y se instala mediante Pip. Esta librería tiene diferentes clases, funciones y métodos los cuales devuelven diferentes datos, los cuales muchos permiten el trading de manera autónoma así como también realizar análisis propios y personalizados.

#### Estrategia de operación
En esta estrategia consta de 3 secciones cruciales: cruce, distancia y operación.
1. **Cruce**: En esta sección se hace el análisis a tiempo real del mercado seleccionado, en este caso, se obtienen las velas a partir de una sección determinada por el y cantidad de velas, posteriormente, se calculan 2 indicadores de medias móviles, uno exponencial de 5 periodos, y otra simple de 20 periodos. Estas funciones son aplicadas con el cierre de cada vela y se ejecuta mediante una función de la librería pandas. Estas suavizan el trayecto del mercado. Después de esto, se busca que el indicador de 5 periodos cruce la de 20 periodos, dependiendo de la dirección de esta, es hacia donde entrará la operación.
2. **Distancia**: En este apartado, se busca que la distancia entre cada indicador sea mayor o igual a la estrategia indicada en el archivo ``config.txt``, siempre y cuando no se vuelva a presentar otro cruce en dirección contraria. Cuando la distancia se cumpla, entra la operación.
3. **Operación**: Aquí solo se maneja la operación, se vigila a tiempo real y de manera constante para que la pérdida o ganancia no sea mayor a la deseada y así, evitar cambios.

El bot lo que hace primero es sincronizarse a la temporalidad del mercado a la que se está operando, después obtener los datos y procesarlos para así, detectar que las 3 secciones de la estrategia se cumplan sucesivamente, después, dar el paso a meter una operación a la dirección correspondiente, después, se vigila dicha operación hasta llegar a una un profit estimado, ya sea en ganancia o pérdida. Finalmente se guardan en una base de datos sql datos estadísticos como hora local y bróker de inicio y final de la operación, máximos y mínimos, etc. Cabe destacar que esto es solo un resumen del código.

Gracias a la automatización y la ausencia de interpretaciones humanas, observamos y concluimos que esta estrategia no es rentable, ya que entre operaciones ganadas y pérdidas es complicado tener números negativos, sin embargo actualmente estamos buscando estrategias más seguras y efectivas; e incluso integrando métodos de Deep Learning si resulta mejor.

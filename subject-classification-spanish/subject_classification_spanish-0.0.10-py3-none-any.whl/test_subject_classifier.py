import unittest
from subject_classifier import SubjectClassifier

class TestSentimentAnalysis(unittest.TestCase):
        
    def test_classifier_normal(self):
        classifier = SubjectClassifier()

        text_text_politics = "La entrada en el 2020 ha comportado cambios en la edad de jubilación y en el cálculo de los años cotizados que se tienen en cuenta para determinar la prestación. Las medidas son de carácter automático, ya que forman parte de la reforma de 2011 que hace que la edad para jubilarse se retrase paulatinamente hasta llegar a los 67 años.  ADVERTISING  Todo esto se da mientras resta pendiente saber cuál será la subida de las prestaciones en el 2020, ya que aunque el Gobierno en funciones ha prometido que se subirán el 0,9% y no perderán poder adquisitivo, la medida no se tomará hasta que esté formado un Ejecutivo. En diciembre de 2019 en España se contabilizaban 6.089.294 pensiones de jubilación, con una prestación media de 1.143,55 euros mensuales.   Pensiones en 2020 Los cambios en la edad de jubilación  Respecto a la edad de jubilación, cada año se va retrasando en virtud del régimen establecido en la reforma de 2011 aprobada durante el mandato de José Luis Rodríguez Zapatero. De esta forma, en 2020 la edad legal ordinaria será de 65 años y 10 meses. Esta edad se aplicará a aquellos que han cotizado menos de 37 años.  Si una persona llega a los 65 años en 2020 y ha cotizado 37 años o más, ya podrá jubilarse con 65 años.  En el caso de la jubilación parcial, en la que se combina trabajo y prestación, el mínimo será de 61 años y 10 meses con 35 años o más cotizados; o de 62 años y 8 meses con 33 años cotizados.  Con cada año que pasa es necesaria más edad para acceder a la jubilación, tanto si se ha cotizado por encima o por debajo de los periodos de referencia  Con cada año que pasa es necesaria más edad para acceder a la jubilación, tanto si se ha cotizado por encima o por debajo de los periodos de referencia Pensiones en 2020 Los cambios en el cálculo de la pensión  Por lo que respecta al cálculo de la pensión que se cobrará la momento de jubilarse, en 2020 se tendrán en cuenta los últimos 23 años cotizados. Estos años cotizados conforman la base reguladora, que es la suma de las bases de cotización en dicho periodo. Hay que tener en cuenta que cuantos más años se tengan en cuenta es posible que se recorte más la pensión, ya que en los últimos años de vida laboral es cuando mejores salarios se suelen cobrar.   Esta es otra de las reformas introducidas con los cambios en las pensiones de la década anterior, momento hasta el que se tenían en cuenta los últimos 15 años trabajados. La idea es que para 2022 ya se tengan en cuenta los últimos 25 años cotizados. De esta manera, en 2021 se computarán los últimos 24 años trabajados y en 2022 los últimos 25 años cotizados.  La base reguladora de la pensión se obtiene de dividir los meses de los años exigidos por el divisor correspondiente La base reguladora de la pensión se obtiene de dividir los meses de los años exigidos por el divisor correspondiente (LV) En 2023 El recorte de las pensiones que viene  Otra de las medidas que tendrán un fuerte calado en el sistema es la llegada del factor de sostenibilidad, que se aplicará a partir de 2023 e irá recortando las nuevas pensiones, teniendo en cuenta que los pensionistas vivirán más. Dicha medida en un principio debía aplicarse en 2019.  El conjunto de medidas se puede consultar al detalle en la guía para la jubilación del Ministerio de Trabajo, Migraciones y Seguridad Social."
        
        print(text_text_politics)
        classesResult = classifier.classify(text_text_politics)
        print(classesResult)
        print("--------")
        self.assertGreater(classesResult["pensiones"], 0.01, "should now it talks about pensions")


        text_text_football =  "Buenas noticias para el Atlético de Madrid a expensas de que la crisis sanitaria provocada por el Covid19 permita volver a la actividad normal en todo el país y eso suponga también el regreso del fútbol. Sabiendo que ahora mismo no es lo más importante, la vuelta de la competición constataría que se ha podido superar esta pesadilla generada por el coronavirus. El caso es que, de momento, el Atlético de Madrid ya sabe que podrá contar con uno de sus hombres más importantes, con Álvaro Morata . El jugador ha aprovechado estas semanas de parón para recuperarse de la lesión que se produjo el pasado 11 de marzo en el partido que el equipo colchonero disputó ante el Liverpool en Anfield Road. Antes de esa cita, el futbolista se lesionaba 15 días antes del partido de ida de los octavos de final ante el Liverpool y tuvo que trabajar contrarreloj para recuperarse. Lo consiguió, claro, pero era evidente que estaba jugando con molestias. Encima, en el choque posterior ante el Sevilla se llevó varios golpes, uno en el glúteo y otro en una de sus piernas, que le hicieron ser seria duda para la cita de Anfield, a la que llegó mermado. De ahí que se acabase lesionando pese a marcar el gol de la victoria. Pues bien, el jugador ya cuenta con el alta médica, según explicó hace unos días el diario Marca. Eso quiere decir que ya está para entrenarse como el resto de compañeros, con algo más de intensidad, dentro del programa que el cuerpo técnico rojiblanco ha transmitido a los futbolistas. El futbolista se tuvo que recuperar en casa a cuenta del confinamiento, pero el club colchonero le puso a su disposición material de fisioterapia, presoterapia, crioterapia y electroestimulación para pasar este trance y cuenta con el seguimiento diario y asesoramiento de los profesionales del club, de los recuperadores del equipo así como del jefe de los servicios médicos."
        print(text_text_football)
        classesResult = classifier.classify(text_text_football)
        print(classesResult.keys())
        self.assertGreater(classesResult["fútbol"], 0.01, "should now it talks about futbol")
        print("--------")

        text_text_covid =  "Ni 24 horas. Es lo que ha durado el consenso que la ministra de Educación y Formación Profesional, Isabel Celaá, decía haber alcanzado con las comunidades autónomas para poner fin al año académico 2019/2020. Autonomías como Madrid, Andalucía, Murcia y País Vasco se han descolgado del acuerdo alcanzado este miércoles por la Conferencia Sectorial de Educación. Los Gobiernos del PP madrileño, andaluz y murciano no apoyan la promoción general de los alumnos. El PNV, por su parte, argumenta que tiene un propio plan para la finalización del curso en Euskadi. Así, los Ejecutivos autonómicos de Madrid y Murcia, liderados por los populares Isabel Díaz Ayuso y Fernando López Miras, respectivamente, no sólo no están de acuerdo con que los estudiantes puedan pasar de curso con carácter general. También han criticado que los alumnos de 4º de la ESO y 2º de Bachilleraro puedan obtener su título sin superar todas las materias. No se puede compartir la propuesta que establece, ni más ni menos, que se titule con asignaturas suspensas, argumentan. Es, por estos dos puntos en concreto, por los que no suscribirán el Acuerdo para el desarrollo del tercer trimestre del curso 2019/2020 y el inicio del curso 2020/2021. Sería injusto, un menosprecio al esfuerzo de los alumnos y una falta de respeto al enorme trabajo que están haciendo los docentes, explica, por su parte, Javier Imbroda, consejero de Educación de Andalucía, quien también se niega a firmar el plan de Celaá. Además, estos Gobiernos regionales del PP coinciden en que sería caótico que cada comunidad tomase diferentes decisiones en ese ámbito que pudieran generar desigualdades entre los alumnos, según comenta la consejera murciana, Esperanza Moreno. La ministra de Educación, Isabel Celaá, este miércoles en rueda de prensa. La ministra de Educación, Isabel Celaá, este miércoles en rueda de prensa. El PNV, pese a ver la intención del Ministerio de Educación con buenos ojos, tampoco rubricará el pacto porque son sólo orientaciones y el Gobierno vasco ya tiene una hoja de ruta propia para cerrar el año académico 2019/2020, haciendo uso de sus competencias en Educación. El 'aprobado para todos' de Celaá que permite titular con suspensos: dos meses sin 'tocar' los libros Joaquín Vera En tiempos de coronavirus, la tercera evaluación será un mero diagnóstico 'evaluado' siempre de manera positiva: repetir será la excepción. El acuerdo de Celáa Estas reacciones son consecuencia de que la ministra de Educación, Isabel Celáa, acordó con las comunidades autónomas que este curso académico no se extendería más allá de junio. Según ella, este miércoles en la Conferencia Sectorial, el máximo órgano de interlocución entre el Gobierno central y las regiones autonómicas en materia educativa, decidieron que todos los alumnos pasen de curso, pero no con la misma nota, fruto de la situación actual por la crisis del coronavirus. Y es que la manera de calificar a los alumnos depende, según este plan, del equipo docente de cada alumno. Así, los profesores de cualquier centro educativo que, en palabras de Celaá, son los que mejor conocen las aptitudes de sus alumnos, decidirán las calificaciones finales de cada estudiante basándose en las notas obtenidas por éste durante la primera y la segunda evaluación. No obstante, los alumnos seguirán cursando el tercere trimestre, que tendrá unas funciones especiales, como la de diagnosticar qué contenidos no quedan bien fijados para darlos el año que viene. Un alumna del colegio Estudio, realizando deberes. Un alumna del colegio Estudio, realizando deberes. La manera de evaluar se tomaría en una decisión colegiada en el marco que regulen las administraciones públicas autonómicas. Por ello, los consejeros de Educación no terminan de ver si sería justo que cada autonomía decida, mediante su propia legislación, cómo será este marco. Hemos pedido que se clarifiquen apartados para que no haya agravios con el resto de comunidades ni se generen desigualdades, ha detallado el consejero de Andalucía. La repetición de alumnos En cuanto a la decisión de que un estudiante repita el curso o no, desde el Ministerio de Educación confían plenamente en que los docentes califiquen a sus alumnos porque son los que mejor conocen sus capacidades. Pese a ello, siempre se va a intentar que el estudiante promocione, ya que las repeticiones serán muy excepcionales y, si fuera el caso, deberán estar sólidamente argumentadas y acompañadas con un plan de refuerzo. De hecho, Celaá ha insistido en la idea de que habrá actividades de evaluación que permitan que los alumnos que no hayan tenido notas satisfactorias en el primer y el segundo trimestre pueden mejorarlas en este tercero para poder promocionar. La disparidad que se pueda generar entre las comunidades, según argumentan los consejeros de Madrid, Andalucía, Murcia, en los criterios de decisión para que los profesores decidan si un alumno promociona o no es una injustica. Esto les empuja a no suscribir el acuerdo. Además, Galicia y Castilla y León -gobernadas por el PP- también se han sumado a estas quejas pero, por el momento, no se han descolgado del plan de Celaá."
        print(text_text_covid)
        classesResult = classifier.classify(text_text_covid)
        print(classesResult)
        self.assertGreater(classesResult["educación"], 0.01, "should now it talks about education")
        print("--------")
    
    def test_main_tags(self):
        classifier = SubjectClassifier(use_main_tags_only=True)

        text_text_politics = "La entrada en el 2020 ha comportado cambios en la edad de jubilación y en el cálculo de los años cotizados que se tienen en cuenta para determinar la prestación. Las medidas son de carácter automático, ya que forman parte de la reforma de 2011 que hace que la edad para jubilarse se retrase paulatinamente hasta llegar a los 67 años.  ADVERTISING  Todo esto se da mientras resta pendiente saber cuál será la subida de las prestaciones en el 2020, ya que aunque el Gobierno en funciones ha prometido que se subirán el 0,9% y no perderán poder adquisitivo, la medida no se tomará hasta que esté formado un Ejecutivo. En diciembre de 2019 en España se contabilizaban 6.089.294 pensiones de jubilación, con una prestación media de 1.143,55 euros mensuales.   Pensiones en 2020 Los cambios en la edad de jubilación  Respecto a la edad de jubilación, cada año se va retrasando en virtud del régimen establecido en la reforma de 2011 aprobada durante el mandato de José Luis Rodríguez Zapatero. De esta forma, en 2020 la edad legal ordinaria será de 65 años y 10 meses. Esta edad se aplicará a aquellos que han cotizado menos de 37 años.  Si una persona llega a los 65 años en 2020 y ha cotizado 37 años o más, ya podrá jubilarse con 65 años.  En el caso de la jubilación parcial, en la que se combina trabajo y prestación, el mínimo será de 61 años y 10 meses con 35 años o más cotizados; o de 62 años y 8 meses con 33 años cotizados.  Con cada año que pasa es necesaria más edad para acceder a la jubilación, tanto si se ha cotizado por encima o por debajo de los periodos de referencia  Con cada año que pasa es necesaria más edad para acceder a la jubilación, tanto si se ha cotizado por encima o por debajo de los periodos de referencia Pensiones en 2020 Los cambios en el cálculo de la pensión  Por lo que respecta al cálculo de la pensión que se cobrará la momento de jubilarse, en 2020 se tendrán en cuenta los últimos 23 años cotizados. Estos años cotizados conforman la base reguladora, que es la suma de las bases de cotización en dicho periodo. Hay que tener en cuenta que cuantos más años se tengan en cuenta es posible que se recorte más la pensión, ya que en los últimos años de vida laboral es cuando mejores salarios se suelen cobrar.   Esta es otra de las reformas introducidas con los cambios en las pensiones de la década anterior, momento hasta el que se tenían en cuenta los últimos 15 años trabajados. La idea es que para 2022 ya se tengan en cuenta los últimos 25 años cotizados. De esta manera, en 2021 se computarán los últimos 24 años trabajados y en 2022 los últimos 25 años cotizados.  La base reguladora de la pensión se obtiene de dividir los meses de los años exigidos por el divisor correspondiente La base reguladora de la pensión se obtiene de dividir los meses de los años exigidos por el divisor correspondiente (LV) En 2023 El recorte de las pensiones que viene  Otra de las medidas que tendrán un fuerte calado en el sistema es la llegada del factor de sostenibilidad, que se aplicará a partir de 2023 e irá recortando las nuevas pensiones, teniendo en cuenta que los pensionistas vivirán más. Dicha medida en un principio debía aplicarse en 2019.  El conjunto de medidas se puede consultar al detalle en la guía para la jubilación del Ministerio de Trabajo, Migraciones y Seguridad Social."
        
        print(text_text_politics)
        classesResult = classifier.classify(text_text_politics)
        print(classesResult)
        print("--------")
        self.assertGreater(classesResult["política"], 0.1, "should now it talks about politics")


        text_text_football =  "Buenas noticias para el Atlético de Madrid a expensas de que la crisis sanitaria provocada por el Covid19 permita volver a la actividad normal en todo el país y eso suponga también el regreso del fútbol. Sabiendo que ahora mismo no es lo más importante, la vuelta de la competición constataría que se ha podido superar esta pesadilla generada por el coronavirus. El caso es que, de momento, el Atlético de Madrid ya sabe que podrá contar con uno de sus hombres más importantes, con Álvaro Morata . El jugador ha aprovechado estas semanas de parón para recuperarse de la lesión que se produjo el pasado 11 de marzo en el partido que el equipo colchonero disputó ante el Liverpool en Anfield Road. Antes de esa cita, el futbolista se lesionaba 15 días antes del partido de ida de los octavos de final ante el Liverpool y tuvo que trabajar contrarreloj para recuperarse. Lo consiguió, claro, pero era evidente que estaba jugando con molestias. Encima, en el choque posterior ante el Sevilla se llevó varios golpes, uno en el glúteo y otro en una de sus piernas, que le hicieron ser seria duda para la cita de Anfield, a la que llegó mermado. De ahí que se acabase lesionando pese a marcar el gol de la victoria. Pues bien, el jugador ya cuenta con el alta médica, según explicó hace unos días el diario Marca. Eso quiere decir que ya está para entrenarse como el resto de compañeros, con algo más de intensidad, dentro del programa que el cuerpo técnico rojiblanco ha transmitido a los futbolistas. El futbolista se tuvo que recuperar en casa a cuenta del confinamiento, pero el club colchonero le puso a su disposición material de fisioterapia, presoterapia, crioterapia y electroestimulación para pasar este trance y cuenta con el seguimiento diario y asesoramiento de los profesionales del club, de los recuperadores del equipo así como del jefe de los servicios médicos."
        print(text_text_football)
        classesResult = classifier.classify(text_text_football,default_threshold=0.02,limit=4)
        self.assertGreater(classesResult["deporte"], 0.1, "should now it talks about futbol")
        print("--------")
        print(classesResult)
        print(classifier.obtain_raw_probabilities(text_text_football))


if __name__ == '__main__':
    unittest.main()
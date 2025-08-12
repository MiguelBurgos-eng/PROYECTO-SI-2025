import sqlite3

conn= sqlite3.connect('base_Conocimiento.db')

c=conn.cursor()

#Para borrar la tabla conocimiento, descomentar la siguiente línea
#c.execute('''DROP TABLE IF EXISTS conocimiento''')

# Para crear la tabla conocimiento, descomentar la siguiente línea
#c.execute('''CREATE TABLE IF NOT EXISTS conocimiento (id INTEGER PRIMARY KEY AUTOINCREMENT, pregunta TEXT NOT NULL, respuesta TEXT NOT NULL)''')  

# Insertar datos en la tabla conocimiento
'''
datos = [
    ('qué hace este proyecto', 'Este proyecto es un tipo Alexa, el cual tiene una base de conocimiento generada en SQLite.'),
    ('qué es sqlite', 'Una base de datos ligera'),
    ('de quién es este proyecto', 'Este proyecto esta hecho por Miguel Burgos, Diego Castillo y Alan Fernandez, Estudiantes de la Universidad Tecnológica de Mexico.'),
    ('con qué tecnologias se realizo este proyecto', 'Este proyecto se realizó con Python, SQLite y la librería de SpeechRecognition.'),
    ('qué es speech recognition', 'Es una librería de Python que permite el reconocimiento de voz.'),
    ('para qué materia se hizo este proyecto', 'Este proyecto se realizó para la materia de Sistemas Inteligentes.'),
    ('qué es un sistema inteligente', 'Un sistema inteligente es un sistema que puede aprender y adaptarse a su entorno.'),

    ('quién pinto la mona lisa', 'La Mona Lisa fue pintada por Leonardo da Vinci.'),
    ('qué es la teoria de la relatividad', 'Es una teoría física formulada por Albert Einstein que describe la gravedad como la curvatura del espacio-tiempo.'),
    ('quién compuso la novena sinfonia', 'La Novena Sinfonía fue compuesta por Ludwig van Beethoven.'),
    ('qué es la segunda guerra mundial', 'Fue un conflicto militar global que duró de 1939 a 1945 e involucró a la mayoría de las naciones del mundo.'),
    ('quién escribio cien años de soledad', 'Cien años de soledad fue escrita por Gabriel García Márquez.'),
    ('qué es el renacimiento', 'El Renacimiento fue un movimiento cultural y artístico que surgió en Europa entre los siglos XIV y XVII.'),
    ('cuál es el planeta mas grande del sistema solar', 'El planeta más grande del sistema solar es Júpiter.'),
    ('qué es el boson de higgs', 'Es una partícula subatómica que explica por qué otras partículas tienen masa.'),
    ('quién fue frida kahlo', 'Frida Kahlo fue una pintora mexicana reconocida por sus autorretratos y su estilo único.'),
    ('qué es el realismo magico', 'Es un estilo literario que mezcla elementos mágicos con la realidad cotidiana.'),
    ('qué es el big bang', 'Es la teoría científica que explica el origen del universo a partir de una gran explosión hace aproximadamente 13.8 mil millones de años.'),

    ('qué fue la revolución francesa', 'La Revolución Francesa fue un proceso político y social que tuvo lugar en Francia entre 1789 y 1799, que terminó con el Antiguo Régimen.'),
    ('quién fue napoleón bonaparte', 'Napoleón Bonaparte fue un militar y político francés que se convirtió en emperador de Francia y conquistó gran parte de Europa a principios del siglo XIX.'),
    ('qué fueron las cruzadas', 'Las Cruzadas fueron una serie de expediciones militares cristianas entre los siglos XI y XIII para recuperar Tierra Santa del control musulmán.'),
    ('qué fue el imperio romano', 'El Imperio Romano fue una de las civilizaciones más poderosas de la antigüedad que dominó gran parte de Europa, África y Asia durante varios siglos.'),
    ('quién fue julio césar', 'Julio César fue un militar y político romano que jugó un papel crucial en la transformación de la República Romana en el Imperio Romano.'),
    ('qué fue la guerra fría', 'La Guerra Fría fue un período de tensión geopolítica entre Estados Unidos y la Unión Soviética que duró desde 1947 hasta 1991.'),
    ('quién fue cleopatra', 'Cleopatra VII fue la última faraona del Antiguo Egipto, conocida por sus relaciones con Julio César y Marco Antonio.'),
    ('qué fue la revolución industrial', 'La Revolución Industrial fue un período de transformación económica y social que comenzó en Inglaterra en el siglo XVIII con la mecanización de la producción.'),
    ('quién descubrió américa', 'América fue descubierta por Cristóbal Colón el 12 de octubre de 1492, aunque ya estaba habitada por pueblos indígenas.'),
    ('qué fue el holocausto', 'El Holocausto fue el genocidio sistemático de aproximadamente seis millones de judíos por la Alemania nazi durante la Segunda Guerra Mundial.'),
    
    ('qué fue la revolución mexicana', 'La Revolución Mexicana fue un conflicto armado que comenzó en 1910 contra la dictadura de Porfirio Díaz y transformó el país política y socialmente.'),
    ('quién fue benito juárez', 'Benito Juárez fue un abogado y político mexicano de origen zapoteco que fue presidente de México y defendió la soberanía nacional.'),
    ('qué fue la conquista de méxico', 'La Conquista de México fue el proceso de invasión y dominación del Imperio Azteca por los españoles liderados por Hernán Cortés entre 1519 y 1521.'),
    ('quién fue miguel hidalgo', 'Miguel Hidalgo fue un sacerdote católico que inició la Guerra de Independencia de México con el Grito de Dolores el 16 de septiembre de 1810.'),
    ('qué fueron los niños héroes', 'Los Niños Héroes fueron seis cadetes del Colegio Militar que murieron defendiendo el Castillo de Chapultepec durante la invasión estadounidense de 1847.'),
    ('quién fue la malinche', 'La Malinche fue una mujer indígena que sirvió como intérprete y consejera de Hernán Cortés durante la conquista de México.'),
    ('qué fue el porfiriato', 'El Porfiriato fue el período de la historia de México durante el cual Porfirio Díaz gobernó el país de manera dictatorial de 1876 a 1911.'),
    
    ('quién escribió don quijote', 'Don Quijote de la Mancha fue escrito por Miguel de Cervantes Saavedra y es considerada la primera novela moderna.'),
    ('quién escribió hamlet', 'Hamlet fue escrita por William Shakespeare y es una de sus tragedias más famosas.'),
    ('qué es la divina comedia', 'La Divina Comedia es un poema épico escrito por Dante Alighieri que narra un viaje imaginario por el Infierno, Purgatorio y Paraíso.'),
    ('quién escribió la ilíada', 'La Ilíada fue escrita por Homero y es uno de los poemas épicos más antiguos de la literatura occidental.'),
    ('quién fue edgar allan poe', 'Edgar Allan Poe fue un escritor estadounidense famoso por sus cuentos de terror y misterio, como El Cuervo y Los Crímenes de la Calle Morgue.'),
    ('qué es el boom latinoamericano', 'El Boom Latinoamericano fue un fenómeno literario de los años 1960-1970 que dio a conocer mundialmente a autores como García Márquez y Vargas Llosa.'),
    ('quién escribió orgullo y prejuicio', 'Orgullo y Prejuicio fue escrito por Jane Austen y es una de las novelas más importantes de la literatura inglesa.'),
    
    ('quién fue isaac newton', 'Isaac Newton fue un físico y matemático inglés que formuló las leyes de la gravitación universal y las leyes del movimiento.'),
    ('qué es la evolución', 'La evolución es el proceso por el cual las especies cambian y se desarrollan a lo largo del tiempo, teoría propuesta por Charles Darwin.'),
    ('quién descubrió la penicilina', 'La penicilina fue descubierta por Alexander Fleming en 1928, revolucionando el tratamiento de infecciones bacterianas.'),
    ('qué es el adn', 'El ADN es la molécula que contiene la información genética de todos los seres vivos y determina las características hereditarias.'),
    ('quién fue marie curie', 'Marie Curie fue una científica polaca-francesa que fue pionera en el estudio de la radiactividad y ganó dos premios Nobel.'),
    ('qué son los agujeros negros', 'Los agujeros negros son regiones del espacio con una gravedad tan intensa que ni siquiera la luz puede escapar de ellos.'),
    ('qué es la fotosíntesis', 'La fotosíntesis es el proceso por el cual las plantas convierten la luz solar, agua y dióxido de carbono en glucosa y oxígeno.'),
    
    ('quién pintó la última cena', 'La Última Cena fue pintada por Leonardo da Vinci y se encuentra en el convento de Santa María de las Gracias en Milán.'),
    ('qué es el impresionismo', 'El impresionismo fue un movimiento artístico que surgió en Francia en el siglo XIX caracterizado por pinceladas sueltas y el uso de la luz.'),
    ('quién fue pablo picasso', 'Pablo Picasso fue un pintor español considerado uno de los artistas más influyentes del siglo XX y cofundador del cubismo.'),
    ('qué es la guernica', 'La Guernica es una pintura de Pablo Picasso que representa los horrores de la guerra, inspirada en el bombardeo de Guernica durante la Guerra Civil Española.'),
    ('quién esculpió el david', 'El David fue esculpido por Miguel Ángel Buonarroti y es una de las esculturas más famosas del Renacimiento.'),
    ('qué es el surrealismo', 'El surrealismo fue un movimiento artístico y literario que buscaba expresar el subconsciente y los sueños.'),
    
    ('quién compuso las cuatro estaciones', 'Las Cuatro Estaciones fueron compuestas por Antonio Vivaldi y son sus conciertos para violín más famosos.'),
    ('qué es una sinfonía', 'Una sinfonía es una composición musical para orquesta, generalmente en cuatro movimientos.'),
    ('quién fue wolfgang amadeus mozart', 'Wolfgang Amadeus Mozart fue un compositor austríaco del período clásico, considerado uno de los más grandes genios musicales de la historia.'),
    ('qué es el jazz', 'El jazz es un género musical que se originó en Nueva Orleans a finales del siglo XIX, caracterizado por la improvisación y los ritmos sincopados.'),
    ('quién compuso el lago de los cisnes', 'El Lago de los Cisnes fue compuesto por Pyotr Ilyich Tchaikovsky y es uno de los ballets más famosos del mundo.'),
    
    ('cuál es el río más largo del mundo', 'El río más largo del mundo es el río Nilo en África, con aproximadamente 6,650 kilómetros de longitud.'),
    ('cuál es la montaña más alta del mundo', 'La montaña más alta del mundo es el Monte Everest, con 8,848 metros de altura, ubicado en la cordillera del Himalaya.'),
    ('cuántos continentes hay', 'Existen siete continentes: Asia, África, América del Norte, América del Sur, Antártida, Europa y Oceanía.'),
    ('cuál es el océano más grande', 'El océano más grande es el Océano Pacífico, que cubre aproximadamente un tercio de la superficie terrestre.'),
    ('cuál es el desierto más grande', 'El desierto más grande del mundo es la Antártida, aunque si consideramos solo desiertos cálidos, es el Sahara en África.'),
    ('cuál es el país más pequeño del mundo', 'El país más pequeño del mundo es la Ciudad del Vaticano, con una superficie de solo 0.17 millas cuadradas.'),
    
    ('qué es la mitología griega', 'La mitología griega es el conjunto de mitos y leyendas de la antigua Grecia que explicaban el origen del mundo y las aventuras de dioses y héroes.'),
    ('quién era zeus', 'Zeus era el rey de los dioses en la mitología griega, dios del cielo y el trueno, y padre de muchos dioses y héroes.'),
    ('qué es la caja de pandora', 'La Caja de Pandora es un mito griego sobre la primera mujer, Pandora, quien abrió una caja que liberó todos los males del mundo.'),
    ('quién fue hércules', 'Hércules era un héroe de la mitología griega famoso por su fuerza sobrehumana y por completar los doce trabajos.'),
    
    ('quién fue sócrates', 'Sócrates fue un filósofo griego considerado uno de los fundadores de la filosofía occidental, maestro de Platón.'),
    ('qué es el existencialismo', 'El existencialismo es una corriente filosófica que enfatiza la existencia individual, la libertad y la responsabilidad personal.'),
    ('quién fue aristóteles', 'Aristóteles fue un filósofo griego discípulo de Platón, que hizo contribuciones fundamentales a la lógica, ética, política y ciencias naturales.'),
    
    ('quién inventó la imprenta', 'La imprenta de tipos móviles fue inventada por Johannes Gutenberg en el siglo XV, revolucionando la difusión del conocimiento.'),
    ('quién inventó el teléfono', 'El teléfono fue inventado por Alexander Graham Bell en 1876.'),
    ('quién inventó la bombilla', 'La bombilla incandescente práctica fue desarrollada por Thomas Edison en 1879.'),
    ('cuándo se inventó internet', 'Internet se desarrolló a partir de ARPANET en los años 1960-1970, pero la World Wide Web fue creada por Tim Berners-Lee en 1989.'),    
]'''
#Para agregar los datos a la tabla conocimiento, descomentar la siguiente línea
#c.executemany("INSERT INTO conocimiento (pregunta, respuesta) VALUES (?, ?)", datos)


#Para ver los datos insertados
c.execute("SELECT * FROM conocimiento")
x=(c.fetchall())
for i in x:
    print(i)


conn.commit()
conn.close()

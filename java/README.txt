En Geany crear un proyecto y especificar:

- Para compilar
  javac -cp "%p/build/:%p/build/lib/*" -d "%p/build" "%f"

- Para ejecutar
  java -cp "%p/build/:%p/build/lib/*" "%e"


Los directoriso corresponden a:

src/

    main/
        java/
            rcr/
                jplayground/
                    RobotBase.java      Clase base para los ronots
                    RobotEPuck.java     Clase para el robot tipo EPuck
                    RobotThymio2.java   Clase para el robot tipo Thymio2

    test/                           Programas de prueba
        java/
            TestCamera.java
            TestEnjambre.java
            TestLed.java
            TestSensorsObject.java
            TestSensorsSimple.java
            TestSensorsThread.java
            TestServerClient.java
            TestSumo.java

build/

    Test*.class

    lib/
        json-20210307.jar

    rcr/
        jplayground/
            Robot*.class

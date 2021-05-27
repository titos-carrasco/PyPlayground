En Geany:
    1) abrir RobotBase.java
    2) crear un proyecto
    3) modificar el comando de compilar a javac -cp "%p/build/:%p/build/lib/*" -d "%p/build" "%f"

Los directorios corresponden a:

src/
    main/
        java/
            rcr/
                jplayground/
                    RobotBase.java      Clase base para los ronots
                    RobotEPuck.java     Clase para el robot tipo EPuck
                    RobotThymio2.java   Clase para el robot tipo Thymio2

build/
    lib/
        json-20210307.jar

    rcr/
        jplayground/
            Robot*.class

En Geany:
    1) abrir TestSumo.java
    2) crear un proyecto
    3) modificar el comando de compilar a javac -cp "%p/../../java_client/build/" "%f"
    4) modificar el comando de ejecutar a java  -cp "%p/../../java_client/build/:%p/../../java_client/build/lib/*:%p" "%e"

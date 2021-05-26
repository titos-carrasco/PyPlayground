# ChangeLog

## v1.2.2 - 2021-05-26
### Changed
- Corrige cliente java para operar adecuadamente con fin de línea '\n' en Windows

### Removed
- Se eliminan los *.class de los commit


## v1.2.1 - 2021-05-26
### Changed
- Incorpora llamada al manejador de eventos de pygame en test_Camera.py
- Toda la operación de métodos y variables de los robots se lleva al hilo GUI - controlStep()


## v1.2.0 - 2021-05-25
### Changed
- Cambia bytearray a bytes
- Convierte a Clases los Tests

### Added
- Agrega Test para los sensores de distancia
- Agrega Cliente y pruebas en Java


## v1.1.0 - 2021-05-24
### Changed
- Modifica Test_Help para no incluir RobotFactory
- Simplifica Test_Led
- Simplifica retorno de sensores
- Cambia retorno None a dict en clases servidor (compatibel con JSON)
- Modifica retorno de imagen de la camara del EPuck para enviar solo bytes (no JSON)
- Simplifica invocacion del loop de pyenki


## v1.0.0 - 2021-05-23
### Changed
- Modifica cliente de robots para incorporar atributos para sus sensores
- Modifica archivos de pruebas para utilizar los atributos de sensores de cada robot
- Modifica README.md eliminando el changelog

### Added
- Agrega archivo Changelog-md

## @28a4244 - 2021-05-22
### Changed
- Corrige archivo README.md

## @c8f4c20 - 2021-05-22

### Changed
- Simplifica modulo cliente


## @f24b3f3 - 2021-05-22
### Added
- Agrega Test_Help.py para desplegar la documentaciín

### Changed
- Documentación las clases
- Refactoring simplificando la implementación

### Removed
- Elimina paquete Utils


## @257bd99 - 2021-05-20
### Changed
- Documenta las clases


## @fcc4cf6 - 2021-05-19
### Changed
- Refactoring y documentación de las clases


## @35d2cd1 - 2021-05-19
### Added
- Agrega soporte para la camara lineal del robot EPuck
- Agrega prueba para la cámara lineal del EPuck

### Changed
- Aumenta tamaño del buffer para la comunicación por sockets

### Fixed
- Corrige conversión de color desde los archivos .worlds a la clase Color de pyenki
- Corrige valor de transparencia en os archivos .worlds


## v0.5.0 - 2021-05-18
### Added
- Agrega soportta los los L>EDs de los robots
- Agrega pruebas para los LEDs
- Agrega pyenki.so al commit

### Changed
- Mueve archivo world.README al directorio raíz

### Fixed
- Corrige transparencia en los archivos .worlds
- Corrige archivo .gitignore


## @32d4826 - 2021-05-18
### Added
- Agrega archivo pyenki.pyd al commit


## @ 643c1a3 - 2021-05-18
### Added
- Agrega soporte para Windows
- Generado con Qt5.12.10
- Generado con Boost 1.76.0
- Testeado en Windows 10 realk/KVM/QENU

### Removed
- Elimina las operaciones non-blocking en los sockets

### Fixed
- Corrige codigo para QT y acceso a DLL


## @ 34e631a - 2021-05-18
### Added
- Primeras pruebas funcionales para Linux

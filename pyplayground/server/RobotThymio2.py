import server.linux.pyenki as pyenki
import server.RobotBase as RobotBase


class MyThymio2( RobotBase.RobotBase, pyenki.Thymio2 ):
    tipo = 'thymio2'

    #--- Constructor
    def __init__( self, name ):
        super().__init__( name )

    #--- Retorna un diccionario con el valor de sus sensores
    def getSensors( self ):
        sensors = {
            "pos":self.pos,
            "leftSpeed":self.leftSpeed,
            "rightSpeed":self.rightSpeed,
            "proximitySensorValues":self.proximitySensorValues,
            "proximitySensorDistances":self.proximitySensorDistances,
            "groundSensorValues":self.groundSensorValues,
            #"angSpeed":self.angSpeed,
            #"angle":self.angle,
            #"collisionElasticity":self.collisionElasticity,
            #"color":self.color,
            #"dryFrictionCoefficient":self.dryFrictionCoefficient,
            #"height":self.height,
            #"interlacedDistance":self.interlacedDistance,
            #"isCylindric":self.isCylindric,
            #"leftEncoder":self.leftEncoder,
            #"leftOdometry":self.leftOdometry,
            #"mass":self.mass,
            #"momentOfInertia":self.momentOfInertia,
            #"radius":self.radius,
            #"rightEncoder":self.rightEncoder,
            #"rightOdometry":self.rightOdometry,
            #"speed":self.speed,
            #"viscousFrictionCoefficient":self.viscousFrictionCoefficient,
            #"viscousMomentFrictionCoefficient":self.viscousMomentFrictionCoefficient
        }
        return { 'error': '', 'answer':{ 'sensors':sensors } }

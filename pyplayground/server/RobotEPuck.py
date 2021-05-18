import pyenki
import server.RobotBase as RobotBase


class MyEPuck( RobotBase.RobotBase,pyenki.EPuck ):
    tipo = 'epuck'

    #--- Constructor
    def __init__( self, name ):
        super().__init__( name )

    #--- Retorna un diccionario con el valor de sus sensores
    def getSensors( self ):
        sensors = {
            "pos":self.pos,
            "leftSpeed":self.leftSpeed,
            "rightSpeed":self.rightSpeed,
            "proximitySensorDistances":self.proximitySensorDistances,
            "proximitySensorValues":self.proximitySensorValues,
            #"angSpeed":self.angSpeed,
            #"angle":self.angle,
            #"cameraImage":self.cameraImage,
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

    def setLedRing( self, on_off ):
        super().setLedRing( on_off )
        return { 'error': '', 'answer':{} }

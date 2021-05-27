package rcr.jplayground;

import java.util.Map;
import java.util.ArrayList;

import org.json.*;

public class RobotThymio2 extends RobotBase {
    private float[] groundSensorValues = null;

    public RobotThymio2( String name, String host, int port ) throws Exception {
        super( name, host, port, "thymio2" );
    }

    public void getSensors()  throws Exception {
        Map<String, Object> map = retrieveSensors();
        groundSensorValues = getFloatArray( (ArrayList)map.get("groundSensorValues") );
    }

    public float[] getGroundSensorValues() {
        return groundSensorValues;
    }

    public void setLedsIntensity( float[] leds ) throws Exception {

        JSONObject json = new JSONObject();
        json.put( "cmd", "setLedsIntensity" );
        json.put( "leds", leds );
        out.print( json );
        out.print( '\n' );
        out.flush();

        String resp = in.readLine();
    }
}

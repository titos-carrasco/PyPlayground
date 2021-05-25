package rcr.jplayground;

import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import org.json.*;

public class RobotEPuck extends RobotBase {

    public RobotEPuck( String name, String host, int port ) throws Exception {
        super( name, host, port, "epuck" );
    }

    public void setLedRing( boolean on_off ) throws Exception {

        JSONObject json = new JSONObject();
        json.put( "cmd", "setLedRing" );
        json.put( "estado", on_off ? 1 : 0 );
        out.println( json );

        String resp = in.readLine();
    }

    public void getSensors() throws Exception {
        Map<String, Object> map = retrieveSensors();
    }

    public List<int[]> getCameraImage() throws Exception {
        JSONObject json = new JSONObject();
        json.put( "cmd", "getCameraImage" );
        out.println( json );

        int[] s = new int[4];
        for( int i = 0; i<4; i++ )
            s[i] = in.read();

        int len = (s[0]<<24) + (s[1]<<16) + (s[2]<<8) + s[3];

        int[] data = new int[len];
        for( int i = 0; i<len; i++ )
            data[i] = in.read();

        List<int[]> imagen = new ArrayList<>();
        for( int i=0; i<len; i+= 4 ) {
            int[] color = { data[i+0], data[i+1], data[i+2], data[i+3] };
            imagen.add( color );
        }

        return imagen;
    }

}

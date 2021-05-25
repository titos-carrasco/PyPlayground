package rcr.jplayground;

import java.util.Map;
import java.util.ArrayList;
import java.math.BigDecimal;

import java.net.Socket;
import java.io.PrintWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.json.*;

public class RobotBase {
    private String name;
    private String host;
    private int port;
    private String tipo;
    private Socket sock;
    protected PrintWriter out;
    protected BufferedReader in;
    private float[] pos = null;
    private float[] speed = null;
    private float[] proximitySensorValues = null;
    private float[] proximitySensorDistances = null;

    public RobotBase( String name, String host, int port, String tipo ) throws Exception {
        this.host = host;
        this.port = port;
        this.name = name;
        this.tipo = tipo;

        // nos conectamos al servidor de playground en donde esta el robot
        sock = new Socket( host, port );
        out = new PrintWriter( sock.getOutputStream(), true );
        in = new BufferedReader( new InputStreamReader( sock.getInputStream(), "iso-8859-1" ) );

        // solicitamos acceso enviando el nombre del robot
        out.println( name );

        // si es aceptado nos envia el tipo de robot
        String el_tipo = in.readLine();
        if( !this.tipo.equals( el_tipo ) )
            throw new Exception( "Robot no aceptado" );
    }

    public void close() {
        try {
            if( sock != null ) {
                out.close();
                in.close();
                sock.close();
            }
        }
        catch( Exception e ) {
        }
    }

    public String getName() {
        return name;
    }

    public float[] getPos() {
        return pos;
    }

    public float[] getSpeed() {
        return speed;
    }

    public float[]  getProximitySensorValues() {
        return proximitySensorValues;
    }

    public float[]  getProximitySensorDistances() {
        return proximitySensorDistances;
    }

    public void setSpeed( int leftSpeed, int rightSpeed ) throws Exception {
        JSONObject json = new JSONObject();
        json.put( "cmd", "setSpeed" );
        json.put( "leftSpeed", leftSpeed );
        json.put( "rightSpeed", rightSpeed );
        out.println( json );

        String resp = in.readLine();
    }

    protected Map<String, Object> retrieveSensors() throws Exception {
        JSONObject json = new JSONObject();
        json.put( "cmd", "getSensors" );
        out.println( json );

        String resp = in.readLine();

        json = new JSONObject( resp );
        Map<String, Object> map = json.toMap();

        speed = getFloatArray( (ArrayList)map.get("speed") );
        pos = getFloatArray( (ArrayList)map.get("pos") );
        proximitySensorValues = getFloatArray( (ArrayList)map.get("proximitySensorValues") );
        proximitySensorDistances = getFloatArray( (ArrayList)map.get("proximitySensorDistances") );

        return map;
    }

    protected float[] getFloatArray( ArrayList arr ) {
        int len = arr.size();
        float[] f = new float[ len ];

        for( int i=0; i<len; i++ ) {
            f[i] = ( (BigDecimal)arr.get(i) ).floatValue();
        }

        return f;
    }
}

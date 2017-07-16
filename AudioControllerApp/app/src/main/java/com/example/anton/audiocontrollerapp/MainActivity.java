package com.example.anton.audiocontrollerapp;

        import android.os.Bundle;
        import android.support.annotation.NonNull;
        import android.support.v7.app.AppCompatActivity;
        import android.support.v7.widget.LinearLayoutCompat;
        import android.view.View;
        import android.widget.LinearLayout;
        import android.widget.Toast;
        import android.widget.ToggleButton;

        import java.io.IOException;
        import java.io.InputStream;
        import java.io.InputStreamReader;
        import java.net.HttpURLConnection;
        import java.net.MalformedURLException;
        import java.net.URL;

        import com.android.volley.Request;
        import com.android.volley.RequestQueue;
        import com.android.volley.Response;
        import com.android.volley.VolleyError;
        import com.android.volley.toolbox.StringRequest;
        import com.android.volley.toolbox.Volley;

        import org.json.JSONArray;
        import org.json.JSONException;
        import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private LinearLayout mZonesContainer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mZonesContainer = (LinearLayout)findViewById(R.id.zonesContainer);
    }


    public void onButtonClick(View view) {

        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://192.168.0.105:8080/AudioController/api/v1/controller/zones";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        ProcessZones(response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(), "Response is: "+ error.toString(), Toast.LENGTH_LONG).show();
            }
        });

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    @NonNull
    private void ProcessZones(String response) {

        try {
            JSONArray zones = new JSONArray(response);
            int howMany = zones.length();
            Toast.makeText(getApplicationContext(), "Zones: "+ howMany, Toast.LENGTH_LONG).show();

            mZonesContainer.removeAllViews();

            for (int i = 0; i < zones.length(); i++) {
                JSONObject zone = zones.getJSONObject(i);
                String zoneName = zone.getString("Name");
                Boolean enabled = zone.getBoolean("Enabled");

                mZonesContainer.addView(createViewForZone(zoneName, enabled));
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }

        return ;
    }

    private View createViewForZone(String zoneName, Boolean enabled) {

        ToggleButton zoneToggle = new ToggleButton(getApplicationContext());
        zoneToggle.setChecked(enabled);
        zoneToggle.setText(zoneName);
        zoneToggle.setTextOn(zoneName);
        zoneToggle.setTextOff(zoneName);

        return zoneToggle;
    }


}

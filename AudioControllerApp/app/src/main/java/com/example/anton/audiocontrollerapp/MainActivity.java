package com.example.anton.audiocontrollerapp;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private LinearLayout mZonesContainer;
    private ControllerModel mController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mZonesContainer = (LinearLayout) findViewById(R.id.zonesContainer);
        mController = new ControllerModel(this, "http://192.168.1.43:8080");
    }


    public void onButtonClick(View view) {
        mController.requestZones(
                new Response.Listener<ArrayList<AudioZone>>() {
                    @Override
                    public void onResponse(ArrayList<AudioZone> zones) {
                        ProcessZones(zones);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(), "Error: " + error.toString(), Toast.LENGTH_LONG).show();
                    }
                });
    }

    private void ProcessZones(ArrayList<AudioZone> zones) {

        int howMany = zones.size();
        Toast.makeText(getApplicationContext(), "Zones: " + howMany, Toast.LENGTH_LONG).show();

        mZonesContainer.removeAllViews();

        for (int i = 0; i < zones.size(); i++) {
            AudioZone zone = zones.get(i);
            createViewForZone(zone);
        }

        return;
    }

    private void createViewForZone(final AudioZone zone) {

        View zoneView = this.getLayoutInflater().inflate(R.layout.zone_layout, mZonesContainer, false);

        ToggleButton zoneToggle = (ToggleButton) zoneView.findViewById(R.id.zoneEnabledToggle);
        zoneToggle.setTextOn(zone.getName() + " - ON");
        zoneToggle.setTextOff(zone.getName() + " - OFF");
        zoneToggle.setChecked(zone.getEnabled());

        zoneToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                zone.setEnabled(isChecked);
                mController.setZoneEnabled(zone);
            }
        });

        mZonesContainer.addView(zoneView);
    }


}

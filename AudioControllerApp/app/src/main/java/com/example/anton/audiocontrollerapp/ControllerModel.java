package com.example.anton.audiocontrollerapp;

import android.content.Context;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by anton on 10-Aug-17.
 */

public class ControllerModel {

    private Context mContext;
    private String mControllerUrl;

    public ControllerModel(Context context, String audioControllerUrl){
        if (context == null){
            throw new IllegalArgumentException("context must be provided");
        }

        mContext = context;
        mControllerUrl = audioControllerUrl;
    }

    public void requestZones(final Response.Listener<ArrayList<AudioZone>> successHandler, Response.ErrorListener errorHandler) {
        RequestQueue queue = Volley.newRequestQueue(mContext);
        String url = mControllerUrl + "/AudioController/api/v1/controller/zones";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(
                Request.Method.GET,
                url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        successHandler.onResponse((ArrayList<AudioZone>) ExtractZones(response));
                    }
                },
                errorHandler);

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    public String getControllerUrl() {
        return mControllerUrl;
    }

    public void setControllerUrl(String mControllerUrl) {
        this.mControllerUrl = mControllerUrl;
    }

    private List<AudioZone> ExtractZones(String response)
    {
        List<AudioZone> zones = new ArrayList<>();

        try {
            JSONArray zonesInJson = new JSONArray(response);

            for (int i = 0; i < zonesInJson.length(); i++) {
                JSONObject zoneJson = zonesInJson.getJSONObject(i);
                String zoneName = zoneJson.getString("Name");
                Boolean enabled = zoneJson.getBoolean("Enabled");

                AudioZone zone = new AudioZone();
                zone.setName(zoneName);
                zone.setEnabled(enabled);
                zones.add(zone);
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }

        return zones;
    }
}

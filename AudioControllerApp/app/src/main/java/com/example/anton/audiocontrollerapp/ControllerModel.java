package com.example.anton.audiocontrollerapp;

import android.content.Context;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by anton on 10-Aug-17.
 */

public class ControllerModel {

    static final String ZONES_URL = "/AudioController/api/v1/controller/zones";

    private Context mContext;
    private String mControllerUrl;
    private RequestQueue mQueue;

    public ControllerModel(Context context, String audioControllerUrl){
        if (context == null){
            throw new IllegalArgumentException("context must be provided");
        }

        mContext = context;
        mControllerUrl = audioControllerUrl;
        mQueue = Volley.newRequestQueue(mContext);
    }

    public String getControllerUrl() {
        return mControllerUrl;
    }

    public void setControllerUrl(String mControllerUrl) {
        this.mControllerUrl = mControllerUrl;
    }

    public void requestZones(final Response.Listener<ArrayList<AudioZone>> successHandler, Response.ErrorListener errorHandler) {
        String url = mControllerUrl + ZONES_URL;

        // Request a string response from the AudioController URL.
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

        mQueue.add(stringRequest);
    }

    public void setZoneEnabled(final AudioZone zone) {
        String url = mControllerUrl + ZONES_URL + "/" + zone.getID();

        JSONObject json = new JSONObject();
        try {
            json.put("Enabled", zone.getEnabled());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest putRequest = new JsonObjectRequest(Request.Method.PUT, url, json,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // response
                        Log.d("Response", response.toString());
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Log.d("Error.Response", "blah");
                    }
                }
        );

//            @Override
//            public Map<String, String> getHeaders() throws AuthFailureError {
//                HashMap<String, String> headers = new HashMap<String, String>();
//                headers.put("Content-Type", "application/json; charset=utf-8");
//                return headers;
//            }

            //@Override
            //protected Map<String, String> getParams() {
            //    Map<String, String> params = new HashMap<String, String>();
//
            //
//
            //    JSONObject json = new JSONObject();
            //    try {
            //        json.put("Enabled", enabled);
            //    } catch (JSONException e) {
            //        e.printStackTrace();
            //    }
//
            //    params.put("data", json);
//
            //    return params;
            //}

        //};

        mQueue.add(putRequest);
    }

    private List<AudioZone> ExtractZones(String response)
    {
        List<AudioZone> zones = new ArrayList<>();

        try {
            JSONArray zonesInJson = new JSONArray(response);

            for (int i = 0; i < zonesInJson.length(); i++) {
                JSONObject zoneJson = zonesInJson.getJSONObject(i);
                Integer zoneId = zoneJson.getInt("ZoneId");
                String zoneName = zoneJson.getString("Name");
                Boolean enabled = zoneJson.getBoolean("Enabled");

                AudioZone zone = new AudioZone();
                zone.setID(zoneId);
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

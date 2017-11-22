package com.example.anton.audiocontrollerapp;

import android.content.Context;
import android.util.Log;

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
import java.util.List;

/**
 * Created by anton on 10-Aug-17.
 */

public class ControllerModel {

    static final String CONTROLLER_URL = "/AudioController/api/v1/controller";
    static final String ZONES_URL = "/AudioController/api/v1/controller/zones";

    private Context mContext;
    private String mControllerServerUrl;
    private RequestQueue mQueue;

    public ControllerModel(Context context, String audioControllerUrl){
        if (context == null){
            throw new IllegalArgumentException("context must be provided");
        }

        mContext = context;
        mControllerServerUrl = audioControllerUrl;
        mQueue = Volley.newRequestQueue(mContext);
    }

    public String getControllerUrl() {
        return mControllerServerUrl;
    }

    public void setControllerUrl(String mControllerUrl) {
        this.mControllerServerUrl = mControllerUrl;
    }

    public void requestInputs(final Response.Listener<ArrayList<AudioInput>> successHandler, Response.ErrorListener errorHandler) {
        String url = mControllerServerUrl + CONTROLLER_URL;

        // Request a string response from the AudioController URL.
        StringRequest stringRequest = new StringRequest(
                Request.Method.GET,
                url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        successHandler.onResponse((ArrayList<AudioInput>) ExtractInputs(response));
                    }
                },
                errorHandler);

        mQueue.add(stringRequest);
    }

    public void requestZones(final Response.Listener<ArrayList<AudioZone>> successHandler, Response.ErrorListener errorHandler) {
        String url = mControllerServerUrl + ZONES_URL;

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
        String url = mControllerServerUrl + ZONES_URL + "/" + zone.getID();

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

        mQueue.add(putRequest);
    }

    public void setActiveInput(final AudioInput input) {
        String url = mControllerServerUrl + CONTROLLER_URL;

        JSONObject json = new JSONObject();
        try {
            json.put("SelectedInput", input.getID());
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

    private List<AudioInput> ExtractInputs(String response)
    {
        List<AudioInput> inputs = new ArrayList<>();

        try {
            JSONObject responseInJSON = new JSONObject(response);

            int activeInput = responseInJSON.getInt("SelectedInput");
            JSONArray inputsInJSON = responseInJSON.getJSONArray("Inputs");

            for (int i = 0; i < inputsInJSON.length(); i++) {
                JSONObject zoneJson = inputsInJSON.getJSONObject(i);
                Integer inputId = zoneJson.getInt("InputId");
                String inputName = zoneJson.getString("Name");
                Boolean enabled = activeInput == inputId;

                AudioInput input = new AudioInput();
                input.setID(inputId);
                input.setName(inputName);
                input.setEnabled(enabled);
                inputs.add(input);
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }

        return inputs;
    }
}

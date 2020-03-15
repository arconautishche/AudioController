package com.example.anton.audiocontrollerapp;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.Toast;
import android.widget.SeekBar;
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
import java.util.List;
import java.util.Date;

public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    private LinearLayout mZonesContainer;
    private ControllerModel mController;
    private Spinner mActiveInputSelector;
    private SeekBar mVolumeSeekBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mZonesContainer = (LinearLayout) findViewById(R.id.zonesContainer);
        mActiveInputSelector = (Spinner) findViewById(R.id.activeInputSelector);
        mActiveInputSelector.setOnItemSelectedListener(this);

        mController = new ControllerModel(this, "http://192.168.1.43:8080");
//        mController = new ControllerModel(this, "http://192.168.1.3:8080");

        mVolumeSeekBar = (SeekBar) findViewById(R.id.volumeSeekBar);
        mVolumeSeekBar.setOnSeekBarChangeListener(new OnVolumeBarChangeListener(mController));

        Refresh();
    }

    public class OnVolumeBarChangeListener implements SeekBar.OnSeekBarChangeListener {
        private ControllerModel mController;
        private int val;
        private Date lastUpdate = new Date();

        public OnVolumeBarChangeListener(ControllerModel controllerModel) {
            mController = controllerModel;
        }

        @Override
        public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
            val = i;
            if ((new Date()).getTime() - lastUpdate.getTime() > 200) {
                lastUpdate = new Date();
                mController.setMasterVolume(val);
            }
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {

        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
            mController.setMasterVolume(val);
        }
    }

    public void onRefreshClick(View view) {
        Refresh();
    }

    private void Refresh() {
        mController.requestStatus(
                new Response.Listener<ControllerStatus>() {
                    @Override
                    public void onResponse(ControllerStatus controllerStatus) {
                        ProcessControllerStatus(controllerStatus);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(
                                getApplicationContext(),
                                "Error with Controller Status: " + error.toString(),
                                Toast.LENGTH_LONG).show();
                    }
                });
    }

    private void ProcessControllerStatus(ControllerStatus controllerStatus) {
        ProcessInputs(controllerStatus.getInputs());
        ProcessZones(controllerStatus.getZones());
        mVolumeSeekBar.setProgress(controllerStatus.getmMasterVolume());
    }

    private void ProcessZones(List<AudioZone> zones) {

        int howMany = zones.size();
        Toast.makeText(getApplicationContext(), "Zones: " + howMany, Toast.LENGTH_LONG).show();

        mZonesContainer.removeAllViews();

        for (int i = 0; i < zones.size(); i++) {
            AudioZone zone = zones.get(i);
            createViewForZone(zone);
        }
    }

    private void ProcessInputs(List<AudioInput> inputs) {

        int howMany = inputs.size();
        Toast.makeText(getApplicationContext(), "Inputs: " + howMany, Toast.LENGTH_LONG).show();

        ArrayList<AudioInput> inputsArray = new ArrayList<>();
        int active = 0;

        for (int i = 0; i < inputs.size(); i++) {
            AudioInput input = inputs.get(i);
            inputsArray.add(input);
            if (input.getEnabled())
                active = i;
        }

        ArrayAdapter<AudioInput> inputsAdapter = new ArrayAdapter<AudioInput>(
                this,
                android.R.layout.simple_spinner_dropdown_item,
                inputsArray);

        mActiveInputSelector.setAdapter(inputsAdapter);
        mActiveInputSelector.setSelection(active);
    }

    public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
        AudioInput selectedInput = (AudioInput) parent.getItemAtPosition(pos);

        Toast.makeText(parent.getContext(),
                "setting input: " + selectedInput,
                Toast.LENGTH_SHORT).show();

        mController.setActiveInput(selectedInput);
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


    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
}

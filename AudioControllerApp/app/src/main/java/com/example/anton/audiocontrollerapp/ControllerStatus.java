package com.example.anton.audiocontrollerapp;

import java.util.List;

public class ControllerStatus {
    private List<AudioZone> mZones;

    public void setZones(List<AudioZone> zones) {
        mZones = zones;
    }

    public List<AudioZone> getZones() {
        return mZones;
    }

    private List<AudioInput> mInputs;

    public void setInputs(List<AudioInput> inputs) {
        mInputs = inputs;
    }

    public List<AudioInput> getInputs() {
        return mInputs;
    }

    private int mMasterVolume;

    public void setMasterVolume(int volume){
        mMasterVolume = volume;
    }

    public int getmMasterVolume(){
        return mMasterVolume;
    }
}

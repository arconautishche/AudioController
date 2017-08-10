package com.example.anton.audiocontrollerapp;

/**
 * Created by anton on 10-Aug-17.
 */

public class AudioZone {

    private String mName;
    private Boolean mEnabled;
    private Integer mID;

    public String getName() {
        return mName;
    }

    public void setName(String name) {
        mName = name;
    }

    public Boolean getEnabled() {
        return mEnabled;
    }

    public void setEnabled(Boolean enabled) {
        mEnabled = enabled;
    }

    public Integer getID() {
        return mID;
    }

    public void setID(Integer mID) {
        this.mID = mID;
    }
}

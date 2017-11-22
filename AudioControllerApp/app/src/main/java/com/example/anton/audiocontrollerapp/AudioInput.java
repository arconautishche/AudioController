package com.example.anton.audiocontrollerapp;

/**
 * Created by anton on 10-Aug-17.
 */

public class AudioInput {

    private String mName;
    private Integer mID;
    private Boolean mActive;

    public String getName() {
        return mName;
    }

    public void setName(String name) {
        mName = name;
    }

    public Boolean getEnabled() {
        return mActive;
    }

    public void setEnabled(Boolean enabled) {
        mActive = enabled;
    }

    public Integer getID() {
        return mID;
    }

    public void setID(Integer mID) {
        this.mID = mID;
    }

    public String toString(){
        return this.mName;
    }
}

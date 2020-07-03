import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import VolumeDown from '@material-ui/icons/VolumeDown';
import VolumeUp from '@material-ui/icons/VolumeUp';

class VolumeSlider extends React.Component {
  updatingVolume = false
  nextVolumeUpdate = null

  constructor(props) {
    super(props)
    this.state = {
      volume: props.volume ? props.volume : 0,
    }
    this.handleChange = this.handleChange.bind(this);
    this.volumeUpdateResponse = this.volumeUpdateResponse.bind(this)
    this.lastVolumeFromServer = null
  }

  handleChange(event, newValue) {
    if (this.state.volume === newValue) return
    this.setState({ volume: newValue })
    console.log("volume changed to " + newValue)
    this.nextVolumeUpdate = newValue
    if (!this.updatingVolume) {
      this.sendVolumeUpdate()
    }
  }

  sendVolumeUpdate() {
    this.updatingVolume = true
    var volume = this.nextVolumeUpdate
    this.nextVolumeUpdate = null
    console.log("sending volume " + volume)
    fetch(this.props.server_address, {
      method: 'PUT',
      body: "{\"MasterVolume\": " + volume + "}"
    }).then(resp => this.volumeUpdateResponse(resp))
  }

  volumeUpdateResponse(resp) {
    if (this.nextVolumeUpdate) {
      this.sendVolumeUpdate()
      return
    }

    this.updatingVolume = false
    resp.json()
      .then(status => this.props.on_controller_status_change(status))
  }

  componentDidUpdate(prevProps) {
    console.log("COMPONENT DID UPDATE")
    const newVolume = this.props.volume
    // if (this.lastVolumeFromServer === newVolume) return

    if (this.updatingVolume) {
      this.lastVolumeFromServer = newVolume
    }
    else {
      if (this.state.volume !== newVolume)
        this.lastVolumeFromServer = newVolume
      console.log("UPDATE VOLUME FROM SERVER: ")
      console.log("new volume: "+newVolume)
      console.log("lastVolumeFromServer: "+this.lastVolumeFromServer)
      if (this.lastVolumeFromServer==null) return
      console.log("UPDATE VOLUME FROM SERVER - LastVolumeFromServer=" + this.lastVolumeFromServer)
      this.setState({ volume: this.lastVolumeFromServer })
      this.lastVolumeFromServer = null
    }
  }

  render() {
    console.log("RENDER")
    return (
      <div >
        <Typography id="continuous-slider" gutterBottom>
          Volume
      </Typography>
        <Grid container>
          <Grid item>
            <VolumeDown />
          </Grid>
          <Grid item xs>
            <Slider
              value={this.state.volume}
              onChange={this.handleChange}
              min={0}
              max={100}
              aria-labelledby="continuous-slider" />
          </Grid>
          <Grid item>
            <VolumeUp />
          </Grid>
        </Grid>
      </div>
    )
  }
}

export default VolumeSlider
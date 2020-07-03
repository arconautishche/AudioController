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
      volume: 0,
    }
    this.handleChange = this.handleChange.bind(this);
    this.volumeUpdateResponse = this.volumeUpdateResponse.bind(this)
  }

  handleChange(event, newValue) {
    this.setState({ volume: newValue })
    console.log("volume changed to "+newValue)
    this.nextVolumeUpdate = newValue
    if (!this.updatingVolume) {
      this.sendVolumeUpdate()
    }
  }

  sendVolumeUpdate() {
    this.updatingVolume = true
    var volume = this.nextVolumeUpdate
    this.nextVolumeUpdate = null
    console.log("sending volume "+volume)
    fetch(this.props.server_address, {
      method: 'PUT',
      body: "{\"MasterVolume\": " + volume + "}"
    }).then(this.volumeUpdateResponse)
  }

  volumeUpdateResponse() {
    if (this.nextVolumeUpdate) {
      this.sendVolumeUpdate()
    }
    this.updatingVolume = false
  }

  render() {
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
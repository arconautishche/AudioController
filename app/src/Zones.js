import React from 'react';
import Grid from '@material-ui/core/Grid';
import ToggleButton from '@material-ui/lab/ToggleButton';
import SpeakerGroupIcon from '@material-ui/icons/SpeakerGroup';

class Zone extends React.Component {
  constructor(props){
    super(props)
    this.state = {zoneStatus: props.zone_status}
  }

  componentDidUpdate(prevprops){
    if (this.props === prevprops) return
    this.setState({zoneStatus: this.props.zone_status})
  }

  render() {
    const zone = this.state.zoneStatus
    return (
      <Grid item>
        <ToggleButton
          variant="contained"
          color="primary"
          value="true"
          key={zone.ZoneId}
          selected={zone.Enabled}
          onClick={(e) => this.handleClick(e)}>
          <Grid container direction="column">
            <Grid item>
              <SpeakerGroupIcon />
            </Grid>
            <Grid item >
              {zone.Name}
            </Grid>
          </Grid>
        </ToggleButton>
      </Grid>
    )
  }

  handleClick(e) {
    const zone = this.state.zoneStatus
    console.log("ZONE " + zone.ZoneId + " clicked")
    console.log(zone)
    console.log()
    fetch(this.props.server_address + "/zones/" + zone.ZoneId, {
      method: 'PUT',
      body: "{\"Enabled\": " + !zone.Enabled + "}"
    })
      .then(resp => resp.json())
      .then(status => this.setState({ zoneStatus: status }))
  }
}

class Zones extends React.Component {
  render() {
    return (
      <Grid direction="row" container spacing={1} align="stretch" justify="space-evenly">
        {this.props.zones
          ? this.props.zones.map(zone => (
            <Zone
              zone_status={zone}
              server_address={this.props.server_address}
              key={zone.ZoneId}
            />
          )
          )
          : null}
      </Grid>
    )
  }
}

export default Zones

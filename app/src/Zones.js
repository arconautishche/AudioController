import React from 'react';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

class Zones extends React.Component {
  constructor(props) {
    super(props)
    // this.state = { zones: null }
  }

  _createButtons() {
    if (!this.props.zones) return null
    const buttons = this.props.zones.map((zone) =>
      <ToggleButton
        variant="contained"
        color="primary"
        value="true"
        key={zone.ZoneId}
        onClick={(e) => this.handleClick(zone.ZoneId, e)}>
        {zone.Name}
      </ToggleButton>
    )
    return buttons
  }

  handleClick(id, e) {
    // console.log("button " + id + " clicked")
    // this.setState({selectedInput: id})
    // fetch(this.props.server_address, {
    //   method: 'PUT',
    //   body: "{\"SelectedInput\": " + id + "}"
    // })
  }

  render() {
    console.log("about to rerender sources")
    console.log(this.props)
    return (
      <Grid direction="row" container spacing={1} align="stretch" justify="space-evenly">
        {this._createButtons()}
      </Grid>
    )
  }
}

export default Zones

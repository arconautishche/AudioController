import React from 'react';
// import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import { Box } from '@material-ui/core';
import MusicOffIcon from '@material-ui/icons/MusicOff';


class Sources extends React.Component {
  constructor(props) {
    super(props)
    this.state = { selectedInput: 0 }
  }

  _createButtons() {
    let inputs = this.props.inputs
    if (!inputs) return null


    let groups = Array.from(new Set(inputs.map(input => input.Group))).sort()

    console.log(groups)
    return groups.reduce((html, group) => {
      html.push(
        <Grid container>
          {
            inputs
              .filter(input => input.Group == group)
              .map(input =>
                <Grid item key={input.InputId} width="101" height="101">
                  <ToggleButton
                    variant="contained"
                    color="primary"
                    value={input.InputId}
                    key={input.InputId}
                    width="101" height="101"
                    onClick={(e) => this.handleClick(input.InputId, e)}>
                    <Grid container direction="column" width="101" height="101">
                      <Grid item width="101" height="101">
                        {input.InputId == 0 ?
                          (<MusicOffIcon width="30" height="30" />) :
                          (<img src={input.icon} width="30" height="30" />)}
                      </Grid>
                      <Grid item width="101" height="101">
                        {input.Name}
                      </Grid>
                    </Grid>
                  </ToggleButton>
                </Grid>
              )
          }
        </Grid>
      )
      return html
    }
      , [])
  }

  handleClick(id, e) {
    console.log("button " + id + " clicked")
    this.setState({ selectedInput: id })
    fetch(this.props.server_address, {
      method: 'PUT',
      body: "{\"SelectedInput\": " + id + "}"
    })
  }

  render() {
    console.log("about to rerender sources")
    console.log(this.props)
    return (
      <Container spacing={1} align="stretch" justify="space-evenly">
        {this._createButtons()}
      </Container>
    )
  }
}

export default Sources;

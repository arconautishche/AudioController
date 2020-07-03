import React from 'react';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import ToggleButton from '@material-ui/lab/ToggleButton';
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

    return groups.reduce((buttons, group) => {
      buttons.push(
        <Grid container justify="center" justify-content="space-evenly" key={group}>
          {
            inputs
              .filter(input => input.Group === group)
              .map(input =>
                <Grid item key={input.InputId} flex-grow="1">
                  <ToggleButton
                    variant="contained"
                    color="primary"
                    value={input.InputId}
                    selected={input.InputId === this.props.selected_input}
                    key={input.InputId}
                    onClick={(e) => this.handleClick(input.InputId, e)}>
                    <Grid container direction="column">
                      <Grid item>
                        {input.InputId === 0 ?
                          (<MusicOffIcon width="30" height="30" />) :
                          (<img src={input.icon} width="30" height="30" alt={input.Name}  />)}
                      </Grid>
                      <Grid item >
                        {input.Name}
                      </Grid>
                    </Grid>
                  </ToggleButton>
                </Grid>
              )
          }
        </Grid>
      )
      return buttons
    }
      , [])
  }

  handleClick(id, e) {
    this.setState({ selectedInput: id })
    fetch(this.props.server_address, {
      method: 'PUT',
      body: "{\"SelectedInput\": " + id + "}"
    })
      .then(resp => resp.json())
      .then(status => this.props.on_controller_status_change(status))
  }

  render() {
    return (
      <Container spacing={1} align="stretch" justify="space-evenly">
        {this._createButtons()}
      </Container>
    )
  }
}

export default Sources;

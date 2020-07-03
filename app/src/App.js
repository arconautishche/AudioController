import React from 'react';
import Container from '@material-ui/core/Container';
import Sources from './Sources.js'
import Zones from './Zones.js'
import VolumeSlider from './Volume.js'


// const server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
const server_address = 'http://192.168.1.38:8080/AudioController/api/v1/controller'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      Inputs: null,
      Zones: null,
      SelectedInput: null,
    }
    this.handleControllerStatus = this.handleControllerStatus.bind(this)
  }

  fetchStatus() {
    fetch(server_address)
      .then(resp => resp.json())
      .then(status => { this.handleControllerStatus(status) })
  }

  handleControllerStatus(controllerStatus) {
    this.setState(controllerStatus, this._handleState)
  }

  render() {
    return (
      <Container maxWidth="xs" children="">
        <Sources
          server_address={server_address}
          inputs={this.state.Inputs}
          selected_input={this.state.SelectedInput}
          on_controller_status_change = {this.handleControllerStatus}
        />
        <VolumeSlider
          server_address={server_address}
        />
        <Zones
          server_address={server_address}
          zones={this.state.Zones}
        />
      </Container>
    );
  }

  componentDidMount() {
    this.fetchStatus()
  }
}

//ReactDOM.render(<App />, document.querySelector('#app'));
export default App;

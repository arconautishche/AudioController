import React from 'react';
// import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Sources from './Sources.js'
import Grid from '@material-ui/core/Grid';
import Zones from './Zones.js'
import VolumeSlider from './Volume.js'
 

// const server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
const server_address = 'http://192.168.1.38:8080/AudioController/api/v1/controller'

class App extends React.Component {
  constructor(props){
    super(props)
    this.state={
      Inputs: null,
      Zones: null
    }
  }

  fetchStatus(){
    fetch(server_address)
      .then(resp => resp.json())
      .then(status => {
          this.setState(status,this._handleState)
          console.log("status fetched")
          console.log(status)
      })
  }

  render() {
    console.log("about to rerender app")
    return (
      <Container maxWidth="xs">
        <Sources server_address={server_address} inputs={this.state.Inputs}/>
        <VolumeSlider server_address={server_address}/>
        <Zones server_address={server_address} zones={this.state.Zones}/>
      </Container>
    );
  }

  componentDidMount(){
    this.fetchStatus()
  }
}

//ReactDOM.render(<App />, document.querySelector('#app'));
export default App;

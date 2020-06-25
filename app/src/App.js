import React from 'react';
// import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

// var setHeader = require('setheader');
// setHeader(res, 'X-Frame-Options', 'DENY');

//const server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
const server_address = 'http://localhost:8080/AudioController/api/v1/controller'


class Sources extends React.Component {
  render() {
    return (
      <Container>
        <Button variant="contained" color="primary">
          Button 1 {this.props.sources}
        </Button>
        <Button variant="contained" color="primary">
          Button 2
        </Button>
      </Container>
    )
  }
}

class App extends React.Component {
  getStatus = async() => {
    const response = await fetch(server_address)
    const status = await response.json(); 
    console.log(status)
    return status
  }

  render() {
    let status = this.getStatus()
    console.log(status)
    return (
      <Container>
        <Sources sources={status.Inputs}/>
      </Container>
    );
  }
}

//ReactDOM.render(<App />, document.querySelector('#app'));
export default App;

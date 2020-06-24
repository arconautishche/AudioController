import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

const server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'

const getStatus = async() => {
  const response = await fetch(server_address
    , {mode:'no-cors'}
    )
  console.log(response.json())
  const myJson = await response.json(); 
}

function Sources() {
  return (
    <Container>
      <Button variant="contained" color="primary">
        Button 1
      </Button>
      <Button variant="contained" color="primary">
        Button 2
      </Button>
    </Container>
  )
}

function App() {
  let status = getStatus()
  return (
    <Container>
      <Sources />
    </Container>
  );
}

//ReactDOM.render(<App />, document.querySelector('#app'));
export default App;

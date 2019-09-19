// @format
import React, {Component} from 'react';
import './App.css';
import Login from './Login';
import Register from './Register';
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loginstatus: '',
    };
  }
  loginStatus = dataFromChild => {
    this.setState({loginstatus: dataFromChild});
    console.log(dataFromChild);
  };
  render() {
    const loginStatus = this.state.loginstatus;
    let component;

    if (loginStatus === 'Please register.') {
      component = <Register />;
    } else {
      component = <Login callbackFromParent={this.loginStatus} />;
    }
    return (
      <div>
        <div className="App">
          <header className="App-header">
            <p>
              Welcome to Leetcode Tracker.
              <br />
              Track your progress and become successful in your interviews.
            </p>
            {component}
          </header>
        </div>
      </div>
    );
  }
}

export default App;

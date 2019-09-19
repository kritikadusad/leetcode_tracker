// @format
import React, {Component} from 'react';
//import './Login.css';
class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {status: '', email: '', password: ''};

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleEmailChange(event) {
    this.setState({email: event.target.value});
  }
  handlePasswordChange(event) {
    this.setState({password: event.target.value});
  }
  handleSubmit(event) {
    event.preventDefault();
    const API = 'http://localhost:5000/register';
    fetch(API, {
      method: 'POST',
      body: JSON.stringify({
        email: this.state.email,
        password: this.state.password,
      }),
    })
      .then(response => response.json())
      .then(server_status => this.setState({status: server_status}));
    this.props.callbackFromParent(this.state.status);
  }
  render() {
    return (
      <div className="Register">
        <p>Please register here</p>
        <form onSubmit={this.handleSubmit}>
          <label>
            Email{' '}
            <input
              type="text"
              autocomplete="username"
              value={this.state.email}
              onChange={this.handleEmailChange}
            />
          </label>
          <br />
          <label>
            Password{' '}
            <input
              type="password"
              autocomplete="new-password"
              value={this.state.password}
              onChange={this.handlePasswordChange}
            />
          </label>
          <br />
          <input type="submit" value="Register" />
        </form>
      </div>
    );
  }
}

export default Register;

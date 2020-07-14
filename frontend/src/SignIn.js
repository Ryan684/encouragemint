import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Copyright from './Copyright'
import { Link } from 'react-router-dom';

export class SignIn extends React.Component {
  constructor(props){
    super(props);
    this.state = {
         username: '', usernameValid: false,
         password: '', passwordValid: false,
         formValid: false,
         errorMsg: {}
      }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  updateUsername = (username) => {
    this.setState({username}, this.validateUsername)
  }

  validateUsername = () => {
    const {username} = this.state;
    let usernameValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!/^[a-zA-Z0-9\\-]{5,}$/.test(username)) {
      usernameValid = false;
      errorMsg.username = 'Must be at least 5 characters long and only contain letters and numbers.'
    }

    this.setState({usernameValid, errorMsg}, this.validateForm)
  }

  updatePassword = (password) => {
    this.setState({password}, this.validatePassword);
  }

  validatePassword = () => {
    const {password} = this.state;
    let passwordValid = true;
    let errorMsg = {...this.state.errorMsg}

    // must be 8 chars
    // must contain a number
    // must contain a special character

    if (!/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/.test(password)) {
      passwordValid = false;
      errorMsg.password = 'Password must be at least 8 characters long, contain a digit and at least one special character.';
    }

    this.setState({passwordValid, errorMsg}, this.validateForm);
  }

  handleSubmit = (event) => {
    event.preventDefault();
    alert('username: ' +this.state.username)
    alert('password: ' +this.state.password)
  }

  render() {
      return (
        <Container component='main' maxWidth='xs'>
          <CssBaseline />
          <div className={this.props.classes.paper}>
            <Avatar className={this.props.classes.avatar}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component='h1' variant='h5'>
              Sign in
            </Typography>
            <form onSubmit={this.handleSubmit} className={this.props.classes.form} noValidate>
               <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='username'
                    label='Username'
                    name='username'
                    autoComplete='username'
                    value={this.state.username}
                    onChange={(e) => this.updateUsername(e.target.value)}
                    error={!this.state.usernameValid && this.state.username.length >= 1 ? true : false}
                    helperText={this.state.usernameValid ? null : this.state.errorMsg.username}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    name='password'
                    label='Password'
                    type='password'
                    id='password'
                    autoComplete='current-password'
                    value={this.state.password}
                    onChange={(e) => this.updatePassword(e.target.value)}
                    error={!this.state.passwordValid && this.state.password.length >= 1 ? true : false}
                    helperText={this.state.passwordValid ? null : this.state.errorMsg.password}
                  />
                </Grid>
                <Grid item xs={12}>
                </Grid>
              </Grid>
              <Button
                type='submit'
                fullWidth
                variant='contained'
                color='primary'
                className={this.props.classes.submit}
              >
                Sign In
              </Button>
              <Grid container>
                <Grid item xs>
                    <Link to='/'>{'Forgot password?'}</Link>
                </Grid>
                <Grid item>
                  <Link to='/signup'>{"Don't have an account? Sign Up"}</Link>
                </Grid>
              </Grid>
            </form>
          </div>
          <Box mt={8}>
            <Copyright />
          </Box>
        </Container>
      );
  };
}
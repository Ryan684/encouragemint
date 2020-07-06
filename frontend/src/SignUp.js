import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Copyright from './Copyright'

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function SignUpFunc() {
  const classes = useStyles();
  return (
    <div>
        <SignUp classes={classes}/>
    </div>
  );
}

export default SignUpFunc;

function ValidationMessage(props) {
  if (!props.valid) {
    return(
      <div className='error-msg'>{props.message}</div>
    )
  }
  return null;
}

class SignUp extends React.Component {
  constructor(props){
    super(props);
    this.state = {
         password: '', passwordValid: false,
         firstName: '', firstNameValid: false,
         lastName: '', lastNameValid: false,
         emailAddress: '', emailAddressValid: false,
         username: '', usernameValid: false,
         formValid: false,
         errorMsg: {}
      }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  validateForm = () => {
    const {emailAddressValid, passwordValid, firstNameValid, lastNameValid, usernameValid} = this.state;
    this.setState({
      formValid: emailAddressValid && passwordValid && firstNameValid && lastNameValid && usernameValid
    })
  }

  updateFirstName = (firstName) => {
    this.setState({firstName}, this.validateFirstName)
  }

  validateFirstName = () => {
    const {firstName} = this.state;
    let firstNameValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!/^[a-zA-Z]{3,}$/.test(firstName)) {
      firstNameValid = false;
      errorMsg.firstName = 'Must be at least 3 characters long and only contain letters'
    }

    this.setState({firstNameValid, errorMsg}, this.validateForm)
  }

  updateLastName = (lastName) => {
    this.setState({lastName}, this.validateLastName)
  }

  validateLastName = () => {
    const {lastName} = this.state;
    let lastNameValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!/^[a-zA-Z]{3,}$/.test(lastName)) {
      lastNameValid = false;
      errorMsg.lastName = 'Must be at least 3 characters long and only contain letters'
    }

    this.setState({lastNameValid, errorMsg}, this.validateForm)
  }

  updateEmailAddress = (emailAddress) => {
    this.setState({emailAddress}, this.validateEmailAddress)
  }

  validateEmailAddress = () => {
    const {emailAddress} = this.state;
    let emailAddressValid = true;
    let errorMsg = {...this.state.errorMsg}

    // checks for format _@_._
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailAddress)) {
      emailAddressValid = false;
      errorMsg.emailAddress = 'Invalid email format'
    }

    this.setState({emailAddressValid, errorMsg}, this.validateForm)
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

  async handleSubmit(event) {
    event.preventDefault();
    if (this.state.formValid) {
      try {
        let response = await fetch('http://127.0.0.1:8000/user/', {
            method: 'POST',
            body: JSON.stringify({
                'first_name': this.state.firstName,
                'last_name': this.state.lastName,
                'email': this.state.emailAddress,
                'username': this.state.username,
                'password': this.state.password
            }),
            headers: {
              'Content-Type': 'application/json'
            }
        });
        let data = await response.json()
        console.log(data);
        return data;
      } catch(err) {
        console.error(err);
      }
    }
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
              Sign up
              </Typography>
              <form onSubmit={this.handleSubmit} className={this.props.classes.form} noValidate>
                <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete='fname'
                    name='firstName'
                    variant='outlined'
                    required
                    fullWidth
                    id='firstName'
                    label='First Name'
                    autoFocus
                    value={this.state.firstName}
                    onChange={(e) => this.updateFirstName(e.target.value)}
                  />
                  <ValidationMessage valid={this.state.firstNameValid} message={this.state.errorMsg.firstName} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='lastName'
                    label='Last Name'
                    name='lastName'
                    autoComplete='lname'
                    value={this.state.lastName}
                    onChange={(e) => this.updateLastName(e.target.value)}
                  />
                  <ValidationMessage valid={this.state.lastNameValid} message={this.state.errorMsg.lastName} />
                </Grid>
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
                  />
                  <ValidationMessage valid={this.state.usernameValid} message={this.state.errorMsg.username} />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='emailAddress'
                    label='Email Address'
                    name='emailAddress'
                    autoComplete='email'
                    value={this.state.emailAddress}
                    onChange={(e) => this.updateEmailAddress(e.target.value)}
                  />
                  <ValidationMessage valid={this.state.emailAddressValid} message={this.state.errorMsg.emailAddress} />
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
                  />
                  <ValidationMessage valid={this.state.passwordValid} message={this.state.errorMsg.password} />
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
                Sign Up
              </Button>
              <Grid container justify='flex-start'>
                <Grid item>
                  <Link href='#' variant='body2'>
                    Already have an account? Sign in
                  </Link>
                </Grid>
              </Grid>
            </form>
          </div>
          <Box mt={5}>
            <Copyright />
          </Box>
        </Container>
      );
  };
}

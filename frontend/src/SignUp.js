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

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://material-ui.com/">
            Encouragemint
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
        </Typography>
    );
}

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

class SignUp extends React.Component {
  constructor(props){
    super(props);
    this.state = {
         firstName: '',
         lastName: '',
         emailAddress: ''
      }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit = (event) => {
    fetch('http://127.0.0.1:8000/profile/', {
        method: 'POST',
        body: JSON.stringify({
            'first_name': this.state.firstName,
            'last_name': this.state.lastName,
            'email_address': this.state.emailAddress
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function(response) {
        console.log(response)
        return response.json();
      });
  }

  render() {
      return (
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <div className={this.props.classes.paper}>
            <Avatar className={this.props.classes.avatar}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <form onSubmit={this.handleSubmit} className={this.props.classes.form} noValidate>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="fname"
                    name="firstName"
                    variant="outlined"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoFocus
                    value={this.state.firstName}
                    onChange={this.handleChange}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="lname"
                    value={this.state.lastName}
                    onChange={this.handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="emailAddress"
                    label="Email Address"
                    name="emailAddress"
                    autoComplete="email"
                    value={this.state.emailAddress}
                    onChange={this.handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                  />
                </Grid>
                <Grid item xs={12}>

                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={this.props.classes.submit}
              >
                Sign Up
              </Button>
              <Grid container justify="flex-start">
                <Grid item>
                  <Link href="#" variant="body2">
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

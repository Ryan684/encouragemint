import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { SignIn } from './SignIn'
import SignUp from './SignUp'
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

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
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function App() {
  const classes = useStyles();
  return (
    <Router>
        <Switch>
          <Route exact path='/'>
            <SignIn classes={classes}/>
          </Route>
          <Route path='/signup'>
            <SignUp classes={classes}/>
          </Route>
        </Switch>
    </Router>
  );
}

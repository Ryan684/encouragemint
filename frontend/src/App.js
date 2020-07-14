import React from 'react';
import SignInFunc from './SignIn'
import SignUpFunc from './SignUp'
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

export default function App() {
  return (
    <Router>
        <Switch>
          <Route exact path='/'>
            <SignInFunc />
          </Route>
          <Route path='/signup'>
            <SignUpFunc />
          </Route>
        </Switch>
    </Router>
  );
}

import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import MenuItem from '@material-ui/core/MenuItem';
import EcoIcon from '@material-ui/icons/Eco';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Copyright from './Copyright'
import { withRouter } from 'react-router-dom';

class RecommendForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
         location: '', locationValid: false,
         duration: '', durationValid: false,
         bloomPeriod: '', bloomPeriodValid: false,
         formValid: false,
         errorMsg: {}
      }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  validateForm = () => {
    const {durationValid, bloomPeriodValid, locationValid} = this.state;
    this.setState({
      formValid: durationValid && bloomPeriodValid && locationValid
    })
  }

  updateLocation = (location) => {
    this.setState({location}, this.validateLocation)
  }

  validateLocation = () => {
    const {location} = this.state;
    let locationValid = true;
    let errorMsg = {...this.state.errorMsg}

    let locationRegex = /^[a-zA-Z0-9\-\s',]+,[a-zA-Z0-9\-\s,']+$/

    if (!locationRegex.test(location)) {
      locationValid = false;
      errorMsg.location = 'Invalid entry for the garden\'s location. A garden\'s location can only contain letters, numbers, hyphens, spaces, commas and apostrophes. To be a valid location, you also have to have at least one degree of accuracy. For example; \'London\' would not be valid, but \'London, UK\' would work.'
    }

    this.setState({locationValid, errorMsg}, this.validateForm)
  }

  updateDuration = (duration) => {
    this.setState({duration}, this.validateDuration)
  }

  validateDuration = () => {
    const {duration} = this.state;
    let durationValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!['PERENNIAL', 'ANNUAL', 'BIENNIAL'].includes(duration.toUpperCase())) {
      durationValid = false;
      errorMsg.duration = 'A garden\'s duration can only be perennial, annual or biennial.'
    }

    this.setState({durationValid, errorMsg}, this.validateForm)
  }

  updateBloomPeriod = (bloomPeriod) => {
    this.setState({bloomPeriod}, this.validateBloomPeriod);
  }

  validateBloomPeriod = () => {
    const {bloomPeriod} = this.state;
    let bloomPeriodValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!['EARLY SPRING', 'LATE SPRING', 'ALL SPRING', 'EARLY SUMMER', 'LATE SUMMER', 'ALL SUMMER', 'EARLY AUTUMN',
    'LATE AUTUMN', 'ALL AUTUMN', 'EARLY WINTER', 'LATE WINTER', 'ALL WINTER'].includes(bloomPeriod.toUpperCase())) {
      bloomPeriodValid = false;
      errorMsg.bloomPeriod = 'A garden\'s bloom period can only be spring, summer, autumn or winter.';
    }

    this.setState({bloomPeriodValid, errorMsg}, this.validateForm);
  }

  async handleSubmit(event) {
    event.preventDefault();
    if (this.state.formValid) {
      try {
        let response = await fetch('http://127.0.0.1:8000/recommend/', {
            method: 'POST',
            body: JSON.stringify({
                'location': this.state.location,
                'duration': this.state.duration,
                'bloom_period': this.state.bloomPeriod
            }),
            headers: {
              'Content-Type': 'application/json'
            }
        });
        let data = await response.json()
        console.log(data);

        if (response.status === 200) {
            this.props.history.push('/');
        }
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
              <EcoIcon />
            </Avatar>
            <Typography component='h1' variant='h5'>
              Tell us about your garden and your preferences
              </Typography>
              <form onSubmit={this.handleSubmit} className={this.props.classes.form} noValidate>
                <Grid container spacing={2}>
                <Grid item xs={12}>
                  <p>Where is your garden? (The more accurate, the better!)</p>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='location'
                    label='Location'
                    name='location'
                    autoComplete='location'
                    value={this.state.location}
                    onChange={(e) => this.updateLocation(e.target.value)}
                    error={!this.state.locationValid && this.state.location.length >= 1 ? true : false}
                    helperText={this.state.locationValid ? null : this.state.errorMsg.location}
                  />
                </Grid>
                <Grid item xs={12}>
                  <p>How hardy do the plants need to be?</p>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='duration'
                    label='Duration'
                    name='duration'
                    value={this.state.duration}
                    onChange={(e) => this.updateDuration(e.target.value)}
                    error={!this.state.durationValid && this.state.duration.length >= 1 ? true : false}
                    helperText={this.state.durationValid ? null : this.state.errorMsg.duration}
                    select
                  >
                    <MenuItem value="Perennial">Perennial</MenuItem>
                    <MenuItem value="Annual">Annual</MenuItem>
                    <MenuItem value="Biennial">Biennial</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={12}>
                  <p>When do you want the plants to bloom?</p>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='bloomPeriod'
                    name='bloomPeriod'
                    label='Bloom Period'
                    type='bloomPeriod'
                    value={this.state.bloomPeriod}
                    onChange={(e) => this.updateBloomPeriod(e.target.value)}
                    error={!this.state.bloomPeriodValid && this.state.bloomPeriod.length >= 1 ? true : false}
                    helperText={this.state.bloomPeriodValid ? null : this.state.errorMsg.bloomPeriod}
                    select
                  >
                    <MenuItem value="Early Spring">Early Spring</MenuItem>
                    <MenuItem value="Late Spring">Late Spring</MenuItem>
                    <MenuItem value="All Spring">All Spring</MenuItem>
                    <MenuItem value="Early Summer">Early Summer</MenuItem>
                    <MenuItem value="Late Summer">Late Summer</MenuItem>
                    <MenuItem value="All Summer">All Summer</MenuItem>
                    <MenuItem value="Early Autumn">Early Autumn</MenuItem>
                    <MenuItem value="Late Autumn">Late Autumn</MenuItem>
                    <MenuItem value="All Autumn">All Autumn</MenuItem>
                    <MenuItem value="Early Winter">Early Winter</MenuItem>
                    <MenuItem value="Late Winter">Late Winter</MenuItem>
                    <MenuItem value="All Winter">All Winter</MenuItem>
                  </TextField>
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
                Search
              </Button>
            </form>
          </div>
          <Box mt={5}>
            <Copyright />
          </Box>
        </Container>
      );
  };
}

export default withRouter(RecommendForm);

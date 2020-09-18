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
import { withRouter } from 'react-router-dom';

class RecommendForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
         season: '', seasonValid: false,
         location: '', locationValid: false,
         duration: '', durationValid: false,
         direction: '', directionValid: false,
         bloomPeriod: '', bloomPeriodValid: false,
         formValid: false,
         errorMsg: {}
      }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  validateForm = () => {
    const {durationValid, bloomPeriodValid, seasonValid, locationValid, directionValid} = this.state;
    this.setState({
      formValid: durationValid && bloomPeriodValid && seasonValid && locationValid && directionValid
    })
  }

  updateSeason = (season) => {
    this.setState({season}, this.validateSeason)
  }

  validateSeason = () => {
    const {season} = this.state;
    let seasonValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!['SPRING', 'SUMMER', 'AUTUMN', 'WINTER'].includes(season.toUpperCase())) {
      seasonValid = false;
      errorMsg.season = 'A garden\'s season can only be spring, summer, autumn or winter.'
    }

    this.setState({seasonValid, errorMsg}, this.validateForm)
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

  updateDirection = (direction) => {
    this.setState({direction}, this.validateDirection)
  }

  validateDirection = () => {
    const {direction} = this.state;
    let directionValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!['NORTH', 'EAST', 'SOUTH', 'WEST'].includes(direction.toUpperCase())) {
      directionValid = false;
      errorMsg.direction = 'A garden\'s direction can only be north, east, south or west.'
    }

    this.setState({directionValid, errorMsg}, this.validateForm)
  }

  updateBloomPeriod = (bloomPeriod) => {
    this.setState({bloomPeriod}, this.validateBloomPeriod);
  }

  validateBloomPeriod = () => {
    const {bloomPeriod} = this.state;
    let bloomPeriodValid = true;
    let errorMsg = {...this.state.errorMsg}

    if (!['SPRING', 'SUMMER', 'AUTUMN', 'WINTER'].includes(bloomPeriod.toUpperCase())) {
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
                'season': this.state.season,
                'location': this.state.location,
                'duration': this.state.duration,
                'direction': this.state.direction,
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
              <LockOutlinedIcon />
            </Avatar>
            <Typography component='h1' variant='h5'>
              Tell us about your garden and your plant preferences
              </Typography>
              <form onSubmit={this.handleSubmit} className={this.props.classes.form} noValidate>
                <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete='season'
                    name='season'
                    variant='outlined'
                    required
                    fullWidth
                    id='season'
                    label='Season'
                    autoFocus
                    value={this.state.season}
                    onChange={(e) => this.updateSeason(e.target.value)}
                    error={!this.state.seasonValid && this.state.season.length >= 1 ? true : false}
                    helperText={this.state.seasonValid ? null : this.state.errorMsg.season}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
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
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='direction'
                    label='Direction'
                    name='direction'
                    autoComplete='direction'
                    value={this.state.direction}
                    onChange={(e) => this.updateDirection(e.target.value)}
                    error={!this.state.directionValid && this.state.direction.length >= 1 ? true : false}
                    helperText={this.state.directionValid ? null : this.state.errorMsg.direction}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    id='duration'
                    label='Duration'
                    name='duration'
                    autoComplete='duration'
                    value={this.state.duration}
                    onChange={(e) => this.updateDuration(e.target.value)}
                    error={!this.state.durationValid && this.state.duration.length >= 1 ? true : false}
                    helperText={this.state.durationValid ? null : this.state.errorMsg.duration}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant='outlined'
                    required
                    fullWidth
                    name='bloomPeriod'
                    label='Bloom Period'
                    type='bloomPeriod'
                    id='bloomPeriod'
                    autoComplete='current-bloomPeriod'
                    value={this.state.bloomPeriod}
                    onChange={(e) => this.updateBloomPeriod(e.target.value)}
                    error={!this.state.bloomPeriodValid && this.state.bloomPeriod.length >= 1 ? true : false}
                    helperText={this.state.bloomPeriodValid ? null : this.state.errorMsg.bloomPeriod}
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
                Sign Up
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

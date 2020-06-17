import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import { ProfileRegistrationForm } from './profileRegistrationForm';

export function App() {
  return (
    <div className="App">
        <Container>
          <Row>
            <Col />
            <Col xs={8}>
                  <header className="App-header">
                    <h1>Create a Profile</h1>
                    <ProfileRegistrationForm />
                  </header>
            </Col>
            <Col />
          </Row>
        </Container>
    </div>
  );
}

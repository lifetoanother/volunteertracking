import './App.css';
import { Navbar, Nav, Container, Button, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import Form from 'react-bootstrap/Form'

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <Navbar bg="dark" variant="dark">
    <Container>
    <Navbar.Brand href="#home">Home</Navbar.Brand>
    <Nav className="me-auto">
      <Nav.Link href="#input">Hours Input</Nav.Link>
    </Nav>
    </Container>
  </Navbar>
      </header>
      <main>
        <Container>
          
          <fieldset>
<Form>
  <Row className="mb-3">
  <Form.Group as={Col} controlId="formTimeIn">
    <Form.Label>Input Hours</Form.Label>
    <Form.Control id="formTimeIn" placeholder="hours "></Form.Control>
  </Form.Group>
  <Form.Group as={Col} controlId="monthlyHours">
  <Form.Label>Total Monthly Hours</Form.Label>
  </Form.Group>
  
 
  </Row>
  <Button type="submit">Submit</Button>
</Form>
</fieldset>
        </Container>
      </main>
    </div>
  );
}

export default App;

import {useState} from 'react';
import {Container, Row, Col, Form, Button} from 'react-bootstrap'
import logo from './img/logo.svg';
import logo_small from './img/logo_small.svg';


const SearchForm = (props) => {
    const [text, setText] = useState(props.data);

    const handleSubmit = (event) => {
        event.preventDefault()
        props.handler({
            "search_query": text,
            "essa": "rigcz"
        });
    };

    const refreshPage = () => {
        window.location.reload();
    }

    if (props.inline) {
        return (
            <Form onSubmit={handleSubmit}>
                <Row className="align-items-center search-bar">
                    <Col xs="4" md="3" lg="2" className="small-logo">
                        <img className="logo-img" onClick={refreshPage} src={logo_small} alt="Wyszukiwara"/>
                    </Col>

                    <Col xs="8" md="4" lg="6" style={{paddingTop: "16px"}}>
                        <Form.Group className="mb-3" controlId="formText">
                            <Form.Control
                                type="text"
                                placeholder="Kto pytal?"
                                value={text}
                                onChange={e => setText(e.target.value)}
                            />
                        </Form.Group>
                    </Col>
                    <Col xs="6" md="3" lg="2">
                        <Form.Check type="checkbox" label="Low rank approx."/>
                    </Col>

                    <Col xs="6" md="2" lg="2">
                        <Button className="w-100" variant="outline-primary" type="submit">
                            Search
                        </Button>
                    </Col>
                </Row>
            </Form>

        )
    }
    return (
        <Form onSubmit={handleSubmit}>
            <Container className="large-logo">
                <img className="logo-img" onClick={refreshPage} src={logo} alt="Wyszukiwara"/>
            </Container>

            <Form.Group className="mb-3" controlId="formText">
                <Form.Control
                    type="text"
                    placeholder="Kto pytal?"
                    value={text}
                    onChange={e => setText(e.target.value)}
                />
            </Form.Group>

            <Container>
                <Row className="justify-content-center align-items-center">
                    <Col xs="12" lg="6">
                        <Form.Check type="checkbox" label="Low rank approx."/>
                    </Col>
                    <Col xs="12" lg="1" style={{height: "10px"}}>
                    </Col>
                    <Col xs="12" lg="5">
                        <Button className="w-100" variant="outline-primary" type="submit">
                            Search
                        </Button>
                    </Col>
                </Row>
            </Container>
        </Form>
    )
}

export default SearchForm;

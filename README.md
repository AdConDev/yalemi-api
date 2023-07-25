# Social Media API

Social Media API with Python, SQL and FastAPI.

## Table of Contents

- [FastAPI](#fastapi)

## API

An API (Application Programming Interface) is a set of functions that allows applications to access data and interact with external software components, operating systems, or microservices. To simplify, an API delivers a user response to a system and sends the system's response back to a user.

## REST Architecture

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) stands for Representational State Transfer. It is a software architecture style that relies on a stateless communications protocol, most commonly, HTTP. It is an alternative to SOAP (Simple Object Access Protocol) and instead of using XML for requests, it uses JSON.

1. ***Client-Server***: There should be a separation between the server that offers a service, and the client that consumes it.
2. ***Stateless***: Each request from a client must contain all the information required by the server to carry out the request. In other words, the server cannot store information provided by the client in one request and use it in another request.
3. ***Cache***: Clients can cache data. For example, if the server returns a response, the client can cache it and use the same response the next time it needs to make the same request.
4. ***Uniform Interface***: The method of communication between a client and a server must be uniform.
5. ***Layered System***: Communication between a client and a server should be standardized in such a way that allows intermediaries to respond to requests instead of the end server, without the client having to do anything different.
6. ***Code on Demand*** (optional): Servers can provide executable code or scripts for clients to execute in their context. This constraint is the only one that is optional.

## API REST

A REST API is an API that conforms to the REST architecture style. It is a set of rules that allow programs to talk to each other. The developer creates the API on the server and allows the client to talk to it.

## FastAPI

[FastAPI](https://github.com/tiangolo/fastapi) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### JSON Schema Validation With Pydantic

[Pydantic](https://pydantic-docs.helpmanual.io/) is a library that provides runtime checking and validation of the data sent and received over APIs. FastAPI uses Pydantic to validate the data.

### Automatic Documentation With Swagger UI

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a collection of HTML, Javascript, and CSS assets that dynamically generate beautiful documentation from a Swagger-compliant API.

## Postman

[Postman](https://www.postman.com/) is a collaboration platform for API development. Postman's features simplify each step of building an API and streamline collaboration so you can create better APIs—faster.

### HTTP Request Methods

- ***GET***: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
- ***POST***: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
- ***PUT***: The PUT method replaces all current representations of the target resource with the request payload.
- ***DELETE***: The DELETE method deletes the specified resource.
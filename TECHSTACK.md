# Social Media API

Social Media API with Python FastAPI and Postgres SQL.

## Table of Contents

- [FastAPI](#fastapi)

## API REST

A REST API is an API that conforms to the REST architecture style. It is a set of rules that allow programs to talk to each other. The developer creates the API on the server and allows the client to talk to it.

### API

An API (Application Programming Interface) is a set of functions that allows applications to access data and interact with external software components, operating systems, or microservices. To simplify, an API delivers a user response to a system and sends the system's response back to a user.

### REST Architecture

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) stands for Representational State Transfer. It is a software architecture style that relies on a stateless communications protocol, most commonly, HTTP. It is an alternative to SOAP (Simple Object Access Protocol) and instead of using XML for requests, it uses JSON.

1. ***Client-Server***: There should be a separation between the server that offers a service, and the client that consumes it.
2. ***Stateless***: Each request from a client must contain all the information required by the server to carry out the request. In other words, the server cannot store information provided by the client in one request and use it in another request.
3. ***Cache***: Clients can cache data. For example, if the server returns a response, the client can cache it and use the same response the next time it needs to make the same request.
4. ***Uniform Interface***: The method of communication between a client and a server must be uniform.
5. ***Layered System***: Communication between a client and a server should be standardized in such a way that allows intermediaries to respond to requests instead of the end server, without the client having to do anything different.
6. ***Code on Demand*** (optional): Servers can provide executable code or scripts for clients to execute in their context. This constraint is the only one that is optional.

#### FastAPI

[FastAPI](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

##### Pydantic

[Pydantic](https://pydantic-docs.helpmanual.io/) is a library that provides runtime checking and validation of the data sent and received over APIs. FastAPI uses Pydantic to validate the data.

##### Swagger UI

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a collection of HTML, Javascript, and CSS assets that dynamically generate beautiful documentation from a Swagger-compliant API.

#### Postman

[Postman](https://www.postman.com/) is a collaboration platform for API development. Postman's features simplify each step of building an API and streamline collaboration so you can create better APIs—faster.

##### HTTP Request Methods

- ***GET***: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
- ***POST***: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
- ***PUT***: The PUT method replaces all current representations of the target resource with the request payload.
- ***DELETE***: The DELETE method deletes the specified resource.

## Database

A ***Database*** is a collection of objects that includes tables, functions, and much more, and this is where your actual ***data*** will lie.

### Database Management System (DBMS)

A ***Database Management System (DBMS)*** is software that allows you to define, manage, and query databases. It creates a ***Database Server***—an instance of the application running on your computer—that includes a default database.

#### PostgreSQL

[PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

##### pgAdmin

With ***pgAdmin***, you get a ***graphical interface*** where you can configure multiple aspects of your ***PostgreSQL server*** and databases, and use a SQL query tool for writing, running, and saving queries.

## Object Relational Mapping (ORM)

An ***Object Relational Mapping (ORM)*** is a technique that lets you query and manipulate data from a database using an object-oriented paradigm. When talking about ORM, most people are referring to a library that implements the Object-Relational Mapping technique, hence the phrase "an ORM".

### SQLModel

[SQLModel](https://sqlmodel.tiangolo.com/) is a library for interacting with SQL databases from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust. It is based on the [Pydantic](https://pydantic-docs.helpmanual.io/) data validation library, and [SQLAlchemy](https://www.sqlalchemy.org/) core. Creators of SQLModel are the same as [FastAPI](https://fastapi.tiangolo.com/)

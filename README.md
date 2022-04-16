# Django Intro Assignment

This repository contains the small microservice app as part of the received assignment.

---

## Stack:
- Django Rest Framework
- PostreSQL
- Docker

## Prerequisites:
- Python
- Django
- PostgreSQL
- Django

## Installation:
``` python3 manage.py runserver 8000 ```

## List of apps:
- Orders
- Users

## User Endpoints:
| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `GET`    | `http://localhost:8080/user/{id}/balance`                             | Retrieve the balance for the user.                      |
| `POST`   | `http://localhost:8080/user/{id}/deposit`                             | Deposit the funds to the user's balance.                       |
| `POST`    | `http://localhost:8080/user/{id}/charge`                          | Charge the funds from the user's balance.                       |

## Order Endpoints:
| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `POST`    | `http://localhost:8080/order/create`                             | Create the new order.                      |
| `GET`   | `http://localhost:8080/order/{order_id}`                             | Get the order by its ID.                       |
| `GET`    | `http://localhost:8080/orders?limit=100&offset=10`                          | Retrieve the list of orders by the paging provided.                       |
| `POST`    | `http://localhost:8080/order/pay`                          | Pay for the order.                       |
| `POST`    | `http://localhost:8080/{order_id}/refund`                          | Refund the money from the paid order.                       |
| `GET`    | `http://localhost:8080/{id}/orders`                          | Get all the order of the specific user.                       |

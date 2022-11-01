## Laboratory work for network programming class
### Food Ordering Service Server
___ 
To start the project make sure you have the Dining Hall Server running and then run the  Client Service Server using the 
```docker-compose up``` command</br>

The basic idea of food ordering simulation is to have multiple clients ordering food from multiple restaurants. The goal is to
adopt the restaurant implementation to be able to integrate with some "third" party services such as Food Ordering service.

`Food ordering service` is connection link between `clients` and `restaurant` . In order to order some foods, client
communicates with the `food ordering services` and post some generated orders. `Food ordering service` receives orders requests
from `clients` and post order to dedicated `restaurant`.

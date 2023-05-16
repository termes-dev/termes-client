# termes-client

> Elegant, modern, and asynchronous Termes Client API framework in Python

``` python
from termes.client import Client

API_HOST = "http://localhost:8080/"  # define Termes API server host

session = Session(...)  # load session, if saved


async with Client(API_HOST, session) as client:
    print(await client.account.get())
```


**termes-client** is a modern, elegant and asynchronous [Termes Client API]() framework. It enables you to easily interact with the Termes Client API and create your own Termes client using Python.

### Key Features
- **Ready**: Install termes-client and start building your applications right away.
- **Easy**: Makes the Termes Client API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous.
- **Powerful**: Full access to Termes Client API to execute any client action and more.
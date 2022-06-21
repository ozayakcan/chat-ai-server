# chat-ai-server

- Client repo: [https://github.com/ozayakcan/chat-ai-client](https://github.com/ozayakcan/chat-ai-client)

Usage on replit:

Install tensorflow-cpu manually
```
pip install tensorflow-cpu
```

Add this lines in .replit file.
```
[packager]
ignoredPackages=["tensorflow"]
```

- Examples

request urls:
```
111.111.111.111/talk
111.111.111.111:8080/talk
example.com:8080/talk
example.com/talk
```

Post
```
{"lang":"en", "message":"Message", "name":"AI Name"}
```

Response
```
{'id': response id , 'message': 'response message'}
```

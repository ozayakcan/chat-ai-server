# Server

- Client: [https://github.com/ozayakcan/chat-ai-client](https://github.com/ozayakcan/chat-ai-client)

# Git
If you are using Git for version control, use this commands.
```
git update-index --assume-unchanged locales/en/train.json
```
```
git update-index --assume-unchanged locales/tr/train.json
```

# Usage

- Request Url Examples:
```
111.111.111.111/talk
111.111.111.111:8080/talk
example.com:8080/talk
example.com/talk
```

- Post Variables
```
locale = (en or tr)
message = (your message)
aiName = (AI's name)
```

- Response
```
{'id': response id(int) , 'message': 'response message'(String)}
```

## Getting Started

```
python3.10 server.py --port 9000 --headers headers.json --body default.html --routes routes
```

## Configure

1.1 Set up custom HTTP response headers in `headers.json`:
```
{
    "Content-Type": "text/html",
    "X-Custom-Header": "MyValue",
    "Server": "SquareSec 1.33.7"
  }
```

2. Modify `default.html` to change the content of the home page
3. Add new routes by creating new page in the `/routes` path

## Logging

Log information about paths, parameters, request headers, cookies, body content, etc.

<img width="499" alt="honeypot" src="https://github.com/user-attachments/assets/4e3da203-755a-47fe-ab59-bfa41bb1b493" />

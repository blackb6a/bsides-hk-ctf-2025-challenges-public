const jwt = require("jsonwebtoken");
const { nanoid } = require("nanoid");
const express = require("express");
const app = express();
const port = 8080;

const FLAG = process.env.FLAG ?? "fakeflag{zzz}";

app.use(express.json());

const users = Object.create(null);

app.post("/flag", (req, res) => {
  const { token } = req.body;
  if (typeof token !== "string") {
    return res.status(400).send("invalid token");
  }

  const decoded = jwt.decode(token);
  if (!decoded) {
    return res.status(400).send("invalid token");
  }

  jwt.verify(token, users[decoded.name].secret, (err, user) => {
    if (err) {
      return res.status(403).send("forbidden");
    } else if (user.admin !== true) {
      return res.status(401).send("unauthorized");
    }

    res.send(FLAG);
  });
});

app.post("/signup", (req, res) => {
  const user = req.body.user;
  if (
    user === undefined ||
    typeof user.name !== "string" ||
    user.name.length > 20
  ) {
    return res.status(400).send("username invalid");
  } else if (JSON.stringify(user).indexOf("admin") > 0) {
    return res.status(409).send("you can't do that!");
  }

  users[user.name] = {
    secret: nanoid(32),
    ...user,
  };

  const token = jwt.sign(user, users[user.name].secret);
  res.send(token);
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
const express = require("express");
const { execSync } = require("child_process");
const app = express();
const port = 8080;

const FLAG = process.env.FLAG ?? "fakeflag{zzz}";

const seeds = Object.create(null),
  tries = Object.create(null);

app.get("/", (req, res) => {
  let { name, key } = req.query;

  if (
    typeof name !== "string" ||
    typeof key !== "string" ||
    parseInt(key, 10).toString() !== key
  ) {
    return res.status(400).send(":(");
  }

  if (name in seeds === false) {
    seeds[name] = Math.floor(1e14 + Math.random() * 9e14);
    tries[name] = 0;
  }

  try {
    key = (
      BigInt(key) +
      BigInt(
        execSync(
          `node --random_seed=${
            seeds[name]
          } -e 'console.log(Array.from(Array(5), Math.random)[${tries[
            name
          ]++}])'`,
          { encoding: "utf-8" }
        ).substring(2)
      )
    ).toString();
  } catch (error) {
    return res.status(500).send(":/ you ran out of tries");
  }

  if (parseInt(key, 16) < parseInt(1e16, 16) && key >= 1e16) {
    return res.send(FLAG);
  }

  res.send(`Try harder, ${key} was not the key.`);
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});

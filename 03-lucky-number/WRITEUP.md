## Techniques
- Predicting `Math.random()`
- Floating point precision error

## Write Up
Let's first ignore the `Math.random()` nonsense and investigate how to pass this check:
```js
if (parseInt(key, 16) < parseInt(1e16, 16) && key >= 1e16) {
    return res.send(FLAG);
}
```

Obviously the key is a string which should be around `1e16`, or `10000000000000000`. Observe that `9999999999999999 === 10000000000000000` holds true due to JavaScript precision errors.

Thus, after some testing, we find that `key = "9999999999999999"` bypasses the check above.

Unfortunately we cannot directly dictate the value of `key`, as a random number is added to it. To set `key` to an arbitrary value, we must know what `Math.random()` will give us.

Notice that a unique seed gets paired up with each "name". This prevents other players from intervening with your predictions of the next `Math.random()`. 

Notice that it generates a maximum of 5 random numbers with the same seed. You can predict the 5th number with https://github.com/PwnFunction/v8-randomness-predictor.

With this, we can first set `?key=0` for the first four requests, plug them into the predictor(remember to add the `0.` prefix), and know what the next `Math.random()` result is, and denote it as `x`.

Simply set `?key` to `9999999999999999-x`(you must not perform this operation in JavaScript for the same reasons listed above), and you should see the flag.

Example:
```python
# First four results from /?key=0&name=zzz
# 7286685292279402
# 8832972610139662
# 9788422146821925
# 24261452563464658

# Shove the numbers into the predictor like this:
sequence = [
    0.7286685292279402,
    0.8832972610139662,
    0.9788422146821925,
    0.24261452563464658
]

# Get 0.11928270479204839 as result
>>> 9999999999999999-11928270479204839
-1928270479204840

# Visit /?key=-1928270479204840&name=zzz and tada!
```

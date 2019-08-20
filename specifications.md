# Die Roll Formatting:

Random number generation in this project is achieved through die rolls. Die rolls must
follow this specific format : `XdY+Z`

- `X` is the number of dice to roll
- `Y` is the number of faces of each die
- `Z` is a flat modifier. The plus (`+`) sign will add that modifier, while the minus (`-`)
sign will subtract the modifier from the result.

`X` is optional. If omitted, `X` will default to 1.

`Z` is optional. If omitted, `Z` will default to 0.


# Treasure Formatting:

Each treasure is formatted in the `treasures.json` file, and each treasure looks like this :

```json
  "A": {
    "thousands": true,
    "coins": {
      "cc": ["25%", "1d6"],
      "sc": ["30%", "1d6"],
      "ec": ["20%", "1d4"],
      "gc": ["35%", "2d6"],
      "pc": ["25%", "1d2"]
    },
    "gems": ["50%", "6d6"],
    "jewels": ["50%", "6d6"],
    "items": ["30%", ["random", "random", "random"]],
    "average_value": 17000
  },
```

The keys for that dictionary are as follows :

- `thousands` : if the coin value is supposed to be in thousands or not
- `coins` : a dictionary containing a key for each coin type. For each coin type, 
define the chance to get that coin type in the treasure, and the amount, as a dice roll.
- `gems` : a list of length 2 describing the chance to get gems in the treasure, 
and the amount of gems as a dice roll.
- `jewels` : similar to `gems`, but for jewels.
- `average_value` : the average value, in gc, of the treasure, excluding magic items.
- `items` : a list of length 2. The first argument is the chance to get magic items 
in the treasure, the second is a list of loot table names.

For items, the loot table names can be as follows :

```
"other-weapons/swords/armors"
"random"
"potions" (or any other loot table name)
"random|other-weapons|swords"
"1d8:potions"
```

The pipe (`|`) character is used in conjunction with the `"random"` loot table name 
to exclude specific loot tables from the randomization.

The colon (`:`) character is used in conjunction with any loot table to repeat a roll on
that table any number of times (as specified by the die roll prefixing the `:` character)

The slash (`/`) character is used to combine any number of loot tables together.

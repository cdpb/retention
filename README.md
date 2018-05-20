## Simple directory retention

### Usage

adjust variables in header for your needs

```
dirs = "/mnt/archive/"

daysaweek = 3
weekstokeep = 104
daystokeep = 60
monthlytokeep = 12
yearlytokeep = 10
```

### Limitations

* only works with dir format `YYYY-MM-DD`
  * can be easly change in `getdirnames()`

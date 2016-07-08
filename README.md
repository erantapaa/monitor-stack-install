
### Synopsis

```sh
$ stack install ...list of packages... > output 2>&1 &
$ ./monitor-stack > output.stats
...
$ ./compute-utilization
$ ./make-data-js
$ open report.html
```

### Introduction

This repo contains scripts used to monitor a long running `stack install`
job under Linux.

The script `monitor-stack` will periodically write statisics about the install job to the file `output.stats`. The format of each line is:

    1467875898.43 27.8 6 explicit-exception-0.1.8 fail-4.9.0.0 farmhash-0.1.0.5 extra-1.4.7 Cabal-1.22.8.0 Cabal-ide-backend-1.23.0.0
    ^- unix time  ^- % idle
                       ^- number of active workers
                         ^- list of packages being worked on

Stats are written to the file approximately once every 5 seconds.

`monitor-stack` will us `ps` to find the `stack install` process automatically.
However, if it fails to find the process you can specify its pid as the first argument:

    monitor-stack pid... > output.stats

`monitor-stack` looks for the exact string `stack install` in the `ps` output.

`compute-utilization` will compute the average %-idle from the `output.stats` file.

`make-data-js` will create JSON data from `output.stats` for use with `report.html`.

`report.html` will show a graph of CPU utilization over the course of the job.

### Caveats

- Only tested under Ubuntu Linux


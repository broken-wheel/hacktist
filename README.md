# hacktist

## Build

To build the _hackt_ toolkit:
```sh
docker buildx build --platform=linux/arm64,linux/amd64 \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --cache-from brokenwheel/hackt \
    --target=release \
    -f hackt_docker/Dockerfile -t brokenwheel/hackt . --push
```

To build the _visualizer_:
```sh
docker buildx build --platform=linux/arm64,linux/amd64 \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --cache-from brokenwheel/act-utils \
    --target=release \
    -f act-utils/Dockerfile -t brokenwheel/act-utils . --push
```

## Usage
Here's an illustration of the usage with an example.

Create a `buffer-hse.hac` CHP specification file under _examples/_ directory:
```
// Assume that 1 unit of time is 1us
preal l_delay= 100000.0;
preal r_delay= 200000.0;

bool l, r;

chp {
    r-, l-;
    *[[r]; $(after=r_delay) l+; [~r]; $(after=r_delay) l-],
    *[[~l]; $(after=l_delay) r+; [l]; $(after=l_delay) r-]
}
```

Create a `run.chpsim` _run_ file also under _examples/_ directory:
```
# use event-specific constant delay
timing per-event
# print activity of all events
watchall-events
# record trace of all events to file
trace buffer-hse.bin
# advance the simulation in time units
# this corresponds to 100s of sim time since we assume that 1 unit of time is 1us
advance 100000000
trace-close
exit
```
> We can set `timing random` to randomize the delay, or
> `timing uniform` to use uniform delay specified using `uniform-delay = <X us>`

Compile the specification file:
```sh
docker run --rm -it -v $PWD/examples:/app brokenwheel/hackt haco buffer-hse.hac buffer-hse.haco
docker run --rm -it -v $PWD/examples:/app brokenwheel/hackt haccreate buffer-hse.haco buffer-hse.hacc
```

Run the simulation:
```sh
docker run --rm -it -v $PWD/examples:/app brokenwheel/hackt sh -c "cat run.chpsim | hacchpsim buffer-hse.hacc"
```

Once the simulation runs without any errors, dump the simulation results using:
```sh
docker run --rm -it -v $PWD/examples:/app brokenwheel/hackt hacdump.sh -d buffer-hse.dot -t buffer-hse.out -b buffer-hse.bin -s chp buffer-hse.hacc
```

Then visualize using:
```sh
docker run --rm -it -v $PWD/examples:/app -p 8988:8988 brokenwheel/act-utils buffer-hse -s -w 5000000
```
This should make the visualizer window available at http://127.0.0.1:8988
> We fix the visualizer window to 5s (i.e., 5000000us) using the `-w` flag.
> 
> Use &lt;right&gt; and &lt;left&gt; arrow keys to step forward and backwards, respectively, through the transition events.
> You may have to click inside the window to bring focus.
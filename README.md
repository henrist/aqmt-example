# Example usage of the AQM test framework

This demonstrates the use of https://github.com/henrist/aqmt

## Getting started

Make sure you fulfill all the dependencies listed at the
aqmt repository.

### Building all programs

Build (and load) the schedulers.

```bash
make
```

If you are going to use Docker, also run:

```bash
make aqmt_docker
```

Note that if you have not set up rootless usage of Docker, you will have to
add `sudo` to the `docker-compose` commands in `Makefile`.

This might take some time, as it will build the Docker image including our
needed packages, compile iproute2, and add other utilities.

### Run Docker containers and connect to AQM container

Start the Docker containers in a seperate terminal:

```bash
make start_docker
```

If everything goes well, you will now have 6 running Docker containers.

SSH into the AQM container:

```bash
make ssh_aqm
```

You are now inside the Docker container! The `aqmt-example` repository you
have cloned, is now available in `/opt/testbed`, and you should be at that
directory. Note that files you add outside of these directories will not
be visible to you outside Docker!

The `aqmt` repository is available in `/opt/aqmt`, and you should have access
to all the programs and variables we are using.

You can try this by:

```bash
echo $IP_CLIENTA
aqmt-show-setup
```

### Running a test

While you are connected with SSH to the AQM container, start tmux, which
is a terminal multiplexer allowing us to have multiple terminals:

```bash
tmux
```

You can now run the example test. For fun, we run it interactivly so we
can look what is going on. This is why we need tmux.

```bash
TEST_INTERACTIVE=1 ./example.py
```

Accept to start the test.

When the test is finished, you can have a look inside `results/example`
directory which will contain all the test data, as well as plottings
from the test!

Now feel free to edit the example and design your own tests.

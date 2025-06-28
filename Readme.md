# plywoodpirate

![](https://img.shields.io/badge/Push%20Requests-welcome-apple)
![](https://img.shields.io/maintenance/yes/2025)
![](https://img.shields.io/github/last-commit/michagrandel/lumbermill)
![](https://img.shields.io/github/actions/workflow/status/michagrandel/lumbermill/main.yaml)
![](https://img.shields.io/github/license/michagrandel/lumbermill)

plywoodpirate extends the standard library of python with some useful general purpose tools. 

## Features

### application

* **BasicApplication** — Basic command line application class. Provides logging, configuration and other useful features 

### asyncio

* **future_lru_cache** — lru_cache for async functions.
* **to_thread** — Run a synchronous function in a separate thread.
* **awaitable** — Convert synchronous function to an async function via thread.
* **tls_handshake** — Perform TLS handshake with a stream reader & writer.
* **CoroutineClass** — Class pattern for implementing object-based coroutines.

### buildins

* **classproperty** — Decorator for defining a method as a property and classmethod.
* **convert** — convert values from and to different types

### collections

* **Item** — An interface for type-agnostic operations between different types.
* **nestednamedtuple** — Creates a nested namedtuple.
* **fdict** — Forces nestednamedtuple to not convert dict to namedtuple.
BidirectionalDict — Dictionary with two-way capabilities.
* **ObjectDict** — Dictionary that can be accessed as though it was an object.
* **OverloadedDict** — Dictionary that can be added or subtracted to.
* **UnderscoreAccessDict** — Dictionary with underscore access.
* **FrozenDict** — Dictionary that is frozen.
* **MultiEntryDict** — Dictionary that can have multiple entries for the same key.
* **ItemDict** — Dictionary that utilizes Item for key and values. 

All *Dict* types above can be combined together (as mixins) to create unique dictionary types.

### config

* **ConfigurationFile** — Simple configuration management for scripts and small tools
* **make_config** — Stores configuration dictionary in-memory.
* **config** — Access in-memory configuration as dictionary.
* **conf** — Access in-memory configuration as nestednametuple.

### datetime

* **convert** — Convert time and dates between different formats.

### functools

* **timeout** — Decorator to add timeout for synchronous and asychronous functions.

### logging

* **Logger** and **getLogger** — default logging configuration and basic features for small to medium tools and scripts, include structured logging.

### pdb

* **sprinkle** — Prints the line and file that this function was just called from.

### sockets

* **is_ip** — Checks if a string is an IP address.

### string

* **ANSI Formatting** — Color formatting.
* **Format** — Persistent ANSI formatter that takes a custom ANSI code.
* **Style** — Persistent ANSI formatter that allows multiple ANSI codes.
* **supports_color** — Check's if the user's terminal supports color.
* **strip_ansi** — Removes ANSI codes from string.

### sys

* **platform** — collect system information 

### textwrap

* **unindent** — Removes indent and white-space from docstrings.

## 💾 Installation

You can install the tool with pip.

*Install with pip:*

```bash

pip install plywoodpirate

```

## 🔌 How to use

Examples will be added soon. You will find some examples in the source code.

## 🛠️ How to build from source

This project uses [hatch](https://hatch.pypa.io/latest/) as build-system.

You can build the project using the default hatch commands. Use this to run a simple
build with default settings:

```bash

hatch build

```

## :+1: How to contribute

Pull requests are allways welcome! :sparkles:

If you don't know where to start, check out the discussions in Github or
open a new one.

Thanks for your interest in contributing! :beers:

Don't forget to read the [Code Of Conduct][Code Of Conduct.md] for more information!

## Special thanks

This project uses code from the following projects:

* [Toolbox](https://github.com/synchronizing/toolbox) (<> by [Felipe Faria](linkedin.com/in/synchronizing))

## :memo: Miscellaneous

- *License*: [Affero GPL](License.md)
- *Main contributor*: [Micha Grandel](mailto:michagrandel@proton.me)
- *Uses*: [Python 3.13+](https://www.python.org/)

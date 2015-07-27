# harpseal

[![Build Status](https://travis-ci.org/ssut/harpseal.svg?branch=master)](https://travis-ci.org/ssut/harpseal)
[![Coverage Status](https://coveralls.io/repos/ssut/harpseal/badge.svg?branch=master&service=github)](https://coveralls.io/github/ssut/harpseal?branch=master)
[![Code Climate](https://codeclimate.com/github/ssut/harpseal/badges/gpa.svg)](https://codeclimate.com/github/ssut/harpseal)
[![Documentation Status](https://readthedocs.org/projects/harpseal/badge/?version=latest)](https://ssut.github.io/harpseal)
[![Dependency Status](https://gemnasium.com/ssut/harpseal.svg)](https://gemnasium.com/ssut/harpseal)

![](https://ssut.github.io/harpseal/_static/harpseal-150x150.png)

**Harpseal**, a next generation linux system resource monitoring tool based on plugins.

For more details, please refer to the [documentation here](https://ssut.github.io/harpseal/).


## Features

* **Plugin** — Harpseal is built upon a plugin system which allows support for new plugin to be easily created and added. It’s quite easy in fact as you can see in this documentation. even you don’t know anything about Harpseal structures.
* **HTTP API** - JSON/JSONP (callback)
    * It is possible to create a cluster monitoring system with super simple HTTP API.
    * As I’ve written above, even you can get jsonp callback mechanism; the more easily, you can create it with Javascript only.
* **Light-weighted**: with event-driven. Harpseal requires a lower memory footprint than many of system resource monitoring tools.
* **Free**: Harpseal is totally free to use even for commercial purposes.
* **Super easy to install**: it’s super easy to install and set up Harpseal server on your Debian-based linux distros because it’s already ready.

## Built-in plugins

* cpu - CPU (each CPU usage, PID count and CPU times.)
* mem - Memory (Detailed memory usage data including swap memory.)
* disk - Disk (each disk IOs and spaces.)
* net - Network (Network statistics.)

... and more are planned to be added soon.

## Installation

Please see the [documentation](https://ssut.github.io/harpseal/).

## TODO

* Text-based reporting, would be used to such as *top*.
* Web GUI, currently working on [another branch](https://github.com/ssut/harpseal-web).

## Help

You can find me on **#ssut** on freenode IRC or you can get in touch via Telegram at **[@ssssut](https://telegram.me/ssssut)**.

## Contributing

1. Fork this project.
2. Create a topic branch.
3. Implement your feature or bug fix.
4. Run `py.test -v` or `python -m py.test -v`.
5. Add a test for your feature or bug fix.
6. Run step 4 again. If your changes are not 100% covered, go back to step 5.
7. Commit and push your changes.
8. Submit a pull request.

## License

**Harpseal** is offered under the [Apache license](http://www.apache.org/licenses/LICENSE-2.0), which like BSD or MIT, is a lot more permissive than the GPL License and compatible with GPL v3 only.
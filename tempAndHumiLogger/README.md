Temperature and Humidity Logger
===============================

Runs different sensors in parallel in order to get more accurate results.
Provides a website wîth visualizations.

Prerequisites
-------------

Install [C library for Broadcom BCM 2835 as used in Raspberry Pi](http://www.airspayce.com/mikem/bcm2835/) since it is required by the node module [node-dht-sensor](https://github.com/momenso/node-dht-sensor) we use.

Installation
------------

    npm install


Run
---

    node index.js
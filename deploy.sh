#!/bin/bash

rsync --delete -avz raspberry/ pi@192.168.70.144:/home/pi/sources

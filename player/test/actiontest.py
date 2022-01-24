#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os

if os.getenv('CI'):
    print('Looks like GitHub!')
else:
    print('Maybe running locally?')

import tempfile
# -*- coding: utf-8 -*-
"""Regenerate probe-dom.html, then read it.

read_probe.py only parses a dump that is already on disk. Run on its own after
an edit it happily reports the previous build's geometry, which is what it did
once here. This drives the browser first, on a profile thrown away each time so
no stylesheet can be served from cache, and only then hands over to the reader.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8807
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-probe')
src = sys.argv[1] if len(sys.argv) > 1 else 'case-story.html'
out = os.path.join(HERE, 'probe-dom.html')

shutil.rmtree(PROFILE, ignore_errors=True)
subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                '--no-default-browser-check', '--force-prefers-reduced-motion',
                '--user-data-dir=' + PROFILE, '--virtual-time-budget=90000',
                '--window-size=2200,1700', '--dump-dom',
                'http://127.0.0.1:%d/probe.html?src=%s' % (PORT, src)],
               stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
print('probe: %s' % src)
subprocess.run([sys.executable, os.path.join(HERE, 'read_probe.py')])

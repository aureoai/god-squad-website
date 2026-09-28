# -*- coding: utf-8 -*-
"""validate.py needs its own PROJECT constant.

The tracked-originals check guards the PROTOTYPE files, which Phase 10 left at
the project root when it moved the theme into god-squad-theme/.
"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phase8', 'validate.py')
s = open(p, encoding='utf-8').read()

OLD = 'THEME = r"C:\\Users\\TEST\\OneDrive\\Documents\\GodSquad Website\\god-squad-theme"'
NEW = OLD + '\nPROJECT = r"C:\\Users\\TEST\\OneDrive\\Documents\\GodSquad Website"'

assert s.count(OLD) == 1, 'THEME constant not found'
s = s.replace(OLD, NEW, 1)
s = s.replace('os.path.join(build.PROJECT,', 'os.path.join(PROJECT,')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('validate.py: PROJECT constant added and the check repointed')

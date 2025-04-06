# About
Mutant is an configuration file manager that uses the M4 macro
language to generate configuration variations for multiple computers
with different requirements.

It does do by allowing configuration templates to lock certain
features behind dependencies as well as allow them to provide
dependencies.

Mutant will then do dependency resolution to try to enable as much
features as it can.

# Dependencies

- Python3.11
- [GNU Stow](https://www.gnu.org/software/stow/)
- [GNU M4](https://www.gnu.org/software/m4/m4.html)

# Bugs
Although M4 was a fun language to play around with, M4 macro
expansion outputs text not tokens, resulting in tons of quoting
and macro hygiene issues.

It was a terrible language choice for this project and you should
not use it if you value your sanity.

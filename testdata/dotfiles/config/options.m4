# Each option name is on a newline.
# Whitespace act as delimiters.
# This file will be run through m4.
# One use of m4 is to get generate options
# based on installed packages.
# Ex. (for gentoo)
#     syscmd(`qlist -I')
# I perfer to prefix generated options.
# Ex.
#     syscmd(`qlist -I | sed "s/^/pack:/"')

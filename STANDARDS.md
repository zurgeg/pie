# Coding standards
We follow a subset of GNU standards. These are:
- Check every system call for an error return.
- In error checks that detect “impossible” conditions, just abort.
- If you make temporary files, check the TMPDIR environment variable; if that variable is defined, use the specified directory instead of /tmp.

Additionally, we have one extra "in-house" standard:
- If on Windows, abort immediately. (I'm joking. Please do not do that)

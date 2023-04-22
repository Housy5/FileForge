# FileForge
A small console tool to generate files for testing.

Usage:

The program will always output the generated file to the desktop for ease of use.
When asked, enter a name that is compatible with Windows limitations.
Next enter the desired size. The default is in bytes how ever when a suffix is provided it might modify the unit.
for example:
  When "128" is entered it will be 128 bytes.
  When "128mb" is entered it will be 128 mb.
  Available suffixes are: b, kb, mb, gb, and tb.
Enter "y" to confirm and wait for it to generate your file.
After that you should be finished!

Dependacies:
  -psutil | pip install psutil

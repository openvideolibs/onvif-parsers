(usage)=

# Usage

Assuming that you've followed the {ref}`installations steps <installation>`, you're now ready to use this package.

Start by importing it:

```python
import onvif_parsers
```

The module only has a single function, [`parse`](../onvif_parsers.html#onvif_parsers.parse), which you can pass an onvif event to and receive a parsed event type.

# Main Tester

There is also a main command line entry point in the module that can be used to test receiving events from a camera. Run the following for usage instructions:

```shell
python -m onvif_parsers --help
```

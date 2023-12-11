# Floodify

A python library for building and evaluating network models of flood storage areas and hydrological processes.

For an example of usage, see the file _example_30k.ipynb_.

More detail to come...

To Do:
- Allow saving and reading of models as a single config file
    - Or add an extra config file to represent remaining nodes and connectivity.
    - Actually it's probably best to incorporate everything into a single network configuration file and 
- Consider turning FSA into a dataclass and extracting the calculation/functionality to Network class
    - In keeping with separating data from functionality
- Consider turning HypsoCurve into a dataclass
- Current flow is instantaneous. There is no consideration of flow routing between FSAs. This will be useful to consider in the future.
- Add logging functioanlity

![Network Outfall Flow](https://github.com/BMcCawley/floodify/blob/main/visuals/outfall_flow.png)
![Network FSA Flow](https://github.com/BMcCawley/floodify/blob/main/visuals/fsa_flow.png)
![Network FSA Volume](https://github.com/BMcCawley/floodify/blob/main/visuals/fsa_volume.png)
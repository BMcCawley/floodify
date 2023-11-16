from numpy.typing import ArrayLike
import networkx as nx
from .fsa import FSA
import numpy as np
from typing import Callable
from scipy.optimize import minimize


class Network(nx.DiGraph):
    def __init__(self, dt: float):
        super().__init__()
        self.dt = dt

    def add_fsa(self, name: str, fsa: FSA):
        self.add_node(name, type="fsa", fsa=fsa, stage=None, volume=None, flow=None)

    def add_inflow(self, name: str, flow: ArrayLike):
        self.add_node(name, type="inflow", flow=flow)

    def add_junction(self, name: str):
        self.add_node(name, type="junction", flow=None)

    def node_inflow(self, name: str) -> ArrayLike:
        """
        Calculate the total inflow to a node by summing the flows from all predecessor nodes.
        The flows are summed element-wise.
        """
        return np.sum(
            [
                self.nodes[predecessor]["flow"]
                for predecessor in self.predecessors(name)
            ],
            axis=0,
        )

    def set_fsa_attribute(self, fsa_name: str, attribute: str, value: float) -> None:
        "Set an FSA attribute in the network."
        setattr(self.nodes[fsa_name]["fsa"], attribute, value)

    def run(self):
        """
        Calculate flow through the network.
        This method checks if all nodes are connected to the rest of the network in at least one direction.
        Then, in order from upstream to downstream, the inflow into each FSA is caculated and the FSA is run.
        """
        if not nx.is_weakly_connected(self):
            # Network structure may still be invalid even if ValueError is not raised here.
            raise ValueError("Network structure is not valid.")

        for name in nx.topological_sort(self):
            if self.nodes[name]["type"] == "inflow":
                continue
            elif self.nodes[name]["type"] == "junction":
                self.nodes[name]["flow"] = self.node_inflow(name)
                continue
            inflows = self.node_inflow(name)
            stage, volume, outflow = self.nodes[name]["fsa"].run(inflows, self.dt)
            self.nodes[name]["stage"] = stage
            self.nodes[name]["volume"] = volume
            self.nodes[name]["flow"] = outflow

    def _objective_function(
        self,
        x: ArrayLike,
        node_parameters: list[tuple[str]],
        objective_function: Callable,
    ) -> float:
        """
        Wrapper function for user-defined objective function. This is passed to scipy.optimize.minimize.
        This function sets FSA parameters and then runs the network before calculating the objective function result.
        x is a 1-D array of parameters to optimise. This is set by scipy.optimize.minimize.
        node-parameters is a list of tuples specifying the nodes and their parameters to be optimised.
        objective_function is the user-defined objective function which is called on the network.
        Returns scalar value of the result of calling the objective function.
        """
        # Loop through each node parameter to optimise and set new values
        for value, node_parameter in zip(x, node_parameters):
            self.set_fsa_attribute(node_parameter[0], node_parameter[1], value)
        # Run the network with the new values
        self.run()
        # Return scalar value result of the objective function, which is called on the network itself
        return objective_function(self)

    def optimise_network(
        self,
        parameter_config: list[dict],
        objective_function: Callable,
        method: str = "Powell",
    ) -> float:
        """Optimises the network using given parameter configuration and objective function"""
        # Set nodes and parameters to be optimised
        node_parameters = [
            (parameter["name"], parameter["parameter"])
            for parameter in parameter_config
        ]
        # Set initial conditions for parameters
        x0 = [parameter["initial"] for parameter in parameter_config]
        # Set the bounds for parameter space
        bounds = [parameter["bounds"] for parameter in parameter_config]
        # Call minimize using self._objective_function
        result = minimize(
            fun=self._objective_function,
            x0=x0,
            args=(node_parameters, objective_function),
            method=method,
            bounds=bounds,
            # options={"disp": True},
        )
        # By calling scipy.optimize.minimize, the optimised parameter values should be assigned in the network
        return result

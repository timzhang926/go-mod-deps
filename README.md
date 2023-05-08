# go-mod-deps

# Go Mod Dependency Tree

## Why
For any Go project, a list of Go packages are reused. These packages have complicated dependencies between them, which can be difficult to keep track of. To help with this, the Go Mod Graph command provides a way to view these dependencies and show the relationships between the packages recursively. This can be useful to understand the full picture of the dependencies, however the output of the go mod graph can be difficult to comprehend. 

* To make it easier to understand, a flat dependencies tree can be used to visualize the graph and make it easier to understand the relationships between the packages.

* If a package is found to have vulnerabilities or is at the end of its maintenance cycle, it can be difficult to know which packages are impacted and should be upgraded. This is especially true in large systems with many interconnected packages. In these cases, it is important to have a tool in place to track the packages relationships, so that any potential issues can be identified and addressed quickly.

* The dependencies of a Go project form our supply chain, and we need to be aware of the software bill of materials. The output of the go mod graph command provides us with the initial information, but it is not easy to be processed by downstream pipelines. To address this issue, the JSON format is very useful.

* To gain a better understanding of the dependencies, it can be helpful to visualize them in a picture format. This could be done using a png or svg file, which can provide a clear and concise representation of the connections between the different components. Visualizing the dependencies in this way can help to quickly identify any potential issues or areas of improvement.

# Screenshots 
## Dependency tree
<img src="./images/deps_tree.png" alt="dependency tree" width="60%" height="60%" title="dependency tree">

## Dependency tree in json
<img src="./images/deps_json.png" alt="dependency tree in json" width="70%" height="70%" title="dependency tree in json">

## Dependency tree in dot
<img src="./images/deps_dot.png" alt="dependency tree in dot" width="100%" height="70%" title="dependency tree in dot">

## The big picture with all dependencies
<img src="./images/deps1.png" alt="big dependency tree" width="100%" height="100%" title="big picture of dependency tree">

## Subset picture with all paths to an Go package.
<img src="./images/deps2.png" alt="sub dependency tree" width="50%" height="50%" title="big picture of sub dependency tree">

# Usage
<img src="./images/deps_help.png" alt="gomoddeps help" width="100%" height="100%" title="gomoddeps help">

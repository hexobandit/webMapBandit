# webMapBandit
WebMapBandit is a tool that maps GET, POST, and other HTTP requests made by a website by processing .har (HTTP Archive) files. It visualizes the network of requests using different layouts and an adjustable URL depth representation.

### Key Features:

- HAR File Parsing: Extracts URLs and HTTP methods from .har files.
- Builds a directed graph where nodes represent URLs and edges represent the HTTP methods.
- Customizable URL Depth: Allows for limiting the depth of the URL path to focus on specific levels of the request hierarchy.
- Graph Layout Options: Supports various layout algorithms for visualizing the graph.

### Usage:

1. Modify Configurations:

<img width="890" alt="image" src="https://github.com/user-attachments/assets/2414ea87-100f-46fc-8d73-cd5a2233e335">

2. Run the script:

<img width="1260" alt="image" src="https://github.com/user-attachments/assets/c6bbcfcc-7f39-43b5-b6ac-39b0c9c93806">

### How to Obtain a .HAR File:

You can obtain .har files using a variety of tools:

1. Browser Developer Tools:
	•	Open Developer Tools (F12) in your browser (Chrome, Firefox, Edge, etc.).
	•	Go to the Network tab.
	•	Load the website you want to analyze.
	•	Right-click anywhere in the request list and choose Save all as HAR or Export HAR.

2. Burp Suite:
	•	Launch Burp Suite and set it up as a proxy.
	•	Capture the website traffic.
	•	In the HTTP history tab, right-click the requests and choose Save Items to export them as a .har file.

3. Other Tools:
	•	Postman: You can export the request history as a .har file from the Postman app.
	•	Fiddler: Capture HTTP/HTTPS traffic and export it as .har using Fiddler.

### Graph Layouts:

	dot: Hierarchical layout (default for directional graphs).
	neato: Force-directed layout for general graphs.
	twopi: Radial layout with concentric circles.
	circo: Circular layout, good for cyclic graphs.
	fdp: Force-directed layout optimized for larger graphs.
	sfdp: Scalable version of fdp for very large graphs.
	patchwork: Grid/tiling layout.
	osage: Clustered layout for grouped nodes.

**WebMapBandit is ideal for understanding the structure and flow of web requests, making it useful for security analysis and performance optimization.**

### Troubleshooting

Working with ```venv``` seems to cause issues with ```pygraphviz```, so if you don`t want to lose your mind, just dont use the virtual env.  
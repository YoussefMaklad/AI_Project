var nodes = new vis.DataSet([]);
var edges = new vis.DataSet([]);
var heuristic = {};
var selectedNodeId = null;
var selectedEdgeId = null;
var container = document.getElementById("mynetwork");
var nodeSelect = document.getElementById("nodeSelect");
var nodeSelect1 = document.getElementById("nodeSelect1");


var data = {
  nodes: nodes,
  edges: edges,
};

var options = {};
var network = new vis.Network(container, data, options);

var nodeIdCounter = 1;

function addNode() {
  // Use the counter as the new node ID
  var newNodeId = nodeIdCounter++;

  var newNodeLabel = "Node " + newNodeId;

  var nodeFont = {
    color: "white",
  };

  var newNode = {
    id: newNodeId,
    label: newNodeLabel + "\nh=1",
    color: "palevioletred",
    font: nodeFont,
    heuristic: 1,
  };

  // Check if the node with the same ID already exists
  if (nodes.get(newNodeId) === null) {
    nodes.add(newNode);
    heuristic[newNodeLabel] = newNode.heuristic;

    // Update the select dropdown with the names of every node
    updateNodeSelect();
    updateNodeSelect2();
  } else {
    console.error("Node with ID " + newNodeId + " already exists.");
  }
}

function updateNodeSelect() {
  var nodeOptions = nodes
    .get()
    .map(
      (node) =>
        `<option value="${node.label.split("\n")[0]}">${node.label}</option>`
    )
    .join("");
  nodeSelect.innerHTML = `<option value="0">Start:</option>${nodeOptions}`;
}
function updateNodeSelect2() {
  var nodeOptions = nodes
    .get()
    .map(
      (node) =>
        `<option value="${node.label.split("\n")[0]}">${node.label}</option>`
    )
    .join("");
  nodeSelect1.innerHTML = `<option value="0">Goal:</option>${nodeOptions}`;
}

network.on("doubleClick", function (params) {
  if (params.nodes.length > 0) {
    if (!selectedNodeId) {
      selectedNodeId = params.nodes[0];
      customAlert("Source node selected. Now double click on the target node.");
    } else if (params.nodes[0] !== selectedNodeId) {
      var connectedNodeId = params.nodes[0];
      var newEdge = {
        from: selectedNodeId,
        to: connectedNodeId,
        label: "1",
        color: "#0969b8",
        width: 5,
        font: { size: 16 },
      };
      edges.add(newEdge);
      printNodeList();
      printEdgeList();
      selectedNodeId = null;
    }
  }
});

function editNode() {
  var selectedNodeId = network.getSelectedNodes()[0];
  if (selectedNodeId) {
    document.getElementById("myModal").style.display = "block";
    document.getElementById("newLabel").value = nodes
      .get(selectedNodeId)
      .label.split("\n")[0];
    document.getElementById("newHeuristic").value =
      heuristic[nodes.get(selectedNodeId).label.split("\n")[0]];
  } else {
    customAlert("Please select a node to edit.");
  }
}

function closeModal() {
  document.getElementById("myModal").style.display = "none";
}

function updateNodeLabelAndHeuristic() {
  var selectedNodeId = network.getSelectedNodes()[0];
  var newLabel = document.getElementById("newLabel").value;
  var newHeuristic = parseInt(document.getElementById("newHeuristic").value);

  if (selectedNodeId && newLabel.trim() !== "") {
    delete heuristic[nodes.get(selectedNodeId).label.split("\n")[0]];
    heuristic[newLabel] = newHeuristic;
    nodes.update({
      id: selectedNodeId,
      label: newLabel + "\nh=" + newHeuristic,
    });
    updateNodeSelect();
    updateNodeSelect2();
    closeModal();
  } else {
    alert("Invalid input. Please enter a valid label and heuristic value.");
  }
}

function editEdge() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  if (selectedEdgeId) {
    document.getElementById("edgeModal").style.display = "block";
    clearEditEdgeInput();
  } else {
    customAlert("Please select an edge to edit.");
  }
}

function clearEditEdgeInput() {
  document.getElementById("newEdgeLabel").value = "";
}

function closeEdgeModal() {
  document.getElementById("edgeModal").style.display = "none";
}

function updateEdgeLabel() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  var newEdgeLabel = document.getElementById("newEdgeLabel").value;

  if (selectedEdgeId && newEdgeLabel.trim() !== "") {
    edges.update({ id: selectedEdgeId, label: newEdgeLabel });
    closeEdgeModal();
  } else {
    alert("Invalid input. Please enter a valid label.");
  }
}

function solve() {
  var strategy = document.getElementById("strategy").value;
  var start = document.getElementById("nodeSelect").value;
  var nodeList = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
  }));

  var edgeList = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
    label: edge.label,
  }));
  // var start = nodeList[0].from;
  console.log("Node List:", nodeList);
  console.log("Edge List:", edgeList);
  console.log("Heuristic:", heuristic);
  console.log("Solving using strategy:", strategy, goal, start);
  fetch("http://localhost:5000/call_function", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      edge: nodeList,
      cost: edgeList,
      heuristic: heuristic,
      strategy: strategy,
      start: start,
      goal: goal,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Log the result in the console
      console.log("Result:", data.result);
    })
    .catch((error) => console.error("Error:", error));
}

function customAlert(message) {
  var customAlertElement = document.getElementById("customAlert");
  customAlertElement.textContent = message;
  customAlertElement.style.display = "block";

  setTimeout(function () {
    customAlertElement.style.display = "none";
  }, 2000);
}

function deleteSelectedNode() {
  var selectedNodeId = network.getSelectedNodes()[0];

  if (selectedNodeId) {
    var selectedNode = nodes.get(selectedNodeId);

    if (selectedNode) {
      console.log("Deleting node:", selectedNode);

      // Remove all edges connected to the selected node
      var connectedEdges = edges.get({
        filter: (edge) =>
          edge.from === selectedNodeId || edge.to === selectedNodeId,
      });
      edges.remove(connectedEdges);

      // Remove the selected node
      nodes.remove({ id: selectedNodeId });

      delete heuristic[selectedNode.label.split("\n")[0]];

      // Find and remove the corresponding option from the dropdown
      var options = document.getElementById("nodeSelect").options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === selectedNode.label.split("\n")[0]) {
          document.getElementById("nodeSelect").remove(i);
          break;
        }
      }
      var options2 = document.getElementById("nodeSelect1").options;
      for (var i = 0; i < options2.length; i++) {
        if (options2[i].value === selectedNode.label.split("\n")[0]) {
          document.getElementById("nodeSelect1").remove(i);
          break;
        }

        // selectedNodeId = null;

        // printNodeList();
        // printEdgeList();
      }
    } else {
      customAlert("Selected node not found.");
    }
  } else {
    customAlert("Please select a node to delete.");
  }
}

function removeSelectedEdge() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  if (selectedEdgeId) {
    edges.remove({ id: selectedEdgeId });
    printEdgeList();
  } else {
    customAlert("Please select an edge to remove.");
  }
}

function printNodeList() {
  var nodeListWithLabels = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
  }));
  console.log("Node List:", nodeListWithLabels);
}

function printEdgeList() {
  var edgeListWithLabels = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
    label: edge.label,
  }));
  console.log("Edge List:", edgeListWithLabels);
}

function printHeuristic() {
  console.log("Heuristic:", heuristic);
}

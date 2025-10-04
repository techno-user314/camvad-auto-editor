import { entrypoints } from "uxp";

entrypoints.setup({
  panels: {
    markerToMulticamPanel: {
      show(event) {
        document.getElementById("runBtn").onclick = () => markersToCameraSwitches();
      }
    }
  }
});

async function markersToCameraSwitches() {
    const { project } = require("premiere");
    const qe = require("qe"); // access QE DOM (still used for multicam)

    const activeSeq = project.activeSequence;
    if (!activeSeq) {
        console.log("No active sequence open.");
        return;
    }

    const markers = activeSeq.markers;
    if (!markers || markers.numMarkers === 0) {
        console.log("No markers found.");
        return;
    }

    // Map marker colors → multicam camera angles
    const colorToCamera = {
        0: 1, // Green
        1: 2, // Red
        2: 3, // Yellow
        3: 4, // Blue
        4: 5  // Magenta, etc.
    };

    let marker = markers.getFirstMarker();
    while (marker) {
        const camNum = colorToCamera[marker.colorIndex];
        if (camNum) {
            // Move playhead
            activeSeq.setPlayerPosition(marker.start.ticks);

            // Add edit
            qe.executeCommandById(400); // "Add Edit"

            // Switch multicam angle
            qe.executeCommandById(231 + (camNum - 1)); 
            console.log(`Marker at ${marker.start.seconds}s → Camera ${camNum}`);
        }
        marker = markers.getNextMarker(marker);
    }
}


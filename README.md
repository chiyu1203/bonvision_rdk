# BonVision random dot kinematogram in Bonsai
This is a repository storing a workflow to present random dot kinematogram with BonVision package in Bonsai.

A random dot kinematogram is a motion‑perception protocol consisting of circular dots moving in the whole field. Some of the dots move coherently in one direction (signal) while others move randomly (noise).

Bonsai is a graphical, event-based language. Its capacity to interact with various types of external hardware in real time, makes it a promising tool in neuroscience. BonVision is a package built up top of that to present visual stimuli across different display and render configurations.

To generate many moving dots in the scene, it would be more efficient to write extension codes than to build workflow in Bonsai GUI.

This article introduces how to write such a extension code that can be used to generate moving dots[https://bonsai-rx.org/docs/tutorials/scripting.html].

Visual stimuli generated with BonVision package are optimised to one viewing point (for rendering stimuli at a specific size, orientation and location,), so the extension files and the example workflow in this workflow can be applicable to different animal species. As long as they are constrained at a location to receive visual stimuli.

In the associated article and database, this example workflow is used to present random dot kinematograms to tethered desert locust.


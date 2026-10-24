# BonVision random dot kinematogram
## Introduction
This is a repository storing a workflow to present random dot kinematogram with [BonVision](https://bonvision.github.io/) package in [Bonsai](https://bonsai-rx.org/).

A random dot kinematogram is a motion‑perception protocol consisting of circular dots moving in the whole field. Some of the dots move coherently in one direction (signal) while others move randomly (noise).

Bonsai is a graphical, event-based language. Its capacity to interact with various types of external hardware in real time, makes it a promising tool in neuroscience. BonVision is a package built up top of that to present visual stimuli across different display and render configurations.

To generate many moving dots in the scene, it would be more efficient to write extension codes than to build workflow in Bonsai GUI.

This [tutorial](https://bonsai-rx.org/docs/tutorials/scripting.html) introduces how to write such a extension code that can be used to generate moving dots.

Visual stimuli generated with BonVision package are optimised to one viewing point (for rendering stimuli at a specific size, orientation and location,), so the extension files and the example workflow in this workflow can be applicable to different animal species. As long as they are constrained at a location to receive visual stimuli.

In the associated article and database, this example workflow is used to present random dot kinematograms to tethered desert locust.

## Start to use the repository
1. The best way to use codes in this github repository is to install [Git](https://git-scm.com/) and then clone this repository to your local device.
Nevertheless, you can always click on the **<> Code** button on the top and select download as zip.
2. Then depending on whether you want to use the [stimulus code](https://github.com/chiyu1203/bonvision_rdk/tree/main/BonsaiWorkflows) or [analysis code](https://github.com/chiyu1203/bonvision_rdk/tree/main/Analysis), move to their respective folders for detailed explanation.


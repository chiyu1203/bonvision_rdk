# BonVision random dot kinematogram
## Introduction
<img width="312" height="131" alt="bonsai_bonvision" src="https://github.com/user-attachments/assets/c760b664-ac1f-4ada-bf24-b14f22d188e4" /><br />
This is a repository storing a workflow to present a random dot kinematogram with [BonVision](https://bonvision.github.io/) package in [Bonsai](https://bonsai-rx.org/).

A random dot kinematogram is a motion‑perception protocol in which circular dots move across the entire field. Some dots move coherently in one direction (signal), while others move randomly (noise).

Bonsai is a graphical, event-based language. Its capacity to interact with various types of external hardware in real time makes it a promising tool in neuroscience. BonVision is a package built on top of that to present visual stimuli across different display and rendering configurations.

To generate many moving dots in the scene, it would be more efficient to write extension code than to build a workflow in the Bonsai GUI.
This is not only efficent for the computer to execute the code but also for exposing parameters, for documentation. 
This [tutorial](https://bonsai-rx.org/docs/tutorials/scripting.html) introduces how to write such an extension code that can be used to generate moving dots.

In this repository, visual stimuli are designed based on one viewing point (for rendering stimuli at a specific size, orientation, and location), so the extension files and the example workflow in this workflow can be applied to different animal species. As long as they are constrained at a location to receive visual stimuli.

In the associated article and database, this example workflow presents random dot kinematograms to tethered desert locusts.

Click the following links to view an example video if it does not pop up automatically. The video is sped up 2.0x. <br />

https://github.com/user-attachments/assets/823a4b4c-9182-4d24-8816-ab129320d2df


You can find the article and database on Zenodo: 10.5281/zenodo.23565813 
## Start to use the repository
1. The best way to use codes in this github repository is to install [Git](https://git-scm.com/) and then clone this repository to your local device.
Nevertheless, you can always click on the **<> Code** button on the top and select download as zip.
2. Then depending on whether you want to use the [stimulus code](https://github.com/chiyu1203/bonvision_rdk/tree/main/BonsaiWorkflows) or [analysis code](https://github.com/chiyu1203/bonvision_rdk/tree/main/Analysis), move to their respective folders for detailed explanations.

## Cite this work
Use the DOI on Zenodo: 10.5281/zenodo.23565813 

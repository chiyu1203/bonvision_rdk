# How to use the rdk workflow in Bonsai?
## Installation Bonsai
1. Download the portable file (.zip) from the [webpage](https://bonsai-rx.org/docs/articles/installation.html)
<br />
<img width="1495" height="803" alt="Screenshot 2026-10-25 180056" src="https://github.com/user-attachments/assets/410bc450-7501-487e-bf38-e79d21bedeb5" /><br />

<br />


**Note**: It is possible to install Bonsai with the Installer (.exe) file.
However, the benefit of using the Portable is that you can install versions of Bonsai on the same machine (but stored in different folders).

3. Unzip the portable and move the folder to where you want to store it

4. Click Bonsai.exe to start the installation process

<img width="602" height="155" alt="Screenshot 2026-10-25 180220" src="https://github.com/user-attachments/assets/d4ca99fb-bb68-44b9-83e9-68828f98c38e" /><br />


4. After installing Bonsai in the workflow, you will see this menu. Here, you can load existing Bonsai workflow files or create a new one.
5. If this is a fresh Bonsai programme, click Manage Packages to install necessary packages first.<br />
<img width="200" height="333" alt="Screenshot 2026-10-25 180228" src="https://github.com/user-attachments/assets/043be9a8-bd85-4904-889f-9fc55d69d801" /><br />

## Installing packages in Bonsai


1. Once you click on Manage Packages, go to Page 2 to find “Start Pack” and install it.
(After those libraries are installed, you shall see a green checkmark on the right).
<img width="799" height="570" alt="Screenshot 2026-10-25 180512" src="https://github.com/user-attachments/assets/074ac562-e2c9-48f4-ab9f-f4f02c2473b9" /><br />



2. Then select the community package from the right dropdown menu, where you can find BonVision to install.


<img width="800" height="573" alt="Screenshot 2026-10-25 180552" src="https://github.com/user-attachments/assets/97e4a67d-87a8-4244-8c9f-9efd8cb7c646" /><br />



3. Once Bonvision is also installed, click "Close". This will bring you to the main menu, where you load a workflow

## Ovewview of the workflow

#### To open the rdk_workflow, either double-click the file or load the workflow via Bonsai.
(To the right of the Start button, the program shows the working directory. Make sure this directory points to your bonvision_rdk folder, as the extension files are stored here)



<img width="715" height="830" alt="Screenshot 2026-10-25 175051_edited" src="https://github.com/user-attachments/assets/99250b96-0337-4cfb-a496-523fd63116ef" /><br />


#### Once the workflow is opened, you will see those nodes connected to each other. In this workflow, they can be subdivided into 4 parts.
1. Loading packages, resources, and defining global variables. <br />
**Nodes to change**:<br />
**CreateWindow** - This node sets up a window where visual stimuli are present. Change TargetRenderFrequency and Height/Width to meet with the spec of your display <br />

<img width="488" height="543" alt="Screenshot 2026-10-25 215707" src="https://github.com/user-attachments/assets/45e40832-e549-4081-91b4-874ffa5ab90f" />

**CraeteRandom** - This node defines the random seed of the randomised sequence. Note: I'd recommend screening over a number of random seeds and picking those that result in the least autocorrelation in the random sequence. (inside VarInit)<br />
<img width="454" height="201" alt="Screenshot 2026-10-25 220707" src="https://github.com/user-attachments/assets/78eb7997-c9fe-40a2-843a-f55ad1ee55bd" />

2. Defining display environment.
**This part influences how the study subject views the display. We use [equirectangular](https://bonvision.github.io/pages/02-Display-Environment-basics/#2d-stimuli) to map the 3D sphere on the window. Because of this mapping, a 2-degree dot will look more or less similar from the observer's viewpoint, no matter where the dot is drawn on the window.<br />
<br /> The Groupworkflow, LED_sphere_mapping, was optimized to present stimuli to 4 subjects; each subject is surrounded by 4 LED screens, so there are quadruplicates of nodes in the group workflow.

**Nodes to change**:<br />
**ViewWindow** - This [node](https://bonvision.github.io/docs/ViewingWindow/#) defines the physical location of your display is relative to the observer (both translational and rotational in the 3D space) It is hard to describe what value you should put in the XYZ as it depends on the relative position between the observer and the display. In our case, we appointed the front screen to be the reference screen so setting is values along rotational axes all equal 0. In terms of Translational displacement, Z represents the distance vector from the screen to the observer, so -12.5 means the screen is in front of the subject by 12.5 cm. Y represents levels between observer's viewpoint and the centre of the screen, so 0 means the centre of the screen and the subject's viewpoint is at the same level the subject. Following this order, the left screen was rotated by 90 degree and positioned on the left side of the subject by 12.5 cm.<br />
<img width="1088" height="340" alt="Screenshot 2026-10-25 222554" src="https://github.com/user-attachments/assets/3af0a8f8-6fb2-43aa-b92d-b3d0d4be4c35" /><br />
**DrawViewport** - This [node](https://bonvision.github.io/docs/DrawViewport/#) defines the size and location of your display in your drawing window. If your drawing window was mapped onto 4 displays, then assign the following values to each one of the displays 0.25, 0.5, 0.75, 1.0. Whether these values go into X or Y axis depends on which orientation the displays are aligned (X means horizontal stack; Y means vertical stack) <br />
<img width="1106" height="336" alt="Screenshot 2026-10-25 225134" src="https://github.com/user-attachments/assets/8b7a1813-8c05-438f-942e-4d4811b66515" /><br />

3. Stimulus workflow


4. Filming workflow



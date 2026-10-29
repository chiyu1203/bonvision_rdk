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


1. Once you click on Manage Packages, go to Page 2 to find “Start Pack” and install it. (After those libraries are installed, you shall see a green checkmark on the right).<br />
<img width="799" height="570" alt="Screenshot 2026-10-25 180512" src="https://github.com/user-attachments/assets/074ac562-e2c9-48f4-ab9f-f4f02c2473b9" /><br />



2. Then select the community package from the right dropdown menu, where you can find BonVision to install.


<img width="800" height="573" alt="Screenshot 2026-10-25 180552" src="https://github.com/user-attachments/assets/97e4a67d-87a8-4244-8c9f-9efd8cb7c646" /><br />



3. Once Bonvision is also installed, click "Close". This will bring you to the main menu, where you load a workflow

## Ovewview of the workflow

#### To open the rdk_workflow, either double-click the file or load the workflow via Bonsai.
(To the right of the Start button, the program shows the working directory. Make sure this directory points to your bonvision_rdk folder, as the extension files are stored here)



<img width="715" height="830" alt="Screenshot 2026-10-25 175051_edited" src="https://github.com/user-attachments/assets/99250b96-0337-4cfb-a496-523fd63116ef" /><br />


#### Once the workflow is opened, you will see those nodes connected to each other. In this workflow, they can be subdivided into 4 parts.
1. **Loading packages, resources, and defining global variables** <br />
These nodes aim to load packages, dependencies, and save incoming data as .CSV files.<br />
**Nodes to change**:<br />
*CreateWindow* - This node sets up a window where visual stimuli are present. Change TargetRenderFrequency and Height/Width to meet with the spec of your display <br />

<img width="488" height="543" alt="Screenshot 2026-10-25 215707" src="https://github.com/user-attachments/assets/45e40832-e549-4081-91b4-874ffa5ab90f" />

*CraeteRandom* - This node defines the random seed of the randomised sequence. Note: I'd recommend screening over a number of random seeds and picking those that result in the least autocorrelation in the random sequence. (inside VarInit)<br />
<img width="454" height="201" alt="Screenshot 2026-10-25 220707" src="https://github.com/user-attachments/assets/78eb7997-c9fe-40a2-843a-f55ad1ee55bd" />

2. **Defining display environment**
These nodes affect how the study subject views the display. We use [equirectangular](https://bonvision.github.io/pages/02-Display-Environment-basics/#2d-stimuli) to map the 3D sphere on the window (2D display). Because of this mapping, a 2-degree dot will look more or less similar from the observer's viewpoint, no matter where the dot is drawn on the window. Note: when presenting full-field visual stimuli with an equirectangular projection, the distortion at higher elevations prevents the rendered environment from covering the entire display. You keep the rendered window like this, or enlarge your rendering window to fit the display. Both methods has its caveats and benefits. For those who cares about distortation, equirectangular projection is not your choices when presenting stimuli at high elevation. <br />
<br /> The Groupworkflow, LED_sphere_mapping, was optimized to present stimuli to 4 subjects; each subject is surrounded by 4 LED screens, so there are quadruplicates of nodes in the group workflow.

**Nodes to change**:<br />
*ViewWindow* - This [node](https://bonvision.github.io/docs/ViewingWindow/#) defines the physical location of your display is relative to the observer (both translational and rotational in the 3D space) It is hard to describe what value you should put in the XYZ as it depends on the relative position between the observer and the display. In our case, we appointed the front screen to be the reference screen so setting is values along rotational axes all equal 0. In terms of Translational displacement, Z represents the distance vector from the screen to the observer, so -12.5 means the screen is in front of the subject by 12.5 cm. Y represents levels between observer's viewpoint and the centre of the screen, so 0 means the centre of the screen and the subject's viewpoint is at the same level the subject. Following this order, the left screen was rotated by 90 degree and positioned on the left side of the subject by 12.5 cm.<br />
<img width="828" height="347" alt="Screenshot 2026-10-28 233618" src="https://github.com/user-attachments/assets/30ed6e7d-e60a-43f9-b308-d00bad187e11" /><br />
*DrawViewport* - This [node](https://bonvision.github.io/docs/DrawViewport/#) defines the size and location of your display in your drawing window. If your drawing window was mapped onto 4 displays, then assign the following values to each one of the displays 0.25, 0.5, 0.75, 1.0. Whether these values go into X or Y axis depends on which orientation the displays are aligned (X means horizontal stack; Y means vertical stack). In this workflow, we stack LED panels horizontally, starting from the left screen. However, there is no fixed rule about this. As long as the rotational direction follow a sequence. <br />
<img width="1106" height="336" alt="Screenshot 2026-10-25 225134" src="https://github.com/user-attachments/assets/8b7a1813-8c05-438f-942e-4d4811b66515" /><br />

3. **Stimulus workflow**<br />
Inside this group workflow, these nodes generate stimuli of interest. In this workflow (the figure below), we used customized scripts to generate many dots. The metadata about those dots is stored in a CSV file in the main workflow. A typical way to generate a stimulus sequence on Bonsai is to first define the length of a stimulus and its interval. Then use *TakeUntil* node connected by a *Timer* to control when to stop presenting stimuli. Once the stimulus disappears, use *Delay* to prolong time of presenting the empty screen. More details can be found [here](https://bonvision.github.io/pages/03-Creating-Basic-Stimuli/#troubleshooting). However, in RDK, the control condition is not an empty screen but moving dots at 0%. Therefore, we designed two streams, one presenting interstimulus intervals and the other presenting stimulus presentation, and then we use the node *Concat* to present them in [sequence](https://bonvision.github.io/pages/04-Series-of-stimuli/).<br />
<img width="1167" height="402" alt="Screenshot 2026-10-29 121911" src="https://github.com/user-attachments/assets/bc25086c-12ff-4c00-9cb0-82ec55f270e4" /><br />
**Nodes to change**:<br />
*Timer*: Duration for the grey screen before presenting any stimuli (no matter it is stimulus or inter-stimulus interval).<br />
*RepeatCount*: how many repetitions do you want to have in this sequence?<br />
Note: I have exposed these two parameters in the main workflow so you can also find them there.
*MotionCoherenceSpecification*: this node is inside the note *4coherence_2directions* and *interval_2length*<br />
<img width="860" height="158" alt="Screenshot 2026-10-29 123544" src="https://github.com/user-attachments/assets/08fc173f-9520-44eb-a8b4-657edfd1b70c" /><br />
Click the three dots on the side to open this editor window. Here you can specify parameters in the RDK. Note: at most, you can generate two motion flow simultaneously. The first one has a suffix 1 in all of its properties. The second one has a suffix 2.<br />
<img width="470" height="457" alt="Screenshot 2026-10-29 123811" src="https://github.com/user-attachments/assets/abbcf31f-778b-4024-82f7-4417e2fee071" /><br />

4. **Filming workflow**<br />
Inside this group workflow, these notes set up the filming environment. A key factor in filming is to position cameras well. Ideally, place the camera where it can film the animal (in this repository, the ball for estimating the animal's trajectory with [Fictrac](https://github.com/rjdmoore/fictrac)) and the event of interest (in this repository, the onset and offset of visual stimuli).<br />
Depending on how accurate you seek in the behavioural metrics (when studying fast movement or associating behaviour with neural data), you can film the animals with a cheap webcam or an industrial-level camera. To align the timing of a behavior with an event of interest, you need to identify when they happen in the video. This can be achieved by designing a synchronisation patch, which changes its pixel value exactly when the stimulus is on (or off) on the screen where the animal can not see it clearly. Then you can film the patch with a camera (as done in this repository). The benefit of filming synchronizing patches directly is that it is easier to set up, and the onset/offset timing you obtain from filming the synchronizing patch will match the stimulus onset/offset (ignoring the LED array update rate). The downside is that the signal-to-noise ratio of a synchronizing patch can be low (because many experiments using visual stimuli will install a visible light filter to prevent light from displays from affecting camera tracking). Also, it is not always possible to film the display. Alternatively, place a light sensor in front of the synchronizing patch. Then program a microcontroller so that it can turn on or off an LED pulse when the light sensor detects that the synchronizing patch has changed its color. In this case, you can place the LED pulse where your camera can capture it, like what is demonstrated in this [tutorial](https://neurogears.org/swc-2020/worksheets/synching/) (example 2).<br />
There are four camera filming threads in the **Filming workflow** because of quadruplicates of units in our acquisition. Below shows one of the filming threads.<br />
<img width="1260" height="243" alt="Screenshot 2026-10-29 142842" src="https://github.com/user-attachments/assets/9b93b564-1d37-4259-a315-604185449e87" /><br />

**Nodes to change**:<br />
*Crop*: Click on the three dots on the right side of the Region of Interest (in the Properties panel) to open a window where you can select a region of interest (rectangle shape). Then Bonsai will sum the RGB values of the pixels in the selected region. This will be the event thread readout.<br />
**Nodes probably need an adjustment**<br />

You may have your own camera, so instead of using the *CameraCapture* node, you might be using *PylonCapture* or another node.<br />

*VideoWriter*: In the case where the video format is different from this default setting, you need to go to the StartFilming group workflow to change its settings.
This group workflow saves incoming acquisition frames as video files and their metadata (including the event thread readout).<br />

<img width="646" height="331" alt="Screenshot 2026-10-29 143837" src="https://github.com/user-attachments/assets/a9405622-f2a3-46d9-93b9-e25b05aa9d76" />

That is pretty much everything. Because the user base is smaller, there isn't much information online about coding in Bonsai, which also means existing chatbots cannot code it well. Coding in Bonsai can be frustrating (its reactive programming model differs from other languages). The GitHub page has an active [discussion forum](https://github.com/orgs/bonsai-rx/discussions)  where you can ask questions or look for templates. Once you get past the learning curve, this program will also help you think about how signal processing works in the brain.

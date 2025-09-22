# Py-YANC
*Yet Another Network Controller - In Python*

### Overview
This is the first version of the code that will evolve over the time.

The main idea is to create a network controller that will handle device configuration, device update, workflows and maybe an automatic config generator.
Also, in the future, AI usage is considered.

At this first version, the code receives an yaml file as provided in .examples/config_example.conf. This example contains all possible configurations. Create your own yaml file using this as a guide.

After creating your file(s), upload them to folder "to_deploy/". The code supports multi device configuration, but single job, which means it is done one after another. Each device must have their own file.

<sub>Future implementations may consider multithread/asyncio/multiprocess support, but we are far from that yet.</sub>

For each yaml file, the system:
- Generates config file.
- Restore factory default configuration if flagged.
- Test if device is reachable.
- Disable logging and unwanted message that could break the code and also configures the hostname to facilitate next step.
- Send the configuration file generated to device.
- Finishes script


### To consider
This is the minimum requirement for the controller to grow since handles the two most basic concepts, configuration and connection.

I am aware that I overcoded some parts or did it not in an optmum way, but it was used to study and understand the concepts. The entire code will be changed in the future for improvements.

At this moment, it supports only Cisco ios devices with a few basic configurations only. Please, check .examples/config_example.conf for more details.

### In the pipeline for first version
<sub>in no particular order</sub>
- [ ] Organize code and folders
- [ ] Create workflows for different steps/requests such as "remove configuration", "deploy", "redeploy", "reconfigure"
- [ ] Support command line args
- [ ] Retrieve information from device (show commands)


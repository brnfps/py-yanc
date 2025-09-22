# Py-YANC
*Yet Another Network Controller - In Python*

### Overview
This is the first version of the code that will evolve over the time.

The main idea is to create a network controller that will handle device configuration, device update, workflows and maybe an automatic config generator.
Also, in the future, AI usage is considered.

At this first version, the code receives an yaml file as provided in .examples/config_example.conf. This example contains all possible configurations. Create your own yaml file using this as a guide.

After creating your file(s), upload them to folder "to_deploy/". The code supports multi device configuration, but single job, which means it is done one after another. Each device must have their own file.

<sub>Future implementations may consider multithread/asyncio/multiprocess support, but we are far from that yet.</sub>


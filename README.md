salt-osx-grains
===============

Additional OS X specific grains for saltstack.
* model
* serial

Writing grains is briefly covered in SaltStack's docs:
http://docs.saltstack.com/topics/targeting/grains.html#writing-grains

model
-----

Model number, as returned by:
```bash
sysctl hw.model
```

serial
------

Serial Number, as returned by:
```bash
ioreg -l | grep IOPlatformSerialNumber
```

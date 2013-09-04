# salt-osx-grains

Additional OS X specific grains for saltstack.
* [asset](#asset)
  * [Create Asset Variable](#create-asset-variable)
* [model](#model)
* [serial](#serial)

Writing grains is briefly covered in [SaltStack's docs](http://docs.saltstack.com/topics/targeting/grains.html#writing-grains).

## asset

Asset information, as returned by:
```bash
nvram asset
```

Storing company asset tag numbers/codes in a non-volatile place can be useful. Ideally, you should store the information in nvram so that it persists when the computer is formatted and reinstalled.

### Create Asset Variable

Store your asset information using the nvram command:
```bash
nvram asset=01234ABCD56789
```

If you store your asset information as _asset_, as shown, then you're good to go!

Otherwise, you'll need to change the [asset_name variable](/VertigoRay/salt-osx-grains/blob/master/salt_osx_grains.py#L5) to match your the name that you chose.  For example, if you work for [Contoso](http://en.wikipedia.org/wiki/Contoso), you may want to store the asset information as _contoso-asset_.  In this case, you would run the following command:

```bash
nvram contoso-asset=01234ABCD56789
```

Then change the [asset_name variable](/VertigoRay/salt-osx-grains/blob/master/salt_osx_grains.py#L5) to:

```python
asset_name = 'contoso-asset'
```

## model

Model number, as returned by:
```bash
sysctl hw.model
```

## serial

Serial Number, as returned by:
```bash
ioreg -l | grep IOPlatformSerialNumber
```

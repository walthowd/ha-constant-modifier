# ha-constant-modifier
This is a custom component for Home Assistant that can be used to modify, patch or overwrite constants in other components. 

## Installation
To install, place the constant_modifier in your Home Assistant configuration directory under the custom_components folder

## Configuration
Add to `configuration.yaml` any constants you need to modify. For example

```
constant_modifier:
  homeassistant.components.websocket_api.http.MAX_PENDING_MSG: 4096
  homeassistant.components.websocket_api.http.PENDING_MSG_PEAK: 2048
```


## Note
This component was created to battle the issue of "Client exceeded max pending messages" when the websocket queue fills in Home Assistant. This seems to be an uncommon issue when using Node-RED and node-red-contrib-home-assistant-websocket in large installations.


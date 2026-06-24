# Kodi HDMI CEC Power Controls

A simple Kodi script addon that lets you trigger HDMI CEC power commands via Kodi's JSON-RPC API.

## What this addon does

It exposes script actions that map to Kodi built-ins:

- `on` -> `CECActivateSource` (wake / switch TV input)
- `off` -> `CECStandby` (put TV/CEC chain in standby)

## Install

1. Zip this folder contents (not the parent folder) so `addon.xml` is at the zip root.
2. In Kodi: **Add-ons -> Install from zip file**.
3. Enable CEC in Kodi settings and ensure your TV/device supports HDMI CEC.

## JSON-RPC examples

Kodi JSON-RPC endpoint is usually:

- `http://<kodi-host>:8080/jsonrpc`

### Turn TV on

```bash
curl -X POST http://<kodi-host>:8080/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "Addons.ExecuteAddon",
    "params": {
      "addonid": "script.hdmi.cec.power",
      "params": ["on"]
    }
  }'
```

### Turn TV off

```bash
curl -X POST http://<kodi-host>:8080/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "Addons.ExecuteAddon",
    "params": {
      "addonid": "script.hdmi.cec.power",
      "params": ["off"]
    }
  }'
```

## Optional argument formats

The addon accepts these equivalent action formats:

- `"on"`
- `"action=on"`
- `"--action=on"`

## Notes

- CEC behavior is device-dependent. Some TVs ignore wake/standby under certain settings.
- `CECStandby` may impact other devices on the CEC chain depending on your setup.

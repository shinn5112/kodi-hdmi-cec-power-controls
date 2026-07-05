# Kodi HDMI CEC Power Controls

A simple Kodi script addon that lets you trigger HDMI CEC power commands via Kodi's JSON-RPC API.

## What this addon does

It exposes script actions that map to Kodi built-ins:

- `on` -> `CECActivateSource` (wake / switch TV input)
- `off` -> `CECStandby` (put TV/CEC chain in standby)

## Install

1. Build the package from this repository root:

  ```bash
  ./package.sh
  ```

  This creates `dist/script.hdmi.cec.power-<version>.zip`.
2. In Kodi: **Add-ons -> Install from zip file**.
3. Ensure HDMI CEC is enabled on your TV and in Kodi.

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

## CEC settings checklist (important)

If `on` works but `off` does not, check Kodi CEC adapter settings first:

1. Kodi path: **Settings -> System -> Input -> Peripherals -> CEC Adapter**
2. Set **Device type** to **Playback device**
3. Set **Devices to power off during shutdown** to include **TV** and **AVR**
4. Verify TV-side CEC vendor setting is enabled (Anynet+, Simplink, Bravia Sync, etc.)

In testing, setting the CEC adapter **Device type** to **Playback device** was required for reliable standby/power-off behavior.

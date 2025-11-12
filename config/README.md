# PhiLaunch Configuration

## Setup

1. Copy the example config:
   ```bash
   cp philaunch.conf.example philaunch.conf
   ```

2. Edit `philaunch.conf` with your settings:
   ```bash
   nano philaunch.conf
   ```

3. Source in your scripts:
   ```bash
   source "${HOME}/config/philaunch.conf"
   ```

## Security

**NEVER commit `philaunch.conf` to git!** It contains your personal configuration.

Only commit `philaunch.conf.example` as a template.

The `.gitignore` file is configured to exclude `philaunch.conf` automatically.

## Variables

All configuration variables are prefixed with `PHILAUNCH_` to avoid conflicts.

See `philaunch.conf.example` for all available options and descriptions.

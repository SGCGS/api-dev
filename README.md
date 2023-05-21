# Back-End API Server Repository of SGCGS Project

## Guide
**Submit a PR instead of a commit directly.**

### Install Dependencies
`pip3 install requests fastapi`

### [WEB API Documentation](https://github.com/SGCGS/api-dev/blob/main/WEB-API.md)
### [Pythonic Public and Utilities API Documentation](https://github.com/SGCGS/api-dev/blob/main/DEV.md)

### Required Configurations
#### `reCaptcha.json`
```json
{
    "site_key": ***reCaptcha v3 site key***,
    "secret": ***reCaptcha v3 secret***,
    "threshold": ***trust threshold***
}
```
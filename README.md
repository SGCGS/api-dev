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

### Deployment
Nginx Proxy Configuration (`location /`)
```
if ($request_method = 'OPTIONS') {
    add_header 'Access-Control-Max-Age' 1728000;
    add_header 'Content-Type' 'text/plain; charset=utf-8';
    add_header 'Content-Length' 0;
    add_header 'Access-Control-Allow-Origin' 'https://sgcgs.com';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
    add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
    add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
    return 204;
}
```
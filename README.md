# SGCGS
## Tips
您知道吗？按下 Ctrl + Shift + V 可以在视觉工作室代码中实时预览 Markdown 文件。


## 开发指南
**请提交PR而不是直接提交到主分支。**

### API Server 安装依赖
`pip3 install requests fastapi`

### 文件管理
前端代码放在 `/web` 文件夹下。  
后端代码根据情况组织在根目录下。

### 前端
链接请使用 Vue 路由  
主题色：  
黑：#000000  
红：#FF0000  
天蓝：#E6F0FD  
背景淡灰：#F6F6F6  
灰：#8590A6
蓝：#0461CF  
知乎  
Vue.js 3 + Element UI Plus  
请在页面加入 Cookie 存在验证，若 Cookie 失效直接登出

### 后端
Nginx + FastAPI + SQLite3  


## 安全
### HSTS
透过 http 访问时重定向，开启HSTS，HSTS缓存有效期一年。

### ReCaptcha
在注册与登陆页面引入验证。

## [API 接口文档](https://github.com/SGCGS/SGCGS.com/blob/main/API.md)
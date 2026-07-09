# 云云助手 MCP 桥 — 一键部署到云端
# 将这个目录部署到 Render / Railway / Fly.io 即可获得公网API
# 手机APP通过这个API跟我通信，不需要同一个WiFi

# 使用 Render 部署(免费):
# 1. 注册 https://render.com (GitHub登录)
# 2. Dashboard → New Web Service
# 3. 连接这个Git仓库，或直接用:
#    Public Git Repository: 将本目录push到GitHub
# 4. Start Command: python mcp_bridge.py
# 5. Deploy → 获得 https://xxx.onrender.com

# 使用 Railway 部署(免费，无需信用卡):
# 1. 注册 https://railway.app (GitHub登录)
# 2. New Project → Deploy from GitHub
# 3. 或: 下载railway CLI → railway up
# 4. 自动获得 https://xxx.up.railway.app

# 部署后，更新App中的SERVER_URL指向你的云地址

"""
云云助手 MCP 桥 — 让手机APP通过公网API跟我通信
启动后任何人可以访问 https://yunyun-bridge.onrender.com/ask?q=xxx
或者自己部署到 Render / Railway / Fly.io
"""
import http.server, json, urllib.parse, os, time
from datetime import datetime

PORT = int(os.environ.get('PORT', 10000))
QUERIES = []
RESPONSES = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(p.query)
        
        if p.path == '/':
            self.send(200, {"ok":True, "name":"云云助手桥", "time":datetime.now().isoformat()})
        elif p.path == '/ask':
            q = qs.get('q', [''])[0]
            if q:
                qid = str(int(time.time()*1000))
                QUERIES.append({"id":qid, "q":q, "ts":datetime.now().isoformat()})
                self.send(200, {"status":"ok", "id":qid, "msg":"已收到, 等待回复"})
            else:
                self.send(400, {"status":"error", "msg":"需要 q 参数"})
        elif p.path == '/check':
            qid = qs.get('id', [''])[0]
            if qid and qid in RESPONSES:
                self.send(200, {"status":"answered", "resp":RESPONSES.pop(qid)})
            else:
                self.send(200, {"status":"waiting"})
        elif p.path == '/pending':
            self.send(200, {"count":len(QUERIES), "queries":[{"id":q["id"],"q":q["q"],"ts":q["ts"]} for q in QUERIES[-10:]]})
        elif p.path == '/reply':
            qid = qs.get('id', [''])[0]
            resp = qs.get('r', [''])[0]
            if qid and resp:
                RESPONSES[qid] = resp
                # Remove from pending
                for i, q in enumerate(QUERIES):
                    if q['id'] == qid:
                        QUERIES.pop(i)
                        break
                self.send(200, {"status":"replied"})
            else:
                self.send(400, {"status":"error", "msg":"需要 id 和 r 参数"})
        else:
            self.send(404, {"error":"not found"})
    
    def do_POST(self):
        cl = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(cl).decode('utf-8')
        data = json.loads(body) if body else {}
        
        if self.path == '/ask':
            q = data.get('q', '')
            if q:
                qid = str(int(time.time()*1000))
                QUERIES.append({"id":qid, "q":q, "ts":datetime.now().isoformat()})
                self.send(200, {"status":"ok", "id":qid})
            else:
                self.send(400, {"status":"error"})
        elif self.path == '/reply':
            qid = data.get('id', '')
            resp = data.get('r', '')
            if qid and resp:
                RESPONSES[qid] = resp
                self.send(200, {"status":"ok"})
            else:
                self.send(400, {"status":"error"})
        else:
            self.send(404, {"error":"not found"})
    
    def send(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Headers','*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def do_OPTIONS(self):
        self.send(200, {})
    
    def log_message(self, fmt, *args):
        pass

print(f"\n🌸 云云 MCP 桥 · 端口 {PORT}")
print(f"{'='*40}")
print(f"  GET  /ask?q=问题    → 提交问题")
print(f"  GET  /check?id=xxx   → 查回复")
print(f"  GET  /pending        → 查看待回复")
print(f"  POST /reply          → 回复问题(我)")
print(f"{'='*40}")

http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()

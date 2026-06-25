# pages/login.py
# محتوای LOGIN_HTML از pages.py قبلی — اینجا import می‌شه
# برای جلوگیری از حجم زیاد، از pages.py قدیمی کپی کن:
#   HTML = LOGIN_HTML  (از pages.py قبلی)

# نمونه ساده برای تست:
HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="UTF-8"><title>ورود · RVG</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Vazirmatn',sans-serif;background:#060f1d;color:#E8F4FF;min-height:100vh;display:flex;align-items:center;justify-content:center}
.card{background:#0d1b2e;border:1px solid rgba(59,130,246,0.2);border-radius:18px;padding:36px 32px;max-width:380px;width:100%}
h1{font-size:20px;margin-bottom:6px}
p{font-size:12px;color:#3D6B8E;margin-bottom:20px}
input{width:100%;padding:12px;border-radius:8px;border:1px solid rgba(59,130,246,0.2);background:rgba(0,0,0,.3);color:#E8F4FF;font-family:inherit;font-size:14px;outline:none;margin-bottom:14px}
button{width:100%;padding:12px;border-radius:8px;border:none;background:#3B82F6;color:#fff;font-family:inherit;font-size:14px;font-weight:600;cursor:pointer}
.err{color:#F87171;font-size:12px;margin-bottom:10px;display:none}
</style></head>
<body>
<div class="card">
  <h1>ورود به پنل</h1>
  <p>RVG Gateway v10.0</p>
  <div class="err" id="err"></div>
  <input type="password" id="pw" placeholder="رمز عبور" autofocus>
  <button onclick="login()">ورود</button>
</div>
<script>
async function login(){
  const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({password:document.getElementById('pw').value})});
  if(r.ok)location.href='/dashboard';
  else{const d=await r.json();document.getElementById('err').textContent=d.detail;document.getElementById('err').style.display='';}
}
document.getElementById('pw').addEventListener('keydown',e=>e.key==='Enter'&&login());
</script>
</body></html>"""

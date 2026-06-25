# pages/login.py

HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · RVG Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#03080f;
  --surface:rgba(8,18,32,0.85);
  --accent:#3B82F6;
  --accent-glow:rgba(59,130,246,0.35);
  --accent-soft:rgba(59,130,246,0.12);
  --text:#E8F4FF;
  --text-dim:#4a7fa8;
  --text-mid:#7BAED4;
  --border:rgba(59,130,246,0.18);
  --border-focus:rgba(59,130,246,0.55);
  --err:#EF4444;
  --err-bg:rgba(239,68,68,0.08);
  --err-border:rgba(239,68,68,0.2);
}
html,body{height:100%;overflow:hidden}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg);
  display:flex;align-items:center;justify-content:center;
  padding:20px;
}

/* ── background layers ── */
.bg-base{position:fixed;inset:0;z-index:0;background:var(--bg)}
.bg-radial{
  position:fixed;inset:0;z-index:1;
  background:
    radial-gradient(ellipse 70% 55% at 50% -5%,rgba(59,130,246,0.13) 0%,transparent 70%),
    radial-gradient(ellipse 40% 40% at 85% 80%,rgba(16,185,129,0.05) 0%,transparent 60%);
}
.bg-grid{
  position:fixed;inset:0;z-index:1;
  background-image:
    linear-gradient(rgba(59,130,246,0.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(59,130,246,0.035) 1px,transparent 1px);
  background-size:52px 52px;
  mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black,transparent);
}
.orb{position:fixed;border-radius:50%;filter:blur(100px);z-index:1;pointer-events:none}
.orb-1{width:500px;height:500px;background:rgba(59,130,246,0.06);top:-150px;right:-150px;animation:drift 12s ease-in-out infinite}
.orb-2{width:350px;height:350px;background:rgba(16,185,129,0.04);bottom:-80px;left:-80px;animation:drift 16s ease-in-out infinite reverse}
@keyframes drift{0%,100%{transform:translate(0,0)}33%{transform:translate(-20px,15px)}66%{transform:translate(15px,-10px)}}

/* ── card ── */
.wrap{position:relative;z-index:10;width:100%;max-width:390px}

.card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:22px;
  padding:36px 32px 32px;
  backdrop-filter:blur(32px) saturate(160%);
  -webkit-backdrop-filter:blur(32px) saturate(160%);
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.03) inset,
    0 2px 80px rgba(0,0,0,0.6),
    0 0 60px var(--accent-glow);
  animation:slideUp .5s cubic-bezier(.16,1,.3,1) both;
}
@keyframes slideUp{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}

/* ── brand ── */
.brand{display:flex;align-items:center;gap:13px;margin-bottom:30px}
.brand-icon{
  width:46px;height:46px;border-radius:13px;
  background:linear-gradient(135deg,rgba(59,130,246,0.25),rgba(59,130,246,0.08));
  border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  color:var(--accent);font-size:22px;
  box-shadow:0 0 20px var(--accent-glow);
  flex-shrink:0;
}
.brand-img{width:46px;height:46px;border-radius:13px;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px var(--accent-glow);flex-shrink:0}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:15px;font-weight:700;color:var(--text);letter-spacing:-.01em}
.brand-ver{font-size:10.5px;color:var(--text-dim);margin-top:2px;display:flex;align-items:center;gap:5px}
.ver-dot{width:5px;height:5px;border-radius:50%;background:var(--accent);display:inline-block;box-shadow:0 0 6px var(--accent)}

/* ── heading ── */
.heading{margin-bottom:24px}
h1{font-size:22px;font-weight:800;color:var(--text);letter-spacing:-.03em;line-height:1.15;margin-bottom:6px}
.sub{font-size:12.5px;color:var(--text-dim);line-height:1.6}

/* ── hint ── */
.hint{
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(59,130,246,0.07);
  border:1px solid rgba(59,130,246,0.13);
  border-radius:11px;padding:10px 14px;
  margin-bottom:20px;
}
.hint-label{font-size:11px;color:var(--text-dim)}
.hint-val{
  font-family:ui-monospace,monospace;font-size:13px;font-weight:700;
  color:var(--accent);
  background:rgba(59,130,246,0.12);
  border:1px solid rgba(59,130,246,0.22);
  padding:3px 12px;border-radius:7px;
  cursor:pointer;transition:all .15s;letter-spacing:.08em;
}
.hint-val:hover{background:rgba(59,130,246,0.22);transform:translateY(-1px)}

/* ── field ── */
.field{margin-bottom:20px}
.field label{
  display:block;font-size:10.5px;font-weight:700;
  color:var(--text-dim);margin-bottom:8px;
  text-transform:uppercase;letter-spacing:.07em;
}
.inp-wrap{position:relative}
input[type=password]{
  width:100%;
  padding:13px 16px 13px 48px;
  border-radius:12px;
  border:1px solid var(--border);
  background:rgba(0,0,0,.25);
  color:var(--text);
  font-family:inherit;font-size:14px;
  outline:none;transition:all .2s;
}
input[type=password]::placeholder{color:var(--text-dim)}
input[type=password]:focus{
  border-color:var(--border-focus);
  background:rgba(0,0,0,.35);
  box-shadow:0 0 0 3px rgba(59,130,246,.1),0 0 20px rgba(59,130,246,.06);
}
.ic{
  position:absolute;left:14px;top:50%;transform:translateY(-50%);
  color:var(--text-dim);font-size:19px;pointer-events:none;transition:.2s;
}
input:focus ~ .ic{color:var(--accent)}

/* ── error ── */
.err{
  display:none;
  background:var(--err-bg);border:1px solid var(--err-border);
  border-radius:11px;padding:10px 14px;margin-bottom:16px;
  font-size:12px;color:#F87171;
  align-items:center;gap:8px;
}
.err.show{display:flex;animation:shake .4s ease}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-5px)}40%{transform:translateX(5px)}60%{transform:translateX(-4px)}80%{transform:translateX(3px)}}

/* ── button ── */
.btn{
  width:100%;padding:13.5px;border-radius:12px;border:none;
  cursor:pointer;
  background:linear-gradient(145deg,#2563EB 0%,#1D4ED8 100%);
  color:#fff;font-family:inherit;font-size:14px;font-weight:600;
  display:flex;align-items:center;justify-content:center;gap:8px;
  box-shadow:0 4px 24px rgba(37,99,235,.45),0 1px 0 rgba(255,255,255,.08) inset;
  transition:all .2s;position:relative;overflow:hidden;
}
.btn::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,.1) 0%,transparent 60%);
  opacity:1;
}
.btn:hover{box-shadow:0 6px 30px rgba(37,99,235,.6);transform:translateY(-1px)}
.btn:active{transform:translateY(0);box-shadow:0 2px 12px rgba(37,99,235,.4)}
.btn:disabled{opacity:.45;cursor:not-allowed;transform:none}

/* ── footer ── */
.footer{
  margin-top:22px;padding-top:18px;
  border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;gap:8px;
  font-size:11px;color:var(--text-dim);
}
.footer a{
  color:var(--accent);font-weight:600;text-decoration:none;
  display:flex;align-items:center;gap:4px;
  transition:.15s;
}
.footer a:hover{color:#60A5FA}

@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg-base"></div>
<div class="bg-radial"></div>
<div class="bg-grid"></div>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="codebox"></div>
      <div>
        <div class="brand-name">codebox</div>
        <div class="brand-ver"><span class="ver-dot"></span>RVG Gateway · v10.0</div>
      </div>
    </div>

    <div class="heading">
      <h1>ورود به پنل</h1>
      <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    </div>

    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>

    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span>
    </div>

    <div class="field">
      <label>رمز عبور</label>
      <div class="inp-wrap">
        <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
        <i class="ti ti-lock ic"></i>
      </div>
    </div>

    <button class="btn" id="btn" onclick="doLogin()">
      <i class="ti ti-login-2"></i> ورود به داشبورد
    </button>

    <div class="footer">
      کانال رسمی
      <a href="https://t.me/CodeBoxo" target="_blank"><i class="ti ti-brand-telegram"></i>@CodeBoxo</a>
    </div>
  </div>
</div>

<script>
const pw = document.getElementById('pw');
const btn = document.getElementById('btn');
const err = document.getElementById('err');
const et = document.getElementById('err-text');

pw.addEventListener('keydown', e => { if(e.key==='Enter') doLogin(); });

async function doLogin(){
  err.classList.remove('show');
  btn.disabled = true;
  btn.innerHTML = '<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r = await fetch('/api/login',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({password:pw.value})
    });
    if(!r.ok){ const d=await r.json().catch(()=>({})); throw new Error(d.detail||'رمز اشتباه است'); }
    btn.innerHTML = '<i class="ti ti-check"></i> موفق!';
    setTimeout(()=>location.href='/dashboard', 300);
  }catch(e){
    et.textContent = e.message;
    err.classList.add('show');
    btn.disabled = false;
    btn.innerHTML = '<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
}
</script>
</body></html>"""

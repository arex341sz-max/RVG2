# pages.py  –  RVG Gateway v9.0
# شامل: LOGIN_HTML, DASHBOARD_HTML, get_public_page_html()

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · RVG Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#060f1d;--card:rgba(10,22,40,0.9);--accent:#3B82F6;--text:#E8F4FF;--dim:#3D6B8E;--mid:#7BAED4;--border:rgba(59,130,246,0.2)}
html,body{height:100%;overflow:hidden}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(59,130,246,0.1),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(59,130,246,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.04) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(90px);z-index:0;animation:fl 9s ease-in-out infinite}
.o1{width:380px;height:380px;background:rgba(59,130,246,0.07);top:-100px;right:-80px}
.o2{width:280px;height:280px;background:rgba(16,185,129,0.04);bottom:-60px;left:-60px;animation-delay:4s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:38px 34px 34px;backdrop-filter:blur(24px);box-shadow:0 0 80px rgba(59,130,246,0.07),0 20px 60px rgba(0,0,0,.5)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.brand-img{width:48px;height:48px;border-radius:13px;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px rgba(59,130,246,0.3);flex-shrink:0}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:16px;font-weight:700;color:var(--text)}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px}
h1{font-size:21px;font-weight:700;color:var(--text);margin-bottom:5px;letter-spacing:-.02em}
.sub{font-size:12px;color:var(--mid);margin-bottom:24px;line-height:1.6}
.hint{display:flex;align-items:center;gap:10px;background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.15);border-radius:10px;padding:10px 14px;margin-bottom:20px}
.hint-label{font-size:11px;color:var(--dim);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;color:var(--accent);background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.25);padding:3px 11px;border-radius:7px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(59,130,246,0.22)}
.field{margin-bottom:18px}
.field label{display:block;font-size:10.5px;font-weight:600;color:var(--mid);margin-bottom:7px;text-transform:uppercase;letter-spacing:.06em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:13px 44px 13px 16px;border-radius:11px;border:1px solid var(--border);background:rgba(0,0,0,.3);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:.2s}
input[type=password]:focus{border-color:rgba(59,130,246,.55);background:rgba(0,0,0,.4);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.2s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#F87171;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:13px;border-radius:11px;border:none;cursor:pointer;background:linear-gradient(135deg,#2563EB,#1D4ED8);color:#fff;font-family:inherit;font-size:14px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(37,99,235,.4);transition:.2s;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.08);opacity:0;transition:.2s}
.btn:hover::before{opacity:1}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--dim)}
.footer a{color:var(--accent);font-weight:600;text-decoration:none;display:flex;align-items:center;gap:4px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="codebox"></div>
      <div><div class="brand-name">codebox</div><div class="brand-sub">RVG Gateway · v9.0</div></div>
    </div>
    <h1>ورود به پنل</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">کانال رسمی<a href="https://t.me/CodeBoxo" target="_blank"><i class="ti ti-brand-telegram"></i>@CodeBoxo</a></div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RVG Gateway · codebox</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#060f1d;--bg2:#0a1628;--bg3:#0e1e35;
  --card:#0d1b2e;--card-b:rgba(59,130,246,0.13);--card-bh:rgba(59,130,246,0.28);
  --accent:#3B82F6;--accent2:#60A5FA;--accent-d:rgba(59,130,246,0.12);
  --green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;
  --purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.1);
  --t1:#E8F4FF;--t2:#7BAED4;--t3:#3D6B8E;
  --sidebar-w:248px;--radius:14px;
  --shadow:0 4px 24px rgba(0,0,0,0.35);
}
[data-theme="light"]{
  --bg:#F0F4FA;--bg2:#E4EDF9;--bg3:#D5E3F5;
  --card:#FFFFFF;--card-b:rgba(59,130,246,0.15);--card-bh:rgba(59,130,246,0.35);
  --accent:#2563EB;--accent2:#1D4ED8;--accent-d:rgba(37,99,235,0.08);
  --green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065F46;
  --red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991B1B;
  --amber:#D97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400E;
  --purple:#7C3AED;--purple-bg:rgba(124,58,237,0.08);
  --t1:#0F172A;--t2:#334155;--t3:#64748B;
  --shadow:0 4px 20px rgba(0,0,0,0.1);
}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1),background .3s,border-color .3s}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:10px;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px var(--accent-d);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:13.5px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px}
.sb-close{display:none;position:absolute;left:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 14px 4px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 6px;border-top-left-radius:0px;border-bottom-left-radius:0px;border-top-right-radius:0px;border-bottom-right-radius:0px; }
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-badge{margin-right:auto;background:rgba(59,130,246,0.15);color:var(--accent2);font-size:9px;padding:1px 6px;border-radius:20px;font-weight:700}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#0098e6,#0077bb);color:#fff;border-radius:9px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s}
.tg-btn:hover{filter:brightness(1.1)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:7px}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:6px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px;transition:background .3s}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{width:28px;height:28px;border-radius:7px;overflow:hidden}
.mob-logo img{width:100%;height:100%;object-fit:cover}
.mob-title{color:var(--t1);font-size:13px;font-weight:700}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:#A78BFA}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:17px 17px 14px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
.m-icon{width:34px;height:34px;border-radius:8px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:17px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:25px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:12px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:16px;padding:20px 22px;margin-bottom:18px;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:background .3s}
.vless-box::before{content:'';position:absolute;top:-50px;left:-50px;width:180px;height:180px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:11px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{background:rgba(0,0,0,.18);border:1px solid var(--card-b);border-radius:9px;padding:13px 15px;font-size:11px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.8;letter-spacing:.01em}
[data-theme="light"] .vl-code{background:rgba(0,0,0,.04)}
.vl-actions{display:flex;gap:8px;margin-top:13px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:500;border-radius:8px;padding:8px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:13px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:var(--accent);color:#fff;box-shadow:0 2px 12px rgba(59,130,246,.3)}
.btn-p:hover{background:#2563EB;box-shadow:0 4px 18px rgba(59,130,246,.4)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(59,130,246,.3)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(59,130,246,.15)}
.btn-g:hover{background:rgba(59,130,246,.22)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.2)}
.btn-pur{background:var(--purple-bg);color:#A78BFA;border:1px solid rgba(139,92,246,.2)}
.btn-pur:hover{background:rgba(139,92,246,.22)}
.btn-sm{padding:5px 9px;font-size:10.5px;border-radius:7px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(59,130,246,0.05);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.ch{position:relative;height:210px}
.ch-lg{position:relative;height:310px}
.ch-sm{position:relative;height:165px}
.tbl{width:100%;border-collapse:collapse}
.tbl th{text-align:right;font-size:9.5px;color:var(--t3);font-weight:700;padding:9px 9px;border-bottom:1px solid var(--card-b);text-transform:uppercase;letter-spacing:.07em;white-space:nowrap}
.tbl td{padding:11px 9px;border-bottom:1px solid rgba(59,130,246,0.04);font-size:12px;vertical-align:middle}
.tbl tr:last-child td{border-bottom:none}
.tbl tbody tr{transition:.12s}
.tbl tbody tr:hover td{background:var(--accent-d)}
.uuid-chip{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent2);background:var(--accent-d);padding:2px 7px;border-radius:5px;display:inline-block;letter-spacing:.02em;cursor:pointer;transition:.15s}
.uuid-chip:hover{background:rgba(59,130,246,.2)}
.ubar{height:6px;border-radius:3px;background:rgba(59,130,246,0.1);overflow:hidden;margin-bottom:3px}
.ubar-f{height:100%;border-radius:3px;transition:width .3s}
.utxt{font-size:9.5px;color:var(--t3)}
.ll{font-weight:600;color:var(--t1);font-size:12.5px}
.lm{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.exp-chip{font-size:9px;padding:2px 7px;border-radius:5px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}
.tog{width:34px;height:19px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;top:3px;right:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--green)}
.tog.on::after{right:18px}
.form-row{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{font-size:10px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.fi,.fs{padding:9px 12px;border-radius:8px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12px;outline:none;transition:.15s;min-width:100px}
[data-theme="light"] .fi,[data-theme="light"] .fs{background:rgba(0,0,0,.04)}
.fi::placeholder{color:var(--t3)}
.fi:focus,.fs:focus{border-color:rgba(59,130,246,.45);background:rgba(0,0,0,.25);box-shadow:0 0 0 3px rgba(59,130,246,.08)}
.fs option{background:var(--bg2)}
[data-theme="light"] .fs option{background:#fff}
.cl{background:var(--accent-d);border:1px solid rgba(59,130,246,.15);border-radius:10px;padding:11px 13px;font-size:11px;color:var(--t2);display:flex;gap:9px;align-items:flex-start;line-height:1.8;margin-top:12px}
.cl i{font-size:15px;color:var(--accent);margin-top:1px;flex-shrink:0}
.cl.amber{background:var(--amber-bg);border-color:rgba(245,158,11,.2);color:var(--amber-t)}
.cl.amber i{color:var(--amber)}
.sub-box{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.2);border-radius:10px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:11px}
.sub-url{font-family:ui-monospace,monospace;font-size:10.5px;color:#A78BFA;word-break:break-all;flex:1}
.erow{padding:9px 0;border-bottom:1px solid rgba(59,130,246,.05)}
.erow:last-child{border-bottom:none}
.etime{color:var(--t3);font-size:9.5px;margin-bottom:3px;display:flex;align-items:center;gap:4px}
.emsg{color:var(--red-t);font-family:ui-monospace,monospace;background:var(--red-bg);padding:6px 9px;border-radius:6px;word-break:break-all;font-size:10.5px}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:5px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s}
.empty{text-align:center;padding:44px 20px;color:var(--t3)}
.empty i{font-size:38px;opacity:.35;margin-bottom:10px;display:block}
.empty p{font-size:12px;margin-top:4px}
.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-bottom:18px}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:18px 20px;transition:all .2s;position:relative;overflow:hidden}
.sub-card::before{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--purple);opacity:.6}
.sub-card:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.sub-card-head{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px}
.sub-card-name{font-size:14px;font-weight:700;color:var(--t1)}
.sub-card-desc{font-size:11px;color:var(--t3);margin-top:3px;line-height:1.6}
.sub-card-meta{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.sub-meta-item{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--t3)}
.sub-meta-item i{font-size:12px}
.sub-card-footer{display:flex;gap:6px;flex-wrap:wrap;padding-top:12px;border-top:1px solid var(--card-b)}
.pub-url-box{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.2);border-radius:8px;padding:10px 13px;display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.pub-url-text{font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA;word-break:break-all;flex:1}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
.modal-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--accent)}
.lrow{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid rgba(59,130,246,.05)}
.lrow:last-child{border-bottom:none}
.lrow-check{width:16px;height:16px;border-radius:4px;cursor:pointer;accent-color:var(--accent)}
.lrow-label{flex:1;font-size:12px;color:var(--t1)}
.lrow-badge{font-size:9px;padding:2px 7px;border-radius:5px;background:var(--green-bg);color:var(--green-t);font-weight:700}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:10px 18px;font-size:12.5px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}
.dash-footer{border-top:1px solid var(--card-b);margin-top:14px;padding-top:14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.df-text{font-size:10px;color:var(--t3)}
.df-link{font-size:11.5px;color:var(--accent2);display:flex;align-items:center;gap:5px;font-weight:600}
@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,.4)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
  .tbl th:nth-child(2),.tbl td:nth-child(2){display:none}
  .sub-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="modal-bg" id="modal-links">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌های <span id="modal-sub-name" style="color:var(--accent)">—</span></div>
    <div id="modal-links-body">در حال بارگذاری...</div>
    <div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-links')">بستن</button>
      <button class="btn btn-p" id="modal-save-btn" onclick="saveSubLinks()"><i class="ti ti-check"></i> ذخیره</button>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-create-sub">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-folder-plus"></i> ساخت گروه جدید</div>
    <div class="fg" style="margin-bottom:13px"><label>نام گروه</label><input class="fi" id="ns-name" placeholder="مثلاً: کانال تلگرام" style="width:100%"></div>
    <div class="fg" style="margin-bottom:13px"><label>توضیحات (اختیاری)</label><input class="fi" id="ns-desc" placeholder="توضیح کوتاه" style="width:100%"></div>
    <div class="fg" style="margin-bottom:16px"><label>رمز صفحه پابلیک (اختیاری)</label><input class="fi" id="ns-pw" type="password" placeholder="خالی = بدون رمز" style="width:100%"></div>
    <div class="cl" style="margin-top:0"><i class="ti ti-info-circle"></i><span>صفحه پابلیک با لینک UUID-based در اینترنت قابل دسترس خواهد بود.</span></div>
    <div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-create-sub')">انصراف</button>
      <button class="btn btn-p" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت</button>
    </div>
  </div>
</div>
<div class="mob-top">
  <div class="ml">
    <div class="mob-logo"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="cb"></div>
    <span class="mob-title">RVG Gateway</span>
  </div>
  <div class="mob-right">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="logo-img"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="cb"></div>
    <div><div class="logo-name">codebox</div><div class="logo-sub">RVG Gateway · v9.0</div></div>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-it" data-pg="testws"><i class="ti ti-wifi"></i> تست WebSocket</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>
  <div class="sb-foot">
    <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button>
    <a class="tg-btn" href="https://t.me/CodeBoxo" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i> @CodeBoxo</a>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>
<main class="main">
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div>
    <div class="tb-right">
      <span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span>
      <span class="badge bg-blue" id="uptime-badge">—</span>
      <button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
    </div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> WebSocket زنده</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">از کل</div></div>
    <div class="metric pur"><div class="m-icon pur"><i class="ti ti-folders"></i></div><div class="m-label">گروه‌های ساب</div><div class="m-val" id="m-subs">—</div><div class="m-sub">فعال</div></div>
  </div>
  <div class="vless-box">
    <div class="vl-header">
      <div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
      <span class="badge bg-blue"><span class="dot db"></span> TLS 443 · WS</span>
    </div>
    <div class="vl-code" id="vless-main">در حال دریافت...</div>
    <div class="vl-actions">
      <button class="btn btn-p" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button>
      <button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button>
      <button class="btn btn-o" onclick="navTo('links')"><i class="ti ti-link-plus"></i> کانفیگ محدود</button>
      <button class="btn btn-pur" onclick="navTo('subgroups')"><i class="ti ti-folders"></i> گروه‌های ساب</button>
    </div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال · سخت‌گیرانه</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS / WS Tunnel</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-folders"></i> Sub Groups</span><span class="sr-v" style="color:var(--green-t)">● فعال v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div>
      <div class="sr" style="flex-direction:column;align-items:flex-start;gap:4px">
        <div style="width:100%;display:flex;justify-content:space-between"><span class="sr-k"><i class="ti ti-gauge"></i> بار نسبی</span><span class="sr-v" id="bw-pct">—%</span></div>
        <div class="spbar" style="width:100%"><div class="spfill" id="bw-bar" style="width:0%"></div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto badge bg-blue" id="lsummary-badge">۰</span></div>
      <div id="lsummary">—</div>
    </div>
  </div>
  <div class="dash-footer">
    <span class="df-text">codebox RVG Gateway v9.0 · Railway · 2025</span>
    <a class="df-link" href="https://t.me/CodeBoxo" target="_blank"><i class="ti ti-brand-telegram"></i> t.me/CodeBoxo</a>
  </div>
</section>
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ با سهمیه، انقضا و گروه‌بندی</div></div>
    <div class="tb-right"><span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span></div>
  </div>
  <div class="card mb16">
    <div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ جدید</div>
    <div class="form-row">
      <div class="fg" style="flex:1;min-width:140px"><label>عنوان</label><input class="fi" id="nl-label" placeholder="مثلاً: کاربر علی" style="width:100%"></div>
      <div class="fg"><label>سهمیه</label><input class="fi" id="nl-val" type="number" min="0" step="0.1" placeholder="0=∞" style="width:110px"></div>
      <div class="fg"><label>واحد</label><select class="fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div>
      <div class="fg"><label>انقضا (روز)</label><input class="fi" id="nl-exp" type="number" min="0" step="1" placeholder="0=∞" style="width:100px"></div>
      <div class="fg"><label>گروه ساب</label><select class="fs" id="nl-sub"><option value="">— بدون گروه —</option></select></div>
      <div class="fg" style="flex:1;min-width:120px"><label>یادداشت</label><input class="fi" id="nl-note" placeholder="اختیاری" style="width:100%"></div>
      <button class="btn btn-p" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت</button>
    </div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>UUID کاملاً رندوم · فقط UUID‌های ثبت‌شده می‌توانند اتصال برقرار کنند · می‌توانید بعداً گروه را تغییر دهید.</span></div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-list"></i> لیست کانفیگ‌ها</div>
    <div style="overflow-x:auto">
      <table class="tbl">
        <thead><tr><th>عنوان / یادداشت</th><th>UUID</th><th>مصرف / سهمیه</th><th>گروه</th><th>انقضا</th><th>وضعیت</th><th>عملیات</th></tr></thead>
        <tbody id="links-tb"></tbody>
      </table>
    </div>
    <div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>
  </div>
</section>
<section class="pg" id="pg-subgroups">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div><div class="tb-sub">هر گروه یک صفحه پابلیک دارد</div></div>
    <div class="tb-right">
      <span class="badge bg-purple" id="subs-pg-cnt">۰ گروه</span>
      <button class="btn btn-pur" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button>
    </div>
  </div>
  <div class="sub-grid" id="subs-grid">
    <div class="empty" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>
  </div>
</section>
<section class="pg" id="pg-subscriptions">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر کانفیگ)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد. از جدول کانفیگ‌ها روی آیکون <i class="ti ti-rss"></i> کلیک کنید.</p>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (ادمین)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:4px">شامل تمام کانفیگ‌های فعال.</p>
      <div class="sub-box"><span class="sub-url" id="sub-all-url">در حال دریافت...</span><div style="display:flex;gap:6px"><button class="btn btn-sm btn-g" onclick="cpSubAll()"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button></div></div>
      <div class="cl amber" style="margin-top:11px"><i class="ti ti-alert-triangle"></i><span>این آدرس فقط در مرورگری که به پنل وارد شده کار می‌کند (نیاز به کوکی سشن).</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-folders"></i> لینک سابسکریپشن گروه‌ها</div>
    <div id="sub-groups-list">در حال بارگذاری...</div>
  </div>
</section>
<section class="pg" id="pg-traffic">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="metrics" style="grid-template-columns:repeat(3,1fr)">
    <div class="metric"><div class="m-icon"><i class="ti ti-database"></i></div><div class="m-label">کل</div><div class="m-val" id="t-traffic">—<span class="m-unit">MB</span></div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-arrow-up"></i></div><div class="m-label">میانگین ساعتی</div><div class="m-val" id="t-avg">—<span class="m-unit">MB</span></div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-chart-bar"></i></div><div class="m-label">پیک ساعتی</div><div class="m-val" id="t-peak">—<span class="m-unit">MB</span></div></div>
  </div>
  <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> نمودار ترافیک ساعتی</div><div class="ch-lg"><canvas id="ch3"></canvas></div></div>
</section>
<section class="pg" id="pg-connections">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات</div></div><div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-list"></i> جزئیات</div><div id="conns-list"></div><div class="empty" id="conns-empty" style="display:none"><i class="ti ti-plug-off"></i><p>هیچ اتصال فعالی نیست</p></div></div>
</section>
<section class="pg" id="pg-security">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:var(--green-t)">● فعال (443)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> پروتکل</span><span class="sr-v">VLESS/WS</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> سشن</span><span class="sr-v">HttpOnly · 7 روز</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> UUID Auth سخت‌گیرانه</span><span class="sr-v" style="color:var(--green-t)">● فعال v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> فعال/غیرفعال کانفیگ</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-lock"></i> رمز صفحه پابلیک ساب</span><span class="sr-v" style="color:var(--green-t)">● اختیاری · SHA-256</span></div>
    </div>
  </div>
</section>
<section class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">۰</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div><div id="errs-full">—</div></div>
</section>
<section class="pg" id="pg-testws">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> تست WebSocket</div></div></div>
  <div class="card" style="max-width:660px">
    <div class="cl amber" style="margin-top:0;margin-bottom:12px"><i class="ti ti-alert-triangle"></i><span>فقط UUID‌های ثبت‌شده و فعال اتصال برقرار می‌کنند.</span></div>
    <div class="form-row" style="margin-bottom:12px">
      <div class="fg" style="flex:1"><label>UUID (باید در کانفیگ‌ها وجود داشته باشد)</label><input class="fi" id="ws-uuid" placeholder="UUID یک کانفیگ فعال" style="width:100%"></div>
      <button class="btn btn-p" onclick="wsConn()"><i class="ti ti-plug-connected"></i> اتصال</button>
      <button class="btn btn-d" onclick="wsDisc()"><i class="ti ti-plug-x"></i> قطع</button>
    </div>
    <div class="form-row" style="margin-bottom:12px">
      <input class="fi" id="ws-msg" placeholder="پیام تست..." style="flex:1">
      <button class="btn btn-o" onclick="wsSend()"><i class="ti ti-send"></i> ارسال</button>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:10px;padding:14px;height:250px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:10.5px;line-height:1.9" id="ws-log">
      <p style="color:var(--t3)">منتظر اتصال...</p>
    </div>
  </div>
</section>
<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-server"></i> اطلاعات سرور</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-world"></i> دامنه</span><span class="sr-v" id="set-host">—</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-route"></i> پورت</span><span class="sr-v">443 (TLS)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-versions"></i> نسخه</span><span class="sr-v">v9.0</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-brand-fastapi"></i> فریم‌ورک</span><span class="sr-v">FastAPI + Uvicorn</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cloud"></i> پلتفرم</span><span class="sr-v">Railway</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-device-floppy"></i> ذخیره‌سازی</span><span class="sr-v">JSON File (/data)</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-key"></i> تغییر رمز عبور</div>
      <div class="fg" style="margin-bottom:11px"><label>رمز فعلی</label><input class="fi" type="password" id="cp-cur" placeholder="رمز فعلی" style="width:100%"></div>
      <div class="fg" style="margin-bottom:11px"><label>رمز جدید</label><input class="fi" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" style="width:100%"></div>
      <div class="fg" style="margin-bottom:14px"><label>تکرار رمز جدید</label><input class="fi" type="password" id="cp-cf" placeholder="تکرار رمز جدید" style="width:100%"></div>
      <button class="btn btn-p" onclick="changePw()" style="width:100%;justify-content:center"><i class="ti ti-key"></i> تغییر رمز</button>
    </div>
  </div>
</section>
</main>
<script>
let isDark=localStorage.getItem('rvg-theme')!=='light';
function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  const icon=dark?'ti-sun':'ti-moon',label=dark?'تم روشن':'تم تاریک';
  document.getElementById('theme-icon').className='ti '+icon;
  document.getElementById('theme-label').textContent=label;
  const mobI=document.getElementById('theme-mob-icon');if(mobI)mobI.className='ti '+icon;
}
function toggleTheme(){isDark=!isDark;localStorage.setItem('rvg-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5))}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> ∞</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)}ر</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)}ر</span>`;
}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}
let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('m-subs').textContent=d.subs_count??'—';
    document.getElementById('errs-badge').textContent=d.total_errors+' خطا';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';
    document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}
function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:var(--green-t);padding:10px;font-size:12px;display:flex;align-items:center;gap:5px"><i class="ti ti-circle-check"></i> هیچ خطایی نیست</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}
let allSubsList=[];
async function loadLinks(){
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    allSubsList=subs;
    const nlSub=document.getElementById('nl-sub');
    nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';
    document.getElementById('lsummary-badge').textContent=toFa(links.length);
    const tb=document.getElementById('links-tb'),empty=document.getElementById('links-empty');
    if(!links.length){tb.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
    empty.style.display='none';
    const subMap=Object.fromEntries(subs.map(s=>[s.sub_id,s.name]));
    tb.innerHTML=links.map(l=>{
      const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
      const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
      const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
      const allowed=l.active&&!l.expired;
      const subOpts='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}"${l.sub_id===s.sub_id?' selected':''}>${esc(s.name)}</option>`).join('');
      return `<tr>
        <td><div class="ll">${esc(l.label)}</div><div class="lm"><span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span>${l.note?`<span title="${esc(l.note)}"><i class="ti ti-note"></i>${esc(l.note.slice(0,20))}${l.note.length>20?'…':''}</span>`:''}</div></td>
        <td><span class="uuid-chip" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}">${l.uuid.slice(0,13)}…</span></td>
        <td><div style="width:115px"><div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div><div class="utxt">${fmtB(l.used_bytes)} / ${lim}</div></div></td>
        <td><select class="fs" style="font-size:10px;padding:4px 8px;min-width:90px" onchange="moveLinkSub('${l.uuid}',this.value)">${subOpts}</select></td>
        <td>${expChip(l.expires_at,l.expired)}</td>
        <td><button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})"></button></td>
        <td><div style="display:flex;gap:4px;flex-wrap:nowrap">
          <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('VLESS کپی شد','ok'))" title="کپی VLESS"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))" title="Sub URL"><i class="ti ti-rss"></i></button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>
          <button class="btn btn-sm btn-g" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
          <button class="btn btn-sm btn-d" onclick="deleteLink('${l.uuid}')" title="حذف"><i class="ti ti-trash"></i></button>
        </div></td>
      </tr>`;
    }).join('');
    document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-v" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');
  }catch(e){console.error(e)}
}
async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const note=document.getElementById('nl-note').value.trim();
  const sub_id=document.getElementById('nl-sub').value||null;
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,sub_id})});
    if(!r.ok)throw new Error('failed');
    ['nl-label','nl-val','nl-exp','nl-note'].forEach(id=>document.getElementById(id).value='');
    toast('کانفیگ ساخته شد ✓','ok');loadLinks();
  }catch(e){toast('خطا در ساخت','err')}
}
async function moveLinkSub(uuid,newSubId){
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:newSubId||null})});
    if(!r.ok)throw new Error();
    toast('گروه تغییر کرد ✓','ok');loadLinks();
  }catch(e){toast('خطا','err')}
}
async function toggleActive(uuid,newState){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'فعال شد ✓':'غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function resetUsage(uuid){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('مصرف ریست شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function deleteLink(uuid){
  if(!confirm('حذف این کانفیگ؟'))return;
  try{const r=await authF('/api/links/'+uuid,{method:'DELETE'});if(!r.ok)throw new Error();toast('حذف شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}
let currentSubId=null;
async function loadSubs(){
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    document.getElementById('subs-nb').textContent=subs.length;
    document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';
    const grid=document.getElementById('subs-grid');
    if(!subs.length){grid.innerHTML='<div class="empty" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>';return}
    grid.innerHTML=subs.map(s=>`
      <div class="sub-card">
        <div class="sub-card-head">
          <div><div class="sub-card-name">${esc(s.name)}</div>${s.desc?`<div class="sub-card-desc">${esc(s.desc)}</div>`:''}</div>
          <div style="display:flex;gap:5px;flex-shrink:0">${s.has_password?'<span class="badge bg-amber"><i class="ti ti-lock"></i> رمز</span>':'<span class="badge bg-green"><i class="ti ti-globe"></i> پابلیک</span>'}</div>
        </div>
        <div class="sub-card-meta">
          <span class="sub-meta-item"><i class="ti ti-link"></i> ${toFa(s.links_count)} کانفیگ</span>
          <span class="sub-meta-item"><i class="ti ti-circle-check" style="color:var(--green)"></i> ${toFa(s.active_count)} فعال</span>
          <span class="sub-meta-item"><i class="ti ti-database"></i> ${esc(s.total_used_fmt)} مصرف</span>
          <span class="sub-meta-item"><i class="ti ti-calendar"></i> ${new Date(s.created_at).toLocaleDateString('fa-IR')}</span>
        </div>
        <div class="pub-url-box">
          <span class="pub-url-text">${esc(s.public_url)}</span>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('لینک پابلیک کپی شد','ok'))"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-pur" onclick="window.open('${esc(s.public_url)}','_blank')"><i class="ti ti-external-link"></i></button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')" title="QR کل گروه"><i class="ti ti-qrcode"></i></button>
        </div>
        <div class="sub-card-footer">
          <button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌ها</button>
          <button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک ساب کپی شد','ok'))"><i class="ti ti-rss"></i> کپی ساب</button>
          <button class="btn btn-sm btn-d" onclick="deleteSub('${esc(s.sub_id)}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
async function createSub(){
  const name=document.getElementById('ns-name').value.trim()||'گروه جدید';
  const desc=document.getElementById('ns-desc').value.trim();
  const pw=document.getElementById('ns-pw').value;
  try{
    const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw})});
    if(!r.ok)throw new Error('failed');
    ['ns-name','ns-desc','ns-pw'].forEach(id=>document.getElementById(id).value='');
    closeModal('modal-create-sub');
    toast('گروه ساخته شد ✓','ok');loadSubs();
  }catch(e){toast('خطا در ساخت گروه','err')}
}
async function deleteSub(sub_id){
  if(!confirm('حذف این گروه؟ کانفیگ‌ها حذف نمی‌شوند.'))return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}
}
async function openSubLinks(sub_id,name){
  currentSubId=sub_id;
  document.getElementById('modal-sub-name').textContent=name;
  document.getElementById('modal-links-body').innerHTML='<div style="color:var(--t3);font-size:12px;padding:10px">در حال بارگذاری...</div>';
  openModal('modal-links');
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    const thisSub=subs.find(s=>s.sub_id===sub_id);
    const inSub=new Set(thisSub?.link_ids||[]);
    if(!links.length){document.getElementById('modal-links-body').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>';return}
    document.getElementById('modal-links-body').innerHTML=links.map(l=>`
      <div class="lrow">
        <input type="checkbox" class="lrow-check" id="lc-${l.uuid}" ${inSub.has(l.uuid)?'checked':''} value="${l.uuid}">
        <label for="lc-${l.uuid}" class="lrow-label">${esc(l.label)}</label>
        ${l.active&&!l.expired?'<span class="lrow-badge">فعال</span>':'<span class="lrow-badge" style="background:var(--red-bg);color:var(--red-t)">غیرفعال</span>'}
        <span style="font-size:9.5px;color:var(--t3)">${fmtB(l.used_bytes)}</span>
      </div>
    `).join('');
  }catch(e){toast('خطا در بارگذاری','err')}
}
async function saveSubLinks(){
  if(!currentSubId)return;
  const checks=document.querySelectorAll('#modal-links-body .lrow-check');
  const link_ids=[...checks].filter(c=>c.checked).map(c=>c.value);
  try{
    const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});
    if(!r.ok)throw new Error();
    const allChecks=[...checks].map(c=>({uuid:c.value,inSub:c.checked}));
    await Promise.all(allChecks.map(({uuid,inSub})=>
      authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:inSub?currentSubId:null})})
    ));
    closeModal('modal-links');
    toast('کانفیگ‌های گروه ذخیره شدند ✓','ok');
    loadSubs();loadLinks();
  }catch(e){toast('خطا در ذخیره','err')}
}
async function loadSubsPage(){
  document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all';
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    const el=document.getElementById('sub-groups-list');
    if(!subs.length){el.innerHTML='<div class="empty"><i class="ti ti-rss-off"></i><p>هنوز گروهی ندارید</p></div>';return}
    el.innerHTML=subs.map(s=>`
      <div style="padding:13px 15px;background:var(--accent-d);border:1px solid var(--card-b);border-radius:10px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:13px;margin-bottom:3px">${esc(s.name)}</div>
          <div style="font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA">${esc(s.sub_url)}</div>
          <div style="font-size:10px;color:var(--t3);margin-top:3px">${toFa(s.links_count)} کانفیگ · ${esc(s.total_used_fmt)} مصرف ${s.has_password?'· 🔒 رمزدار':''}</div>
        </div>
        <div style="display:flex;gap:5px;flex-wrap:wrap">
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i> پابلیک</button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){}
}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ✓','ok'))}
async function loadConns(){
  try{const r=await authF('/stats'),d=await r.json();const cl=document.getElementById('conns-list'),ce=document.getElementById('conns-empty');if(d.active_connections===0){cl.innerHTML='';ce.style.display='block';return}ce.style.display='none';cl.innerHTML=`<div style="padding:13px;background:var(--green-bg);border:1px solid rgba(16,185,129,.15);border-radius:9px;display:flex;align-items:center;gap:12px;font-size:12px;color:var(--green-t)"><span class="dot dg pulse"></span>${d.active_connections} اتصال فعال · کل ${d.total_traffic_mb.toFixed(1)} MB</div>`;}catch(e){}
}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){
  try{const r=await authF('/api/links'),d=await r.json();const links=d.links||[];const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];document.getElementById('vless-main').textContent=def?def.vless_link:'هنوز کانفیگی وجود ندارد';}catch(e){}
}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();toast('رفرش شد','ok')}
async function changePw(){
  const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
  if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}
  if(nw.length<4){toast('حداقل ۴ کاراکتر','err');return}
  if(nw!==cf){toast('تکرار رمز اشتباه','err');return}
  try{
    const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    toast('رمز تغییر کرد ✓','ok');
    ['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast('✗ '+e.message,'err')}
}
function initCharts(){
  const opts={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'rgba(13,27,46,.95)',borderColor:'rgba(59,130,246,.2)',borderWidth:1,titleColor:'#E8F4FF',bodyColor:'#7BAED4',callbacks:{label:v=>`${v.parsed.y.toFixed(2)} MB`}}},scales:{x:{grid:{color:'rgba(59,130,246,.04)'},ticks:{color:'#3D6B8E',font:{size:9}}},y:{grid:{color:'rgba(59,130,246,.04)'},ticks:{color:'#3D6B8E',font:{size:9},callback:v=>v+'MB'}}}};
  const ds={label:'MB',data:[],borderColor:'rgba(59,130,246,.8)',backgroundColor:'rgba(59,130,246,.05)',fill:true,tension:.45,pointRadius:3,pointHoverRadius:5,borderWidth:2};
  ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch3=new Chart(document.getElementById('ch3'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch2=new Chart(document.getElementById('ch2'),{type:'doughnut',data:{labels:['VLESS/WS','HTTP Proxy','سایر'],datasets:[{data:[70,25,5],backgroundColor:['rgba(59,130,246,.8)','rgba(16,185,129,.7)','rgba(139,92,246,.7)'],borderColor:'rgba(0,0,0,0)',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{color:'var(--t2)',font:{size:9},padding:10,usePointStyle:true}}}}});
}
let ws;
function wsLog(c,m){const l=document.getElementById('ws-log'),p=document.createElement('p');const colors={ok:'#34D399',err:'#F87171',info:'#7BAED4',sent:'#FCD34D'};p.style.color=colors[c]||'#fff';p.textContent='['+new Date().toLocaleTimeString('fa-IR')+'] '+m;l.appendChild(p);l.scrollTop=l.scrollHeight}
function wsConn(){const u=document.getElementById('ws-uuid').value.trim();if(!u){toast('UUID را وارد کنید','err');return}const url=(location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws/'+u;wsLog('info','اتصال: '+url);ws=new WebSocket(url);ws.onopen=()=>wsLog('ok','✓ متصل - UUID معتبر');ws.onerror=()=>wsLog('err','✗ خطا - UUID نامعتبر یا غیرفعال');ws.onmessage=m=>wsLog('info','دریافت '+(m.data.size||m.data.length)+' byte');ws.onclose=e=>wsLog('err','قطع ('+e.code+')'+(e.code===1008?' - دسترسی رد شد':''))}
function wsSend(){const m=document.getElementById('ws-msg').value;if(!m||!ws||ws.readyState!==1)return;ws.send(m);wsLog('sent','ارسال: '+m);document.getElementById('ws-msg').value=''}
function wsDisc(){if(ws)ws.close()}
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  document.getElementById('sub-all-url')&&(document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all');
  fetchStats();fetchDefaultVless();loadLinks();loadSubs();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('pg-links').classList.contains('on'))loadLinks();
    if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();
    if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();
  },5000);
});
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب — نمایش کانفیگ‌ها با QR code و آمار"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RVG Sub · codebox</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#060f1d;--bg2:#0a1628;--card:#0d1b2e;--card-b:rgba(59,130,246,0.13);--accent:#3B82F6;--accent2:#60A5FA;--accent-d:rgba(59,130,246,0.12);--green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;--red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;--amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;--purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.1);--t1:#E8F4FF;--t2:#7BAED4;--t3:#3D6B8E;--radius:14px;--shadow:0 4px 24px rgba(0,0,0,0.35)}}
html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif;color:var(--t1);font-size:14px}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 0%,rgba(59,130,246,0.08),transparent 60%),var(--bg);z-index:0;pointer-events:none}}
.grid{{position:fixed;inset:0;background-image:linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px);background-size:44px 44px;z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:780px;margin:0 auto;padding:28px 16px 60px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;flex-wrap:wrap;gap:12px}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand-img{{width:42px;height:42px;border-radius:11px;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 18px rgba(59,130,246,.25)}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:15px;font-weight:700;color:var(--t1)}}
.brand-sub{{font-size:10px;color:var(--t3)}}
.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:22px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:14px 16px}}
.stat-label{{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}}
.stat-val{{font-size:22px;font-weight:700;color:var(--t1);line-height:1}}
.stat-sub{{font-size:10px;color:var(--t3);margin-top:4px}}
.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:20px 22px;margin-bottom:18px}}
.sub-name{{font-size:20px;font-weight:700;color:var(--t1);margin-bottom:6px}}
.sub-desc{{font-size:12px;color:var(--t2);line-height:1.8;margin-bottom:14px}}
.sub-sub-box{{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.2);border-radius:9px;padding:11px 13px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA;word-break:break-all;flex:1}}
.cfg-title{{font-size:13px;font-weight:700;color:var(--t2);margin-bottom:12px;display:flex;align-items:center;gap:6px;text-transform:uppercase;letter-spacing:.06em}}
.cfg-title i{{color:var(--accent);font-size:16px}}
.cfg-grid{{display:grid;gap:12px}}
.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:16px 18px;transition:all .2s;position:relative;overflow:hidden}}
.cfg-card::after{{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--green);opacity:.7}}
.cfg-card.inactive::after{{background:var(--red)}}
.cfg-card:hover{{border-color:rgba(59,130,246,.28);transform:translateY(-2px);box-shadow:var(--shadow)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px}}
.cfg-label{{font-size:14px;font-weight:700;color:var(--t1)}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:3px 9px;border-radius:20px}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.cfg-usage{{margin-bottom:14px}}
.ubar{{height:7px;border-radius:4px;background:rgba(59,130,246,0.1);overflow:hidden;margin-bottom:4px}}
.ubar-f{{height:100%;border-radius:4px;transition:width .4s}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}
.cfg-vless{{background:rgba(0,0,0,.2);border:1px solid var(--card-b);border-radius:8px;padding:10px 12px;font-size:10px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.7;margin-bottom:12px}}
.cfg-actions{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.btn{{font-family:inherit;font-size:11.5px;font-weight:600;border-radius:8px;padding:7px 13px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}}
.btn i{{font-size:12px}}
.btn-p{{background:var(--accent);color:#fff;box-shadow:0 2px 12px rgba(59,130,246,.3)}}
.btn-p:hover{{background:#2563EB}}
.btn-g{{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(59,130,246,.15)}}
.btn-g:hover{{background:rgba(59,130,246,.22)}}
.btn-pur{{background:var(--purple-bg);color:#A78BFA;border:1px solid rgba(139,92,246,.2)}}
.btn-pur:hover{{background:rgba(139,92,246,.22)}}
.conn-chip{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;padding:3px 8px;border-radius:20px;background:var(--green-bg);color:var(--green-t);font-weight:700}}
.dot{{width:5px;height:5px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.lock-card{{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:38px 32px;text-align:center;max-width:380px;margin:80px auto}}
.lock-icon{{font-size:48px;color:var(--accent);margin-bottom:16px;opacity:.7}}
.lock-title{{font-size:18px;font-weight:700;margin-bottom:6px}}
.lock-sub{{font-size:12px;color:var(--t3);margin-bottom:22px}}
.lock-inp{{width:100%;padding:11px 14px;border-radius:9px;border:1px solid var(--card-b);background:rgba(0,0,0,.3);color:var(--t1);font-family:inherit;font-size:13px;outline:none;margin-bottom:12px;text-align:center;letter-spacing:.1em}}
.lock-inp:focus{{border-color:rgba(59,130,246,.5);box-shadow:0 0 0 3px rgba(59,130,246,.1)}}
.lock-err{{color:var(--red-t);font-size:11.5px;margin-bottom:12px;min-height:16px}}
.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:9px 18px;font-size:12px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:7px;box-shadow:var(--shadow);white-space:nowrap}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}}
.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(4px)}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:24px;text-align:center;max-width:340px;width:calc(100% - 32px)}}
.qr-title{{font-size:14px;font-weight:700;margin-bottom:16px;color:var(--t1)}}
.qr-img{{border-radius:12px;overflow:hidden;margin-bottom:14px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:8px;border-radius:12px}}
.footer{{text-align:center;padding-top:30px;font-size:11px;color:var(--t3)}}
.footer a{{color:var(--accent2);font-weight:600}}
@media(max-width:500px){{.stats-bar{{grid-template-columns:1fr 1fr}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid"></div>
<div class="toast" id="toast"></div>
<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>
<div class="wrap">
  <div class="top">
    <div class="brand">
      <div class="brand-img"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="cb"></div>
      <div><div class="brand-name">codebox</div><div class="brand-sub">RVG Gateway · v9.0</div></div>
    </div>
    <a href="https://t.me/CodeBoxo" target="_blank" style="display:flex;align-items:center;gap:5px;font-size:12px;color:#A78BFA;font-weight:600"><i class="ti ti-brand-telegram" style="font-size:16px"></i> @CodeBoxo</a>
  </div>
  <div id="root">
    <div style="text-align:center;padding:80px 20px;color:var(--t3)"><i class="ti ti-loader-2" style="font-size:38px;display:block;margin-bottom:14px;animation:spin 1s linear infinite"></i>در حال بارگذاری...</div>
  </div>
  <div class="footer">کانال رسمی: <a href="https://t.me/CodeBoxo" target="_blank">@CodeBoxo</a> · RVG Gateway v9.0</div>
</div>
<script>
const UUID_KEY='{uuid_key}';
let savedPw='';

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
function toFa(n){{return String(n).replace(/\\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

async function loadData(pw=''){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}

function renderLock(name,errMsg=''){{
  document.getElementById('root').innerHTML=`
    <div class="lock-card">
      <div class="lock-icon"><i class="ti ti-lock"></i></div>
      <div class="lock-title">${{esc(name)}}</div>
      <div class="lock-sub">این گروه رمزدار است. رمز را وارد کنید.</div>
      <div class="lock-err" id="lock-err">${{esc(errMsg)}}</div>
      <input class="lock-inp" type="password" id="lock-pw" placeholder="رمز عبور" autofocus>
      <button class="btn btn-p" style="width:100%;justify-content:center" onclick="submitLock()"><i class="ti ti-lock-open"></i> ورود</button>
    </div>
  `;
  document.getElementById('lock-pw').addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}});
}}

async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{renderLock(data.name,'رمز اشتباه است');return}}
  savedPw=pw;
  renderContent(data);
}}

function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;

  /* ── لینک ساب کل گروه ──
     d.sub_url از سرور میاد: https://host/sub-group/uuid_key
     اگه به هر دلیلی خالی بود، خودمون میسازیم */
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
  const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');

  /* ── ذخیره global برای دسترسی از onclick ها ── */
  window._rvgSubUrl  = subUrl;
  window._rvgSubName = d.name;
  window._rvgLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    sub   : l.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''),
    label : l.label,
  }}));

  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div style="font-size:11px;color:var(--t3);margin-bottom:12px;display:flex;align-items:center;gap:5px">
        <i class="ti ti-clock"></i> آخرین بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}
      </div>
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(subUrl)}}</span>
        <button class="btn btn-pur" style="padding:5px 10px;font-size:11px"
          onclick="navigator.clipboard.writeText(window._rvgSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-g" style="padding:5px 10px;font-size:11px"
          onclick="showQR(window._rvgSubName + ' — کل گروه', window._rvgSubUrl)">
          <i class="ti ti-qrcode"></i> QR کل
        </button>
      </div>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{toFa(activeCount)}}</div>
        <div class="stat-sub">از ${{toFa(d.links.length)}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{toFa(d.active_connections)}}</div>
        <div class="stat-sub" style="color:var(--green-t);display:flex;align-items:center;gap:4px"><span class="dot"></span> آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف</div>
        <div class="stat-val" style="font-size:17px;margin-top:3px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">همه کانفیگ‌ها</div>
      </div>
    </div>

    <div class="cfg-title"><i class="ti ti-link"></i> کانفیگ‌ها (${{toFa(d.links.length)}} عدد)</div>
    <div class="cfg-grid">
      ${{d.links.map((l, i) => {{
        const pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
        return `
          <div class="cfg-card${{l.active ? '' : ' inactive'}}">
            <div class="cfg-head">
              <div>
                <div class="cfg-label">${{esc(l.label)}}</div>
                ${{l.connections > 0 ? `<span class="conn-chip" style="margin-top:4px;display:inline-flex"><span class="dot"></span> ${{toFa(l.connections)}} اتصال</span>` : ''}}
              </div>
              <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '<i class="ti ti-circle-check"></i> فعال' : '<i class="ti ti-circle-x"></i> غیرفعال'}}</span>
            </div>
            <div class="cfg-usage">
              <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
              <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{lim}}</span></div>
            </div>
            <div class="cfg-vless">${{esc(l.vless_link)}}</div>
            <div class="cfg-actions">
              <button class="btn btn-p"
                onclick="navigator.clipboard.writeText(window._rvgLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))">
                <i class="ti ti-copy"></i> کپی لینک
              </button>
              <button class="btn btn-g"
                onclick="showQR(window._rvgLinks[${{i}}].label, window._rvgLinks[${{i}}].vless)">
                <i class="ti ti-qrcode"></i> QR
              </button>
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}

async function autoRefresh(){{
  try{{
    const data = await loadData(savedPw);
    if (!data.locked) renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    if (data.locked) {{ renderLock(data.name); return; }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML =
      '<div style="text-align:center;padding:80px 20px;color:var(--red-t)"><i class="ti ti-alert-circle" style="font-size:38px;display:block;margin-bottom:14px"></i>خطا در بارگذاری</div>';
  }}
}}

init();
</script>
</body></html>"""

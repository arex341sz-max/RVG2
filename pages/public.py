# pages/public.py — صفحه پابلیک ساب‌گروه

def get_html(uuid_key: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>اشتراک · RVG Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg:#03080f;
  --surface:rgba(8,18,32,0.9);
  --card:rgba(10,22,38,0.75);
  --accent:#3B82F6;
  --accent-glow:rgba(59,130,246,0.25);
  --accent-soft:rgba(59,130,246,0.1);
  --text:#E8F4FF;
  --text-dim:#4a7fa8;
  --text-mid:#7BAED4;
  --border:rgba(59,130,246,0.16);
  --green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;
  --purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.1);
  --pink:#EC4899;--pink-bg:rgba(236,72,153,0.1);--pink-t:#F472B6;
}}
html,body{{min-height:100%}}
body{{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg);color:var(--text);
  min-height:100vh;display:flex;flex-direction:column;align-items:center;
  padding:36px 16px 60px;font-size:14px;
}}

/* bg */
.bg-base{{position:fixed;inset:0;z-index:0;background:var(--bg)}}
.bg-radial{{
  position:fixed;inset:0;z-index:1;
  background:
    radial-gradient(ellipse 60% 50% at 50% -5%,rgba(59,130,246,0.12),transparent 65%),
    radial-gradient(ellipse 35% 35% at 90% 85%,rgba(16,185,129,0.05),transparent 60%);
}}
.bg-grid{{
  position:fixed;inset:0;z-index:1;
  background-image:linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px);
  background-size:52px 52px;
  mask-image:radial-gradient(ellipse 90% 90% at 50% 50%,black,transparent);
}}

.wrap{{position:relative;z-index:10;width:100%;max-width:680px}}

/* hero card */
.hero{{
  background:var(--surface);
  border:1px solid var(--border);border-radius:20px;
  padding:24px 24px 20px;
  backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
  box-shadow:0 0 0 1px rgba(255,255,255,0.03) inset,0 24px 80px rgba(0,0,0,.55);
  margin-bottom:14px;
  animation:fadeUp .45s cubic-bezier(.16,1,.3,1) both;
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}

.hero-head{{display:flex;align-items:center;gap:13px;margin-bottom:18px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
.hero-icon{{
  width:42px;height:42px;border-radius:12px;
  background:linear-gradient(135deg,rgba(59,130,246,0.25),rgba(59,130,246,0.08));
  border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  color:var(--accent);font-size:20px;flex-shrink:0;
  box-shadow:0 0 16px var(--accent-glow);
}}
.hero-title{{font-size:17px;font-weight:700;letter-spacing:-.02em}}
.hero-sub{{font-size:11.5px;color:var(--text-dim);margin-top:3px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.hero-sub span{{display:flex;align-items:center;gap:4px}}
.hero-sub i{{font-size:12px;color:var(--text-dim)}}

.actions{{display:flex;gap:8px;flex-wrap:wrap}}
.btn{{
  font-family:inherit;font-size:12.5px;font-weight:500;
  border-radius:9px;padding:9px 16px;cursor:pointer;
  display:inline-flex;align-items:center;gap:6px;
  border:none;transition:all .15s;white-space:nowrap;
}}
.btn i{{font-size:13px}}
.btn-p{{background:var(--accent);color:#fff;box-shadow:0 2px 16px rgba(59,130,246,.35)}}
.btn-p:hover{{background:#2563EB;box-shadow:0 4px 22px rgba(59,130,246,.5);transform:translateY(-1px)}}
.btn-g{{background:rgba(59,130,246,0.1);color:#60A5FA;border:1px solid rgba(59,130,246,0.18)}}
.btn-g:hover{{background:rgba(59,130,246,0.18);transform:translateY(-1px)}}
.btn:active{{transform:translateY(0)!important}}

/* link cards */
.links-wrap{{display:flex;flex-direction:column;gap:10px;margin-top:14px}}
.link-card{{
  background:var(--card);border:1px solid var(--border);
  border-radius:14px;padding:16px 18px;
  transition:all .18s;
  animation:fadeUp .45s cubic-bezier(.16,1,.3,1) both;
}}
.link-card:hover{{border-color:rgba(59,130,246,0.32);background:rgba(10,22,38,0.9);transform:translateX(-2px)}}
.link-head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:6px}}
.link-name{{font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px}}
.link-tags{{display:flex;gap:4px;flex-wrap:wrap;align-items:center}}

/* proto tags */
.pt{{font-size:9px;padding:2px 8px;border-radius:5px;font-weight:700;display:inline-flex;align-items:center;gap:2px;letter-spacing:.03em}}
.pt-vless{{background:rgba(59,130,246,0.14);color:#60A5FA}}
.pt-trojan{{background:rgba(16,185,129,0.14);color:#34D399}}
.pt-hysteria2{{background:rgba(245,158,11,0.14);color:#FCD34D}}
.pt-vmess{{background:rgba(139,92,246,0.14);color:#A78BFA}}
.pt-wireguard{{background:rgba(236,72,153,0.14);color:#F472B6}}
.pt-off{{background:rgba(239,68,68,0.1);color:#F87171}}

/* link uri */
.link-uri{{
  font-family:ui-monospace,monospace;font-size:10.5px;
  color:var(--text-mid);line-height:1.7;
  padding:10px 12px;border-radius:9px;
  background:rgba(0,0,0,.2);border:1px solid rgba(59,130,246,0.08);
  word-break:break-all;
  max-height:62px;overflow:hidden;
  margin-bottom:10px;
}}

/* link actions */
.link-bottom{{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}}
.link-meta{{display:flex;gap:12px;flex-wrap:wrap;font-size:10.5px;color:var(--text-dim)}}
.link-meta span{{display:flex;align-items:center;gap:4px}}
.link-meta i{{font-size:11px}}
.link-btns{{display:flex;gap:6px}}
.btn-sm{{padding:6px 11px;font-size:11px;border-radius:7px}}

/* usage bar */
.usage-wrap{{margin-top:10px}}
.ubar{{height:4px;border-radius:3px;background:rgba(59,130,246,0.1);overflow:hidden}}
.ubar-f{{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),#60A5FA);transition:width .4s ease}}

/* password box */
.pw-box{{
  background:var(--surface);border:1px solid var(--border);border-radius:20px;
  padding:48px 32px;text-align:center;
  backdrop-filter:blur(28px);
  animation:fadeUp .45s cubic-bezier(.16,1,.3,1) both;
}}
.pw-box h2{{font-size:20px;font-weight:700;margin-bottom:8px}}
.pw-box p{{font-size:12.5px;color:var(--text-dim);margin-bottom:20px}}
.pw-input{{
  padding:12px 16px;border-radius:11px;
  border:1px solid var(--border);
  background:rgba(0,0,0,.3);color:var(--text);
  font-family:inherit;font-size:14px;outline:none;
  width:100%;max-width:280px;display:block;margin:0 auto 14px;text-align:center;
  transition:.2s;
}}
.pw-input:focus{{border-color:rgba(59,130,246,.5);box-shadow:0 0 0 3px rgba(59,130,246,.1)}}

/* empty / error */
.empty{{
  background:var(--surface);border:1px solid var(--border);border-radius:20px;
  padding:60px 32px;text-align:center;
  backdrop-filter:blur(28px);
  animation:fadeUp .45s cubic-bezier(.16,1,.3,1) both;
}}
.empty-icon{{font-size:40px;opacity:.25;margin-bottom:12px;display:block}}
.empty p{{font-size:13px;color:var(--text-dim)}}

/* toast */
.toast{{
  position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(80px);
  background:rgba(16,24,40,.95);border:1px solid var(--border);
  border-radius:12px;padding:11px 20px;
  font-size:12.5px;color:var(--text);
  backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(0,0,0,.5);
  display:flex;align-items:center;gap:8px;z-index:9999;
  transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .3s;
  opacity:0;white-space:nowrap;
}}
.toast.show{{transform:translateX(-50%) translateY(0);opacity:1}}
.toast i{{color:var(--green);font-size:15px}}

/* modal */
.modal-bg{{
  position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:999;
  display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(6px);padding:20px;
}}
.modal{{
  background:var(--surface);border:1px solid var(--border);
  border-radius:18px;padding:28px;text-align:center;max-width:300px;width:100%;
  box-shadow:0 24px 80px rgba(0,0,0,.6);
}}
.modal img{{border-radius:10px;margin-bottom:14px;display:block;margin-inline:auto}}
.modal p{{font-size:11px;color:var(--text-dim);margin-bottom:14px;word-break:break-all;line-height:1.6}}

.footer{{text-align:center;font-size:11px;color:var(--text-dim);margin-top:28px;position:relative;z-index:10}}
.footer a{{color:var(--accent);text-decoration:none;font-weight:600}}
.footer a:hover{{color:#60A5FA}}

@keyframes spin{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="bg-base"></div>
<div class="bg-radial"></div>
<div class="bg-grid"></div>

<div class="wrap" id="wrap">
  <div class="hero">
    <div style="text-align:center;padding:28px 0;color:var(--text-dim)">
      <i class="ti ti-loader-2" style="font-size:26px;animation:spin 1s linear infinite;display:block;margin-bottom:8px"></i>
      <span style="font-size:12px">در حال بارگذاری...</span>
    </div>
  </div>
</div>

<div class="footer">RVG Gateway v10.0 · <a href="https://t.me/CodeBoxo" target="_blank">@CodeBoxo</a></div>

<div class="toast" id="toast"><i class="ti ti-check"></i><span id="toast-text">کپی شد!</span></div>

<script>
const KEY = '{uuid_key}';
let subData = null;

function esc(s){{return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;')}}

function showToast(msg='کپی شد!'){{
  const t = document.getElementById('toast');
  document.getElementById('toast-text').textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2200);
}}

function cp(text){{
  navigator.clipboard.writeText(text).then(()=>showToast('کپی شد!')).catch(()=>showToast('خطا در کپی'));
}}

function cpSub(){{
  cp(location.protocol+'//'+location.host+'/sub-group/'+KEY);
  showToast('لینک سابسکریپشن کپی شد!');
}}

function qrShow(t){{
  let m = document.createElement('div');
  m.className='modal-bg';
  m.innerHTML=`<div class="modal">
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&color=60A5FA&bgcolor=03080f&data=${{encodeURIComponent(t)}}" width="220" height="220">
    <p>${{esc(t)}}</p>
    <button class="btn btn-g" onclick="this.closest('.modal-bg').remove()"><i class="ti ti-x"></i> بستن</button>
  </div>`;
  m.onclick = e=>{{if(e.target===m)m.remove()}};
  document.body.appendChild(m);
}}

function protoClass(p){{
  const map={{vless:'pt-vless',trojan:'pt-trojan',hysteria2:'pt-hysteria2',vmess:'pt-vmess',wireguard:'pt-wireguard'}};
  return map[p]||'pt-vless';
}}

function usageWidth(used,limit){{
  if(!limit||limit===0)return 100;
  return Math.min(100,(used/limit)*100);
}}

function usageColor(pct){{
  if(pct>=90)return 'var(--red)';
  if(pct>=70)return 'var(--amber)';
  return 'var(--accent)';
}}

async function load(){{
  const wrap = document.getElementById('wrap');
  try{{
    const r = await fetch('/api/public/sub/'+KEY);
    const d = await r.json();
    subData = d;

    if(d.locked){{
      wrap.innerHTML=`<div class="pw-box">
        <div style="font-size:36px;margin-bottom:12px"><i class="ti ti-lock" style="color:var(--amber)"></i></div>
        <h2>${{esc(d.name)}}</h2>
        <p>این صفحه رمزدار است. رمز را وارد کنید.</p>
        <input class="pw-input" type="password" id="pw-inp" placeholder="رمز عبور">
        <button class="btn btn-p" style="margin:0 auto;display:flex" onclick="unlock()"><i class="ti ti-lock-open"></i> باز کردن</button>
      </div>`;
      setTimeout(()=>document.getElementById('pw-inp')?.focus(),100);
      return;
    }}

    if(!d.links||!d.links.length){{
      wrap.innerHTML='<div class="empty"><i class="ti ti-link-off empty-icon"></i><p>لینکی در این اشتراک موجود نیست</p></div>';
      return;
    }}

    const usedPct = d.total_used&&d.total_limit ? Math.round((d.total_used/d.total_limit)*100) : 0;
    const uColor = usageColor(usedPct);

    let html = `<div class="hero">
      <div class="hero-head">
        <div class="hero-icon"><i class="ti ti-rss"></i></div>
        <div>
          <div class="hero-title">${{esc(d.name)}}</div>
          <div class="hero-sub">
            <span><i class="ti ti-plug"></i> ${{d.active_connections||0}} اتصال فعال</span>
            <span><i class="ti ti-database"></i> ${{d.total_used_fmt||'0 B'}} مصرف</span>
            <span><i class="ti ti-link"></i> ${{d.links.length}} لینک</span>
          </div>
        </div>
      </div>`;

    if(d.total_limit){{
      html+=`<div class="usage-wrap" style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;font-size:10.5px;color:var(--text-dim);margin-bottom:5px">
          <span>مصرف کلی</span>
          <span style="color:${{uColor}};font-weight:600">${{usedPct}}%</span>
        </div>
        <div class="ubar"><div class="ubar-f" style="width:${{usedPct}}%;background:linear-gradient(90deg,${{uColor}},${{uColor}}aa)"></div></div>
      </div>`;
    }}

    html+=`<div class="actions">
      <button class="btn btn-p" onclick="cpSub()"><i class="ti ti-copy"></i> کپی سابسکریپشن</button>
      <a class="btn btn-g" href="/sub-group/${{KEY}}" target="_blank"><i class="ti ti-external-link"></i> باز در اپ</a>
    </div>`;

    html+=`</div><div class="links-wrap">`;

    d.links.forEach((l,idx)=>{{
      const pc = protoClass(l.protocol||'vless');
      const animDelay = idx*0.06;
      const lu = l.used_bytes||0, ll = l.limit_bytes||0;
      const lPct = ll ? Math.min(100,Math.round((lu/ll)*100)) : 0;
      const lColor = usageColor(lPct);
      html+=`<div class="link-card" style="animation-delay:${{animDelay}}s">
        <div class="link-head">
          <div class="link-name">
            <span class="pt ${{pc}}">${{(l.protocol||'vless').toUpperCase()}}</span>
            ${{esc(l.label)}}
            ${{l.active?'':'<span class="pt pt-off">غیرفعال</span>'}}
          </div>
        </div>
        <div class="link-uri">${{esc(l.link_url)}}</div>
        ${{ll?`<div class="usage-wrap" style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-dim);margin-bottom:4px">
            <span>${{l.used_fmt}} / ${{l.limit_fmt}}</span>
            <span style="color:${{lColor}};font-weight:600">${{lPct}}%</span>
          </div>
          <div class="ubar"><div class="ubar-f" style="width:${{lPct}}%;background:${{lColor}}"></div></div>
        </div>`:'<div class="link-bottom" style="margin-bottom:10px"><div class="link-meta"><span><i class="ti ti-database"></i> ${{l.used_fmt}}</span>${{l.connections?`<span><i class="ti ti-plug"></i> ${{l.connections}} اتصال</span>`:\'\'}}${{l.limit_fmt&&l.limit_fmt!==\'نامحدود\'?`<span><i class="ti ti-infinity"></i> ${{l.limit_fmt}}</span>`:\'<span><i class="ti ti-infinity"></i> نامحدود</span>\'}}</div></div>'}}
        <div class="link-btns">
          <button class="btn btn-g btn-sm" onclick="cp('${{esc(l.link_url)}}')"><i class="ti ti-copy"></i> کپی لینک</button>
          <button class="btn btn-g btn-sm" onclick="qrShow('${{esc(l.link_url)}}')"><i class="ti ti-qrcode"></i> QR</button>
        </div>
      </div>`;
    }});

    html += `</div>`;
    wrap.innerHTML = html;

  }}catch(e){{
    wrap.innerHTML='<div class="empty"><i class="ti ti-alert-triangle empty-icon" style="color:var(--red);opacity:.5"></i><p>خطا در بارگذاری اطلاعات</p></div>';
  }}
}}

async function unlock(){{
  const pw = document.getElementById('pw-inp')?.value;
  if(!pw) return;
  const r = await fetch('/api/public/sub/'+KEY+'?pw='+encodeURIComponent(pw));
  const d = await r.json();
  if(d.locked){{showToast('رمز اشتباه است!'); return;}}
  load();
}}

document.addEventListener('keydown',e=>{{if(e.key==='Enter')unlock()}});
load();
</script>
</body></html>"""

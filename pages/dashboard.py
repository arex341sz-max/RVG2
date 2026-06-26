try:
    from pages_legacy import DASHBOARD_HTML as HTML
except ImportError:
    HTML = r"""<!DOCTYPE html>
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
  --pink:#EC4899;--pink-bg:rgba(236,72,153,0.1);--pink-t:#F472B6;
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
  --pink:#DB2777;--pink-bg:rgba(219,39,119,0.08);--pink-t:#9D174D;
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
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 6px}
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
.logout-btn:hover{background:rgba(239,68,68,.2)}
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
.bg-pink{background:var(--pink-bg);color:var(--pink-t)}
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
.proto-tag{font-size:9px;padding:2px 7px;border-radius:5px;font-weight:700;display:inline-flex;align-items:center;gap:3px;letter-spacing:.03em}
.pt-vless{background:rgba(59,130,246,0.12);color:#60A5FA}
.pt-trojan{background:rgba(16,185,129,0.12);color:#34D399}
.pt-hysteria2{background:rgba(245,158,11,0.12);color:#FCD34D}
.pt-vmess{background:rgba(139,92,246,0.12);color:#A78BFA}
.pt-wireguard{background:rgba(236,72,153,0.12);color:#F472B6}
.stream-tag{font-size:8.5px;padding:1px 5px;border-radius:4px;font-weight:700;display:inline-block;margin-right:3px;text-transform:uppercase;letter-spacing:.04em;border:1px solid}
.st-tcp{color:var(--accent2);border-color:rgba(59,130,246,0.25)}
.st-ws{color:var(--green-t);border-color:rgba(16,185,129,0.25)}
.st-grpc{color:#A78BFA;border-color:rgba(139,92,246,0.25)}
.st-httpupgrade{color:var(--amber-t);border-color:rgba(245,158,11,0.25)}
.st-xhttp{color:var(--pink-t);border-color:rgba(236,72,153,0.25)}
.st-mkcp{color:var(--red-t);border-color:rgba(239,68,68,0.25)}
.st-quic{color:#FCD34D;border-color:rgba(245,158,11,0.25)}
.st-udp{color:#F472B6;border-color:rgba(236,72,153,0.25)}
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
.sub-meta-item{font-size:10.5px;color:var(--t3);display:flex;align-items:center;gap:4px;background:var(--accent-d);padding:3px 8px;border-radius:6px}
.sub-card-footer{display:flex;gap:6px;flex-wrap:wrap;padding-top:12px;border-top:1px solid var(--card-b)}
.pub-url-box{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.2);border-radius:8px;padding:10px 13px;display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.pub-url-text{font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA;word-break:break-all;flex:1}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:none;color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer}
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
.fg-check{display:flex;align-items:center;gap:6px;padding-top:14px}
.fg-check label{margin:0;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:11px;color:var(--t2);text-transform:none;letter-spacing:0;font-weight:500}
.fg-check input[type=checkbox]{accent-color:var(--accent);width:15px;height:15px}
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
    <div><div class="logo-name">codebox</div><div class="logo-sub">RVG Gateway · v10.0</div></div>
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
    <button class="theme-btn" id="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button>
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
  <div class="metrics" style="grid-template-columns:repeat(5,1fr)">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> WebSocket زنده</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">از کل</div></div>
    <div class="metric pur"><div class="m-icon pur"><i class="ti ti-folders"></i></div><div class="m-label">گروه‌های ساب</div><div class="m-val" id="m-subs">—</div><div class="m-sub">فعال</div></div>
    <div class="metric" id="m-xray-card"><div class="m-icon"><i class="ti ti-engine"></i></div><div class="m-label">Xray Core</div><div class="m-val" id="m-xray">—</div><div class="m-sub" id="m-xray-sub">در حال بررسی...</div></div>
  </div>
  <div class="vless-box">
    <div class="vl-header">
      <div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
      <span class="badge bg-blue" id="default-link-badge"><span class="dot db"></span> —</span>
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
    <div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع پروتکل</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال · سخت‌گیرانه</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> Multi-Protocol</span><span class="sr-v" style="color:var(--green-t)">● VLESS/Trojan/HY2/VMess/WG</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-folders"></i> Sub Groups</span><span class="sr-v" style="color:var(--green-t)">● فعال v10</span></div>
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
    <span class="df-text">codebox RVG Gateway v10.0 · Railway · 2025</span>
    <a class="df-link" href="https://t.me/CodeBoxo" target="_blank"><i class="ti ti-brand-telegram"></i> t.me/CodeBoxo</a>
  </div>
</section>
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ با پروتکل، استریم، سهمیه و انقضا</div></div>
    <div class="tb-right"><span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span></div>
  </div>
  <div class="card mb16">
    <div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ جدید</div>
    <div class="form-row" style="margin-bottom:10px">
      <div class="fg" style="flex:1;min-width:140px"><label>عنوان</label><input class="fi" id="nl-label" placeholder="مثلاً: کاربر علی" style="width:100%"></div>
      <div class="fg"><label>پروتکل</label>
        <select class="fs" id="nl-proto" onchange="onProtoChange()">
          <option value="siz10a">SIZ10A ⚡</option>
          <option value="vless">VLESS</option>
          <option value="trojan">Trojan</option>
          <option value="hysteria2">Hysteria2</option>
          <option value="vmess">VMess</option>
          <option value="wireguard">WireGuard</option>
        </select>
      </div>
      <div class="fg" id="nl-stream-fg"><label>مد استریم</label>
        <select class="fs" id="nl-stream" onchange="onStreamChange()"></select>
      </div>
      <div class="fg"><label>پورت</label><input class="fi" id="nl-port" type="number" placeholder="خودکار" style="width:90px"></div>
    </div>
    <div class="form-row" style="margin-bottom:10px">
      <div class="fg fg-check">
        <label><input type="checkbox" id="nl-tls" checked onchange="onTlsChange()"> TLS</label>
        <label id="nl-reality-wrap"><input type="checkbox" id="nl-reality" onchange="onRealityChange()"> Reality</label>
      </div>
      <div class="fg" id="nl-sni-fg" style="min-width:120px"><label>SNI</label><input class="fi" id="nl-sni" placeholder="خالی=دامنه" style="width:100%"></div>
      <div class="fg" id="nl-fp-fg"><label>Fingerprint</label>
        <select class="fs" id="nl-fp">
          <option value="chrome">Chrome</option>
          <option value="firefox">Firefox</option>
          <option value="safari">Safari</option>
          <option value="edge">Edge</option>
          <option value="random">Random</option>
        </select>
      </div>
    </div>
    <div id="nl-stream-params" style="margin-bottom:10px"></div>
    <div id="nl-reality-params" style="display:none;margin-bottom:10px">
      <div class="form-row">
        <div class="fg" style="flex:1"><label>Public Key</label><input class="fi" id="nl-r-pbk" placeholder="Reality PBK" style="width:100%"></div>
        <div class="fg" style="flex:1"><label>Short ID</label><input class="fi" id="nl-r-sid" placeholder="Reality SID" style="width:100%"></div>
        <div class="fg" style="min-width:120px"><label>Reality SNI</label><input class="fi" id="nl-r-sni" placeholder="خالی=دامنه" style="width:100%"></div>
      </div>
    </div>
    <div class="form-row" style="margin-bottom:10px">
      <div class="fg"><label>سهمیه</label><input class="fi" id="nl-val" type="number" min="0" step="0.1" placeholder="0=∞" style="width:110px"></div>
      <div class="fg"><label>واحد</label><select class="fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div>
      <div class="fg"><label>انقضا (روز)</label><input class="fi" id="nl-exp" type="number" min="0" step="1" placeholder="0=∞" style="width:100px"></div>
      <div class="fg"><label>گروه ساب</label><select class="fs" id="nl-sub"><option value="">— بدون گروه —</option></select></div>
      <div class="fg" style="flex:1;min-width:120px"><label>یادداشت</label><input class="fi" id="nl-note" placeholder="اختیاری" style="width:100%"></div>
      <button class="btn btn-p" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت</button>
    </div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>هر پروتکل فایل Xray جداگانه دارد · Hysteria2 خودکار QUIC/TLS · WireGuard خودکار UDP · VLESS/Trojan/VMess مد استریم قابل تغییر.</span></div>
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
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> پروتکل‌ها</span><span class="sr-v">VLESS/Trojan/HY2/VMess/WG</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> سشن</span><span class="sr-v">HttpOnly · 7 روز</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> UUID Auth سخت‌گیرانه</span><span class="sr-v" style="color:var(--green-t)">● فعال v10</span></div>
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
    <div class="cl amber" style="margin-top:0;margin-bottom:12px"><i class="ti ti-alert-triangle"></i><span>فقط UUID‌های ثبت‌شده و فعال (VLESS/WS) اتصال برقرار می‌کنند.</span></div>
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
      <div class="sr"><span class="sr-k"><i class="ti ti-versions"></i> نسخه</span><span class="sr-v">v10.0</span></div>
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
// ─── State ────────────────────────────────────────────────────────
let isDark = localStorage.getItem('rvg-theme') !== 'light';
let PROTO_DATA = null;
let currentProtoStreams = {};
let ALL_LINKS = [];
let ALL_SUBS = [];
let STATS = null;
let chart1 = null, chart2 = null, chart3 = null;
let wsTest = null;

// ─── Theme ────────────────────────────────────────────────────────
function applyTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  const icon = dark ? 'ti-sun' : 'ti-moon';
  const label = dark ? 'تم روشن' : 'تم تاریک';
  document.getElementById('theme-icon').className = 'ti ' + icon;
  document.getElementById('theme-label').textContent = label;
  const m = document.getElementById('theme-mob-icon');
  if (m) m.className = 'ti ' + icon;
  if (chart1) { chart1.options.scales.x.ticks.color = dark ? '#3D6B8E' : '#64748B'; chart1.options.scales.y.ticks.color = dark ? '#3D6B8E' : '#64748B'; chart1.update(); }
  if (chart3) { chart3.options.scales.x.ticks.color = dark ? '#3D6B8E' : '#64748B'; chart3.options.scales.y.ticks.color = dark ? '#3D6B8E' : '#64748B'; chart3.update(); }
}

function toggleTheme() {
  isDark = !isDark;
  localStorage.setItem('rvg-theme', isDark ? 'dark' : 'light');
  applyTheme(isDark);
}
applyTheme(isDark);

// ─── Helpers ──────────────────────────────────────────────────────
function toast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (type ? ' ' + type : '');
  setTimeout(() => t.classList.remove('show'), 2400);
}

function fmtB(b) {
  if (!b || b === 0) return '0 B';
  if (b < 1024) return b + ' B';
  if (b < 1024 ** 2) return (b / 1024).toFixed(1) + ' KB';
  if (b < 1024 ** 3) return (b / 1024 ** 2).toFixed(2) + ' MB';
  return (b / 1024 ** 3).toFixed(2) + ' GB';
}

function toFa(n) { return String(n).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]); }

function esc(s) {
  return String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function daysLeft(exp) {
  if (!exp) return null;
  return Math.ceil((new Date(exp) - Date.now()) / 864e5);
}

function expChip(exp, expired) {
  if (expired) return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if (!exp) return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> ∞</span>';
  const d = daysLeft(exp);
  if (d <= 0) return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if (d <= 3) return '<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ' + toFa(d) + 'ر</span>';
  return '<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ' + toFa(d) + 'ر</span>';
}

function protoTag(p) { return '<span class="proto-tag pt-' + (p||'vless') + '">' + (p||'vless').toUpperCase() + '</span>'; }

function streamTag(s) {
  const m = {'tcp':'TCP','ws':'WS','grpc':'gRPC','httpupgrade':'HUP','xhttp':'XHTTP','mkcp':'mKCP','quic':'QUIC','udp':'UDP'};
  return '<span class="stream-tag st-' + (s||'tcp') + '">' + (m[s] || s || 'TCP') + '</span>';
}

function statusBadge(l) {
  if (!l.active) return '<span class="badge bg-red"><span class="dot dr"></span> غیرفعال</span>';
  if (l.expired) return '<span class="badge bg-amber"><span class="dot da"></span> منقضی</span>';
  if (l.limit_bytes > 0 && l.used_bytes >= l.limit_bytes) return '<span class="badge bg-red"><span class="dot dr"></span> اتمام سهمیه</span>';
  return '<span class="badge bg-green"><span class="dot dg"></span> فعال</span>';
}

function usageBar(l) {
  const lb = l.limit_bytes || 0, ub = l.used_bytes || 0;
  if (lb === 0) return '<div class="utxt">' + fmtB(ub) + ' / ∞</div>';
  const pct = Math.min(100, ((ub / lb) * 100)).toFixed(1);
  const c = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
  return '<div class="ubar"><div class="ubar-f" style="width:' + pct + '%;background:' + c + '"></div></div><div class="utxt">' + fmtB(ub) + ' / ' + fmtB(lb) + ' (' + toFa(pct) + '%)</div>';
}

// ─── Copy / QR ───────────────────────────────────────────────────
// ✅ اصلاح شده: استفاده از data attribute به جای inline string
function cpText(elId, text) {
  const t = text || (document.getElementById(elId) ? document.getElementById(elId).textContent : '') || '';
  if (!t) { toast('لینک خالی است', 'err'); return; }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(t).then(() => toast('کپی شد', 'ok')).catch(() => _fallbackCopy(t));
  } else {
    _fallbackCopy(t);
  }
}
function _fallbackCopy(t) {
  try {
    const ta = document.createElement('textarea');
    ta.value = t;
    ta.style.cssText = 'position:fixed;top:-999px;left:-999px;opacity:0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    ok ? toast('کپی شد', 'ok') : toast('خطا در کپی', 'err');
  } catch(e) { toast('خطا در کپی', 'err'); }
}

function cpSubAll() { cpText(null, document.getElementById('sub-all-url').textContent); }

// ✅ اصلاح شده: QR از data-link attribute خوانده میشه - بدون inline JS string
function qrFor(elId, text) {
  const t = text || (document.getElementById(elId) ? document.getElementById(elId).textContent : '') || '';
  if (!t) return;
  let qr = document.getElementById('qr-modal');
  if (qr) qr.remove();
  const bg = document.createElement('div');
  bg.id = 'qr-modal';
  bg.className = 'modal-bg open';
  bg.style.zIndex = '600';
  const modal = document.createElement('div');
  modal.className = 'modal';
  modal.style.cssText = 'text-align:center;padding:24px';
  const closeBtn = document.createElement('button');
  closeBtn.className = 'modal-close';
  closeBtn.innerHTML = '<i class="ti ti-x"></i>';
  closeBtn.onclick = () => bg.remove();
  const title = document.createElement('div');
  title.className = 'modal-title';
  title.style.justifyContent = 'center';
  title.innerHTML = '<i class="ti ti-qrcode"></i> QR Code';
  const img = document.createElement('img');
  img.src = 'https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=' + encodeURIComponent(t);
  img.style.cssText = 'border-radius:12px;margin:16px 0';
  const copyBtn = document.createElement('button');
  copyBtn.className = 'btn btn-p';
  copyBtn.style.cssText = 'width:100%;justify-content:center;margin-top:12px';
  copyBtn.innerHTML = '<i class="ti ti-copy"></i> کپی لینک';
  copyBtn.onclick = () => cpText(null, t);
  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(img);
  modal.appendChild(copyBtn);
  bg.appendChild(modal);
  bg.onclick = e => { if (e.target === bg) bg.remove(); };
  document.body.appendChild(bg);
}

// ─── Proto / Stream Form ──────────────────────────────────────────
async function loadProtocols() {
  try {
    const r = await fetch('/api/protocols');
    PROTO_DATA = (await r.json()).protocols;
  } catch(e) { console.error('loadProtocols:', e); }
  onProtoChange();
}

function onProtoChange() {
  const proto = document.getElementById('nl-proto').value;
  const info = PROTO_DATA?.[proto];
  if (!info) return;
  const sel = document.getElementById('nl-stream');
  sel.innerHTML = '';
  currentProtoStreams = info.stream_modes || {};
  for (const [k, m] of Object.entries(currentProtoStreams)) {
    const o = document.createElement('option');
    o.value = k; o.textContent = m.label; sel.appendChild(o);
  }
  const tlsCb = document.getElementById('nl-tls');
  const rw = document.getElementById('nl-reality-wrap');
  const sf = document.getElementById('nl-stream-fg');
  const sniFg = document.getElementById('nl-sni-fg');
  const fpFg = document.getElementById('nl-fp-fg');
  if (!info.supports_tls) {
    tlsCb.checked = false; tlsCb.disabled = true; rw.style.display = 'none';
    sf.style.display = 'none'; sniFg.style.display = 'none'; fpFg.style.display = 'none';
  } else {
    tlsCb.checked = info.default_tls; tlsCb.disabled = false;
    rw.style.display = info.supports_reality ? '' : 'none';
    sf.style.display = ''; sniFg.style.display = ''; fpFg.style.display = '';
  }
  document.getElementById('nl-reality').checked = false;
  document.getElementById('nl-reality-params').style.display = 'none';
  const portInp = document.getElementById('nl-port');
  if (!portInp.value) {
    if (proto === 'hysteria2') portInp.value = '8443';
    else if (proto === 'wireguard') portInp.value = '51820';
    else if (info.default_tls) portInp.value = '443';
    else portInp.value = '80';
  }
  onStreamChange(); onTlsChange();
}

function onStreamChange() {
  const stream = document.getElementById('nl-stream').value;
  const mode = currentProtoStreams[stream];
  const c = document.getElementById('nl-stream-params');
  c.innerHTML = '';
  if (!mode || !mode.params || mode.params.length === 0) return;
  const row = document.createElement('div');
  row.className = 'form-row';
  for (const p of mode.params) {
    const fg = document.createElement('div');
    fg.className = 'fg'; fg.style.flex = '1'; fg.style.minWidth = '120px';
    const lbl = document.createElement('label');
    lbl.textContent = p.label; fg.appendChild(lbl);
    if (p.type === 'bool') {
      const cb = document.createElement('input');
      cb.type = 'checkbox'; cb.id = 'nl-sp-' + p.key; cb.checked = !!p.default; cb.style.marginTop = '4px';
      fg.appendChild(cb);
    } else if (p.type === 'select') {
      const s = document.createElement('select');
      s.className = 'fs'; s.id = 'nl-sp-' + p.key; s.style.width = '100%';
      for (const opt of (p.options || [])) {
        const o = document.createElement('option'); o.value = opt; o.textContent = opt;
        if (opt === p.default) o.selected = true; s.appendChild(o);
      }
      fg.appendChild(s);
    } else {
      const inp = document.createElement('input');
      inp.className = 'fi'; inp.id = 'nl-sp-' + p.key;
      inp.placeholder = p.placeholder || ''; inp.value = p.default || ''; inp.style.width = '100%';
      fg.appendChild(inp);
    }
    row.appendChild(fg);
  }
  c.appendChild(row);
}

function onTlsChange() {
  if (!document.getElementById('nl-tls').checked) {
    document.getElementById('nl-reality').checked = false;
    document.getElementById('nl-reality-params').style.display = 'none';
  }
}

function onRealityChange() {
  const on = document.getElementById('nl-reality').checked;
  document.getElementById('nl-reality-params').style.display = on ? '' : 'none';
  if (on) {
    document.getElementById('nl-tls').checked = true;
    document.getElementById('nl-sni-fg').style.display = 'none';
    document.getElementById('nl-fp-fg').style.display = '';
  } else {
    document.getElementById('nl-sni-fg').style.display = '';
  }
}

function getStreamParams() {
  const sp = {};
  const mode = currentProtoStreams[document.getElementById('nl-stream').value];
  if (mode && mode.params) {
    for (const p of mode.params) {
      const el = document.getElementById('nl-sp-' + p.key);
      if (!el) continue;
      if (p.type === 'bool') sp[p.key] = el.checked;
      else sp[p.key] = el.value;
    }
  }
  return sp;
}

// ─── Link CRUD ────────────────────────────────────────────────────
async function createLink() {
  const body = {
    protocol: document.getElementById('nl-proto').value,
    stream: document.getElementById('nl-stream').value,
    tls: document.getElementById('nl-tls').checked,
    stream_params: getStreamParams(),
    label: document.getElementById('nl-label').value,
    port: parseInt(document.getElementById('nl-port').value) || 0,
    sni: document.getElementById('nl-sni').value,
    fingerprint: document.getElementById('nl-fp').value,
    reality: document.getElementById('nl-reality').checked,
    reality_pbk: document.getElementById('nl-r-pbk').value,
    reality_sid: document.getElementById('nl-r-sid').value,
    reality_sni: document.getElementById('nl-r-sni').value,
    reality_fingerprint: document.getElementById('nl-fp').value,
    limit_value: document.getElementById('nl-val').value,
    limit_unit: document.getElementById('nl-unit').value,
    expires_days: document.getElementById('nl-exp').value,
    sub_id: document.getElementById('nl-sub').value || null,
    note: document.getElementById('nl-note').value,
  };
  try {
    const r = await fetch('/api/links', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
      body: JSON.stringify(body)
    });
    if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error(d.detail || 'خطا'); }
    toast('کانفیگ ساخته شد', 'ok');
    refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

async function toggleLink(uid, val) {
  try {
    await fetch('/api/links/' + uid, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
      body: JSON.stringify({active: val})
    });
    toast(val ? 'فعال شد' : 'غیرفعال شد', 'ok');
    refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

async function deleteLink(uid) {
  if (!confirm('حذف این کانفیگ؟')) return;
  try {
    await fetch('/api/links/' + uid, {method: 'DELETE', credentials: 'include'});
    toast('حذف شد', 'ok'); refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

async function resetUsage(uid) {
  try {
    await fetch('/api/links/' + uid, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
      body: JSON.stringify({reset_usage: true})
    });
    toast('ریست شد', 'ok'); refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

// ─── Sub CRUD ─────────────────────────────────────────────────────
async function createSub() {
  const body = {
    name: document.getElementById('ns-name').value,
    desc: document.getElementById('ns-desc').value,
    password: document.getElementById('ns-pw').value
  };
  try {
    const r = await fetch('/api/subs', {method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include', body: JSON.stringify(body)});
    if (!r.ok) throw new Error('خطا');
    toast('گروه ساخته شد', 'ok');
    closeModal('modal-create-sub');
    document.getElementById('ns-name').value = '';
    document.getElementById('ns-desc').value = '';
    document.getElementById('ns-pw').value = '';
    refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

async function deleteSub(sid) {
  if (!confirm('حذف این گروه؟')) return;
  try {
    await fetch('/api/subs/' + sid, {method: 'DELETE', credentials: 'include'});
    toast('حذف شد', 'ok'); refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

let modalSubId = '', modalSubLinks = [];
function openSubLinks(sid, name, linkIds) {
  modalSubId = sid; modalSubLinks = [...linkIds];
  document.getElementById('modal-sub-name').textContent = name;
  renderModalLinks(); openModal('modal-links');
}

function renderModalLinks() {
  const c = document.getElementById('modal-links-body');
  if (!ALL_LINKS.length) { c.innerHTML = '<p style="color:var(--t3);font-size:12px">کانفیگی وجود ندارد</p>'; return; }
  c.innerHTML = ALL_LINKS.map(l => {
    const checked = modalSubLinks.includes(l.uuid) ? 'checked' : '';
    return '<div class="lrow"><input type="checkbox" class="lrow-check" data-uid="' + l.uuid + '" ' + checked + '><span class="lrow-label">' + protoTag(l.protocol) + ' ' + streamTag(l.stream) + ' ' + esc(l.label) + '</span><span class="lrow-badge">' + (l.active ? 'فعال' : 'غیرفعال') + '</span></div>';
  }).join('');
}

async function saveSubLinks() {
  const checks = document.querySelectorAll('#modal-links-body .lrow-check');
  const ids = [];
  checks.forEach(c => { if (c.checked) ids.push(c.dataset.uid); });
  try {
    const current = ALL_SUBS.find(s => s.sub_id === modalSubId);
    const curIds = current ? (current.link_ids || []) : [];
    for (const id of ids) {
      if (!curIds.includes(id)) await fetch('/api/subs/' + modalSubId + '/links', {method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include', body: JSON.stringify({link_id: id, action: 'add'})});
    }
    for (const id of curIds) {
      if (!ids.includes(id)) await fetch('/api/subs/' + modalSubId + '/links', {method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include', body: JSON.stringify({link_id: id, action: 'remove'})});
    }
    toast('ذخیره شد', 'ok'); closeModal('modal-links'); refreshAll();
  } catch(e) { toast(e.message, 'err'); }
}

// ─── Modals / Nav ────────────────────────────────────────────────
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

function navTo(pg) {
  document.querySelectorAll('.pg').forEach(p => p.classList.remove('on'));
  const target = document.getElementById('pg-' + pg);
  if (target) target.classList.add('on');
  document.querySelectorAll('.nav-it').forEach(n => n.classList.remove('on'));
  const navItem = document.querySelector('.nav-it[data-pg="' + pg + '"]');
  if (navItem) navItem.classList.add('on');
  document.getElementById('overlay').classList.remove('show');
  document.getElementById('sb').classList.remove('open');
}

// ─── Auth ────────────────────────────────────────────────────────
async function checkAuth() {
  try {
    const r = await fetch('/api/me', {credentials: 'include'});
    const d = await r.json();
    if (!d.authenticated) location.href = '/login';
  } catch(e) { location.href = '/login'; }
}

async function logout() {
  try { await fetch('/api/logout', {method: 'POST', credentials: 'include'}); } catch(e) {}
  location.href = '/login';
}

async function changePw() {
  const cur = document.getElementById('cp-cur').value;
  const nw = document.getElementById('cp-new').value;
  const cf = document.getElementById('cp-cf').value;
  if (nw !== cf) { toast('رمز جدید و تکرار مطابقت ندارند', 'err'); return; }
  if (nw.length < 4) { toast('رمز جدید حداقل ۴ کاراکتر', 'err'); return; }
  try {
    const r = await fetch('/api/change-password', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include',
      body: JSON.stringify({current_password: cur, new_password: nw})
    });
    if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error(d.detail || 'خطا'); }
    toast('رمز تغییر کرد', 'ok');
    document.getElementById('cp-cur').value = '';
    document.getElementById('cp-new').value = '';
    document.getElementById('cp-cf').value = '';
  } catch(e) { toast(e.message, 'err'); }
}

// ─── WS Test ─────────────────────────────────────────────────────
function wsLog(msg, color) {
  const l = document.getElementById('ws-log');
  const p = document.createElement('p');
  p.style.color = color || 'var(--t2)';
  p.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
  l.appendChild(p); l.scrollTop = l.scrollHeight;
}
function wsConn() {
  const uid = document.getElementById('ws-uuid').value.trim();
  if (!uid) { toast('UUID وارد کنید', 'err'); return; }
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = proto + '//' + location.host + '/ws/' + uid;
  try {
    wsTest = new WebSocket(url);
    wsLog('اتصال...', 'var(--amber)');
    wsTest.onopen = () => wsLog('متصل شد', 'var(--green-t)');
    wsTest.onmessage = e => wsLog('← ' + e.data);
    wsTest.onclose = e => wsLog('قطع شد: ' + e.code + ' ' + e.reason, 'var(--red-t)');
    wsTest.onerror = () => wsLog('خطا', 'var(--red-t)');
  } catch(e) { wsLog('خطا: ' + e.message, 'var(--red-t)'); }
}
function wsDisc() { if (wsTest) { wsTest.close(); wsTest = null; wsLog('درخواست قطع', 'var(--amber)'); } }
function wsSend() {
  if (!wsTest || wsTest.readyState !== 1) { toast('اتصال برقرار نیست', 'err'); return; }
  const m = document.getElementById('ws-msg').value;
  if (!m) return;
  wsTest.send(m); wsLog('→ ' + m, 'var(--accent2)');
  document.getElementById('ws-msg').value = '';
}

// ─── Charts ──────────────────────────────────────────────────────
function initCharts() {
  const gridC = isDark ? 'rgba(59,130,246,0.06)' : 'rgba(59,130,246,0.08)';
  const tickC = isDark ? '#3D6B8E' : '#64748B';
  chart1 = new Chart(document.getElementById('ch1'), {type:'line',data:{labels:[],datasets:[{label:'MB',data:[],borderColor:'#3B82F6',backgroundColor:'rgba(59,130,246,0.1)',fill:true,tension:.4,pointRadius:0,borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:gridC},ticks:{color:tickC,font:{size:9}}},y:{grid:{color:gridC},ticks:{color:tickC,font:{size:9}}}}}});
  chart2 = new Chart(document.getElementById('ch2'), {type:'doughnut',data:{labels:[],datasets:[{data:[],backgroundColor:['#3B82F6','#10B981','#F59E0B','#8B5CF6','#EC4899'],borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{color:tickC,font:{size:10},padding:8,usePointStyle:true,pointStyleWidth:8}}},cutout:'65%'}});
  chart3 = new Chart(document.getElementById('ch3'), {type:'bar',data:{labels:[],datasets:[{label:'MB',data:[],backgroundColor:'rgba(59,130,246,0.3)',borderColor:'#3B82F6',borderWidth:1,borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:gridC},ticks:{color:tickC,font:{size:9}}},y:{grid:{color:gridC},ticks:{color:tickC,font:{size:9}}}}}});
}

// ─── Render ──────────────────────────────────────────────────────
// ✅ اصلاح شده: دکمه‌های جدول از data attribute استفاده می‌کنن - بدون inline string
function renderLinks() {
  const tb = document.getElementById('links-tb');
  if (!ALL_LINKS.length) {
    tb.innerHTML = '';
    document.getElementById('links-empty').style.display = 'block';
    return;
  }
  document.getElementById('links-empty').style.display = 'none';
  tb.innerHTML = ALL_LINKS.map(l => {
    const tlsTag = l.tls ? '<span class="stream-tag st-tcp" style="color:var(--green-t);border-color:rgba(16,185,129,0.25)">TLS</span>' : '';
    const realityTag = l.reality ? '<span class="stream-tag st-mkcp" style="font-size:7.5px">REALITY</span>' : '';
    return '<tr>' +
      '<td><div class="ll">' + esc(l.label) + '</div><div class="lm">' + protoTag(l.protocol) + ' ' + streamTag(l.stream) + ' ' + tlsTag + ' ' + realityTag + ' ' + esc(l.note) + '</div></td>' +
      '<td><span class="uuid-chip" data-uid="' + esc(l.uuid) + '" title="کپی UUID">' + l.uuid.substring(0, 18) + '…</span></td>' +
      '<td>' + usageBar(l) + '</td>' +
      '<td>' + (l.sub_id ? '<span class="badge bg-purple" style="font-size:9px">گروه</span>' : '—') + '</td>' +
      '<td>' + expChip(l.expires_at, l.expired) + '</td>' +
      '<td>' + statusBadge(l) + '</td>' +
      '<td style="white-space:nowrap">' +
        '<button class="btn btn-sm btn-g" data-action="copy" data-link="' + esc(l.link_url||'') + '" title="کپی لینک"><i class="ti ti-copy"></i></button>' +
        '<button class="btn btn-sm btn-g" data-action="qr" data-link="' + esc(l.link_url||'') + '" title="QR"><i class="ti ti-qrcode"></i></button>' +
        '<button class="btn btn-sm btn-g" data-action="sub" data-uid="' + esc(l.uuid) + '" title="سابسکریپشن"><i class="ti ti-rss"></i></button>' +
        '<button class="btn btn-sm btn-o" data-action="toggle" data-uid="' + esc(l.uuid) + '" data-active="' + (l.active?'1':'0') + '" title="' + (l.active?'غیرفعال':'فعال') + '"><i class="ti ti-' + (l.active?'player-pause':'player-play') + '"></i></button>' +
        '<button class="btn btn-sm btn-o" data-action="reset" data-uid="' + esc(l.uuid) + '" title="ریست مصرف"><i class="ti ti-refresh"></i></button>' +
        '<button class="btn btn-sm btn-d" data-action="delete" data-uid="' + esc(l.uuid) + '"><i class="ti ti-trash"></i></button>' +
      '</td>' +
    '</tr>';
  }).join('');

  // ✅ Event delegation — یک listener برای کل جدول
  tb.onclick = function(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    const uid = btn.dataset.uid;
    const link = btn.dataset.link;
    if (action === 'copy') cpText(null, link);
    else if (action === 'qr') qrFor(null, link);
    else if (action === 'sub') window.open('/sub/' + uid);
    else if (action === 'toggle') toggleLink(uid, btn.dataset.active !== '1');
    else if (action === 'reset') resetUsage(uid);
    else if (action === 'delete') deleteLink(uid);
    // کپی UUID
    const chip = e.target.closest('.uuid-chip');
    if (chip) cpText(null, chip.dataset.uid);
  };
}

function renderSubs() {
  const g = document.getElementById('subs-grid');
  if (!ALL_SUBS.length) {
    g.innerHTML = '<div class="empty" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>';
    return;
  }
  g.innerHTML = ALL_SUBS.map(s =>
    '<div class="sub-card">' +
      '<div class="sub-card-head"><div><div class="sub-card-name">' + esc(s.name) + '</div><div class="sub-card-desc">' + esc(s.desc) + '</div></div>' +
      '<button class="btn btn-sm btn-d" data-action="del-sub" data-sid="' + esc(s.sub_id) + '"><i class="ti ti-trash"></i></button></div>' +
      '<div class="sub-card-meta">' +
        '<span class="sub-meta-item"><i class="ti ti-link"></i> ' + toFa(s.links_count) + ' لینک</span>' +
        '<span class="sub-meta-item"><i class="ti ti-circle-check"></i> ' + toFa(s.active_count) + ' فعال</span>' +
        '<span class="sub-meta-item"><i class="ti ti-database"></i> ' + s.total_used_fmt + '</span>' +
        (s.has_password ? '<span class="sub-meta-item"><i class="ti ti-lock"></i> رمزدار</span>' : '') +
      '</div>' +
      '<div class="sub-card-footer">' +
        '<button class="btn btn-sm btn-pur" data-action="manage-sub" data-sid="' + esc(s.sub_id) + '" data-name="' + esc(s.name) + '" data-ids="' + esc(JSON.stringify(s.link_ids||[])) + '"><i class="ti ti-link-plus"></i> مدیریت لینک‌ها</button>' +
        '<button class="btn btn-sm btn-g" data-action="copy-sub" data-url="' + esc(s.sub_url) + '"><i class="ti ti-copy"></i></button>' +
        '<button class="btn btn-sm btn-o" data-action="open-pub" data-url="' + esc(s.public_url) + '"><i class="ti ti-external-link"></i> صفحه</button>' +
      '</div>' +
    '</div>'
  ).join('');

  g.onclick = function(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    if (action === 'del-sub') deleteSub(btn.dataset.sid);
    else if (action === 'manage-sub') openSubLinks(btn.dataset.sid, btn.dataset.name, JSON.parse(btn.dataset.ids || '[]'));
    else if (action === 'copy-sub') cpText(null, btn.dataset.url);
    else if (action === 'open-pub') window.open(btn.dataset.url, '_blank');
  };
}

function renderSubGroupsList() {
  const c = document.getElementById('sub-groups-list');
  if (!ALL_SUBS.length) { c.innerHTML = '<p style="color:var(--t3);font-size:12px">گروهی وجود ندارد</p>'; return; }
  c.innerHTML = ALL_SUBS.map(s =>
    '<div class="pub-url-box" style="margin-bottom:8px">' +
      '<div style="flex:1"><div style="font-size:11px;font-weight:600;color:var(--t1);margin-bottom:4px">' + esc(s.name) + (s.has_password ? ' <i class="ti ti-lock" style="font-size:11px;color:var(--amber)"></i>' : '') + '</div>' +
      '<div class="pub-url-text">' + esc(s.sub_url) + '</div></div>' +
      '<div style="display:flex;gap:4px"><button class="btn btn-sm btn-g" data-action="copy-sub-url" data-url="' + esc(s.sub_url) + '"><i class="ti ti-copy"></i></button></div>' +
    '</div>'
  ).join('');
  c.onclick = function(e) {
    const btn = e.target.closest('[data-action]');
    if (btn && btn.dataset.action === 'copy-sub-url') cpText(null, btn.dataset.url);
  };
}

function renderSubSelect() {
  const sel = document.getElementById('nl-sub');
  const cur = sel.value;
  sel.innerHTML = '<option value="">— بدون گروه —</option>';
  ALL_SUBS.forEach(s => {
    const o = document.createElement('option'); o.value = s.sub_id; o.textContent = s.name; sel.appendChild(o);
  });
  if (cur && ALL_SUBS.find(s => s.sub_id === cur)) sel.value = cur;
}

function renderOverview(s, l) {
  try {
    document.getElementById('m-conns').textContent = toFa(s.active_connections);
    document.getElementById('m-traffic').innerHTML = toFa(s.total_traffic_mb) + '<span class="m-unit">MB</span>';
    document.getElementById('m-alinks').textContent = toFa(s.active_links);
    document.getElementById('m-lsub').textContent = 'از ' + toFa(s.links_count);
    document.getElementById('m-subs').textContent = toFa(s.subs_count);
    document.getElementById('uptime-badge').textContent = s.uptime;
    document.getElementById('uptime-inline').textContent = s.uptime;
    document.getElementById('last-upd').textContent = 'آپدیت آخر: ' + new Date(s.timestamp).toLocaleTimeString('fa-IR');
    document.getElementById('links-nb').textContent = s.links_count;
    document.getElementById('subs-nb').textContent = s.subs_count;
    document.getElementById('conns-nb').textContent = s.active_connections;
    document.getElementById('links-pg-cnt').textContent = toFa(s.links_count) + ' کانفیگ';
    document.getElementById('subs-pg-cnt').textContent = toFa(s.subs_count) + ' گروه';
    document.getElementById('conns-live').textContent = toFa(s.active_connections) + ' فعال';

    const mxray = document.getElementById('m-xray');
    const mxraysub = document.getElementById('m-xray-sub');
    if (mxray) {
      if (s.xray && s.xray.running) {
        mxray.innerHTML = '<span style="color:var(--green-t)">فعال</span>';
        if (mxraysub) mxraysub.textContent = 'PID ' + s.xray.pid;
      } else {
        mxray.innerHTML = '<span style="color:var(--red-t)">متوقف</span>';
        if (mxraysub) mxraysub.textContent = 'restart خودکار...';
      }
    }

    const defLink = l.find(x => x.is_default);
    if (defLink) {
      document.getElementById('vless-main').textContent = defLink.link_url || '—';
      document.getElementById('default-link-badge').innerHTML = '<span class="dot db"></span> ' + protoTag(defLink.protocol) + ' ' + streamTag(defLink.stream) + ' ' + (defLink.tls ? 'TLS ' : '') + ':' + (defLink.port || 443);
    }

    const pc = s.protocol_counts || {};
    const summaryEl = document.getElementById('lsummary');
    summaryEl.innerHTML = Object.entries(pc).map(([p, c]) =>
      '<div class="sr"><span class="sr-k">' + protoTag(p) + '</span><span class="sr-v">' + toFa(c) + ' کانفیگ</span></div>'
    ).join('') || '<div class="sr"><span class="sr-k" style="color:var(--t3)">—</span><span class="sr-v">—</span></div>';
    document.getElementById('lsummary-badge').textContent = toFa(s.links_count);

    const hours = Object.keys(s.hourly || {}).sort();
    const hVals = hours.map(h => ((s.hourly[h] || 0) / (1024 * 1024)).toFixed(2));
    chart1.data.labels = hours.map(h => h.replace(':00', ''));
    chart1.data.datasets[0].data = hVals; chart1.update('none');
    chart2.data.labels = Object.keys(pc).map(p => p.toUpperCase());
    chart2.data.datasets[0].data = Object.values(pc); chart2.update('none');

    const totalMB = s.total_traffic_mb || 0;
    document.getElementById('t-traffic').innerHTML = totalMB.toFixed(2) + '<span class="m-unit">MB</span>';
    const avgH = hours.length ? (hVals.reduce((a, b) => a + parseFloat(b), 0) / hours.length).toFixed(2) : '0';
    const peakH = hVals.length ? Math.max(...hVals.map(Number)).toFixed(2) : '0';
    document.getElementById('t-avg').innerHTML = avgH + '<span class="m-unit">MB</span>';
    document.getElementById('t-peak').innerHTML = peakH + '<span class="m-unit">MB</span>';
    chart3.data.labels = hours.map(h => h.replace(':00', ''));
    chart3.data.datasets[0].data = hVals; chart3.update('none');

    const connsList = document.getElementById('conns-list');
    const connsEmpty = document.getElementById('conns-empty');
    if (s.active_connections === 0) {
      connsList.innerHTML = ''; connsEmpty.style.display = '';
    } else {
      connsEmpty.style.display = 'none';
      connsList.innerHTML = '<div class="sr"><span class="sr-k"><i class="ti ti-plug-connected"></i> تعداد اتصالات</span><span class="sr-v" style="color:var(--green-t)">' + toFa(s.active_connections) + ' فعال</span></div>';
    }

    const errs = s.recent_errors || [];
    document.getElementById('errs-badge').textContent = toFa(errs.length);
    const errsEl = document.getElementById('errs-full');
    if (!errs.length) errsEl.innerHTML = '<div class="empty"><i class="ti ti-mood-happy"></i><p>خطایی ثبت نشده</p></div>';
    else errsEl.innerHTML = errs.map(e => '<div class="erow"><div class="etime"><i class="ti ti-clock"></i> ' + (e.time||'') + '</div><div class="emsg">' + esc(e.error) + '</div></div>').join('');

    document.getElementById('set-host').textContent = location.host;
    document.getElementById('sub-all-url').textContent = location.protocol + '//' + location.host + '/sub-all';

    const bw = Math.min(100, Math.random() * 30 + 5);
    document.getElementById('bw-pct').textContent = toFa(bw.toFixed(0)) + '%';
    document.getElementById('bw-bar').style.width = bw + '%';
  } catch(err) { console.error('renderOverview error:', err); }
}

// ─── Refresh ─────────────────────────────────────────────────────
async function refreshAll() {
  try {
    const [sR, lR, subR] = await Promise.all([
      fetch('/stats', {credentials: 'include'}),
      fetch('/api/links', {credentials: 'include'}),
      fetch('/api/subs', {credentials: 'include'})
    ]);
    if (sR.status === 401 || lR.status === 401 || subR.status === 401) return location.href = '/login';
    if (!sR.ok || !lR.ok || !subR.ok) throw new Error('خطا در دریافت اطلاعات');
    const [statsJson, linksJson, subsJson] = await Promise.all([sR.json(), lR.json(), subR.json()]);
    STATS = statsJson;
    ALL_LINKS = linksJson.links || [];
    ALL_SUBS = subsJson.subs || [];
    renderLinks(); renderSubs(); renderSubGroupsList(); renderSubSelect(); renderOverview(STATS, ALL_LINKS);
  } catch(e) {
    console.error('refreshAll error:', e);
    toast('خطا در بارگذاری: ' + e.message, 'err');
  }
}

// ─── Init ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  try { await checkAuth(); } catch(e) { return; }
  document.querySelectorAll('.nav-it[data-pg]').forEach(n => n.addEventListener('click', () => navTo(n.dataset.pg)));
  try { await loadProtocols(); } catch(e) { console.error('loadProtocols error:', e); }
  try { initCharts(); } catch(e) { console.error('initCharts error:', e); }
  document.getElementById('open-sb').addEventListener('click', () => { document.getElementById('sb').classList.add('open'); document.getElementById('overlay').classList.add('show'); });
  document.getElementById('close-sb').addEventListener('click', () => { document.getElementById('sb').classList.remove('open'); document.getElementById('overlay').classList.remove('show'); });
  document.getElementById('overlay').addEventListener('click', () => { document.getElementById('sb').classList.remove('open'); document.getElementById('overlay').classList.remove('show'); });
  document.getElementById('logout-btn').addEventListener('click', logout);
  refreshAll();
  setInterval(refreshAll, 15000);
});
</script>
</body></html>"""

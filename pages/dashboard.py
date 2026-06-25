# pages/dashboard.py
# محتوای DASHBOARD_HTML از pages.py قبلی رو اینجا paste کن:
# HTML = DASHBOARD_HTML

# همون HTML کامل قبلی — فقط یه بخش کوچک اضافه شده برای Xray status:
# در بخش داشبورد، بعد از metric های موجود این رو اضافه کن:
#
#   <div class="metric">
#     <div class="m-icon"><i class="ti ti-cpu"></i></div>
#     <div class="m-label">Xray Core</div>
#     <div class="m-val" id="m-xray">—</div>
#     <div class="m-sub" id="m-xray-sub">—</div>
#   </div>
#
# و در تابع renderOverview:
#   if(s.xray?.running) {
#     document.getElementById('m-xray').innerHTML = '<span style="color:var(--green-t)">فعال</span>';
#     document.getElementById('m-xray-sub').textContent = 'PID ' + s.xray.pid;
#   } else {
#     document.getElementById('m-xray').innerHTML = '<span style="color:var(--red-t)">متوقف</span>';
#     document.getElementById('m-xray-sub').textContent = 'restart خودکار...';
#   }

# فعلاً از pages.py قدیمی import می‌کنیم:
try:
    from pages_legacy import DASHBOARD_HTML as HTML
except ImportError:
    HTML = "<h1 style='font-family:sans-serif;padding:40px;color:#fff;background:#060f1d;min-height:100vh'>Dashboard — فایل pages/dashboard.py را کامل کنید</h1>"

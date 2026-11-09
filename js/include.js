/* ============================================================
   include.js —— 纯静态站的组件引入（无构建工具）
   用法：
     <div data-include="components/header.html"></div>
     <div data-include="components/footer.html"></div>
   原理：fetch 取片段 → 替换占位 div → 再执行一次脚本初始化。
   注意：fetch 需要 http(s)，直接双击 file:// 打开会被浏览器拦。
        本地预览：在项目根目录跑 `python -m http.server 8000`，
        然后访问 http://localhost:8000
   ============================================================ */
(function () {
  'use strict';

  function loadInto(el) {
    var src = el.getAttribute('data-include');
    if (!src) return Promise.resolve();

    return fetch(src, { cache: 'no-cache' })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
        return res.text();
      })
      .then(function (html) {
        el.innerHTML = html;
        // 片段里也可能带 <script>，innerHTML 不会执行，这里手动补一遍
        var scripts = el.querySelectorAll('script');
        for (var i = 0; i < scripts.length; i += 1) {
          var s = document.createElement('script');
          if (scripts[i].src) s.src = scripts[i].src;
          else s.textContent = scripts[i].textContent;
          document.body.appendChild(s);
        }
      })
      .catch(function (err) {
        el.innerHTML =
          '<div style="padding:12px 16px;margin:12px auto;max-width:1120px;' +
          'border:1px dashed #8A94A3;border-radius:12px;color:#8A94A3;' +
          'font:14px/1.7 system-ui;text-align:center">' +
          '组件 ' + src + ' 没加载出来（' + err.message + '）。' +
          '这通常是因为用 file:// 直接打开了页面，请用本地 http 服务预览。' +
          '</div>';
      });
  }

  function boot() {
    var slots = Array.prototype.slice.call(
      document.querySelectorAll('[data-include]')
    );
    Promise.all(slots.map(loadInto)).then(function () {
      document.dispatchEvent(new CustomEvent('includes:ready'));
      // 引入完成后再初始化通用脚本（它自己也会在 DOMContentLoaded 时跑一次）
      if (window.__commonBoot) window.__commonBoot();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();

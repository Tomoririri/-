/* ============================================================
   common.js —— 全站共享脚本库
   个人介绍静态主页 · 任务二「组件开发与样式统一」
   ------------------------------------------------------------
   职责（只做三件事，不侵入业务）：
     1. 响应式导航：汉堡按钮开关菜单（含 ARIA、ESC、点击遮罩/链接自动关闭）
     2. 视口变化时复位状态，避免桌面端残留 is-open
     3. 页脚年份自动更新
   依赖：无。所有钩子都是 data-* 属性，不绑定具体类名。
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 响应式导航 ---------- */
  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.querySelector('[data-nav]');
    if (!toggle || !nav) return;

    var MOBILE = '(max-width: 768px)';

    function isMobile() {
      return window.matchMedia(MOBILE).matches;
    }

    function open() {
      nav.classList.add('is-open');
      document.body.classList.add('is-nav-open');
      toggle.setAttribute('aria-expanded', 'true');
    }

    function close() {
      nav.classList.remove('is-open');
      document.body.classList.remove('is-nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    }

    function isOpen() {
      return nav.classList.contains('is-open');
    }

    toggle.addEventListener('click', function () {
      if (isOpen()) {
        close();
      } else {
        open();
      }
    });

    /* 点菜单里的链接：先收起，再让它跳转 */
    nav.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (link && isMobile()) close();
    });

    /* 按 ESC 收起，焦点回到按钮 */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) {
        close();
        toggle.focus();
      }
    });

    /* 在菜单外点一下也收起 */
    document.addEventListener('click', function (e) {
      if (!isOpen() || !isMobile()) return;
      if (nav.contains(e.target) || toggle.contains(e.target)) return;
      close();
    });

    /* 从手机尺寸拉回桌面：把状态复位，别留下滚动锁 */
    var mq = window.matchMedia(MOBILE);
    var onChange = function () {
      if (!mq.matches) close();
    };
    if (mq.addEventListener) {
      mq.addEventListener('change', onChange);
    } else if (mq.addListener) {
      mq.addListener(onChange);
    }
  }

  /* ---------- 2. 页脚年份 ---------- */
  function initYear() {
    var slots = document.querySelectorAll('[data-current-year]');
    var year = String(new Date().getFullYear());
    for (var i = 0; i < slots.length; i += 1) {
      slots[i].textContent = year;
    }
  }

  /* ---------- 3. 当前页高亮（静态站可选） ---------- */
  function initActiveLink() {
    var path = window.location.pathname.split('/').pop() || 'index.html';
    var links = document.querySelectorAll('[data-nav] .site-nav__link');
    for (var i = 0; i < links.length; i += 1) {
      var href = links[i].getAttribute('href') || '';
      if (href && href === path) {
        links[i].classList.add('site-nav__link--active');
        links[i].setAttribute('aria-current', 'page');
      }
    }
  }

  /* ---------- 启动 ---------- */
  function boot() {
    initNav();
    initYear();
    initActiveLink();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();

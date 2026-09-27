/* ═══════════ دعوة زفاف سيف ونور ═══════════ */
(function () {
  'use strict';

  var WEDDING     = new Date(2026, 9, 2, 20, 0, 0);   // الشهر من صفر: 9 = أكتوبر
  var WEDDING_END = new Date(2026, 9, 3, 0, 0, 0);
  var CAL_DATES   = '20261002T170000Z/20261002T210000Z'; // ٨ م — ١٢ ص بتوقيت مصر (+٣)
  var TITLE       = 'حفل زفاف سيف ونور';
  var PLACE       = 'قاعة Grand VIP - سوهاج';
  var MAP_URL     = 'https://maps.app.goo.gl/3fqqN8fuBwerPQ9b7';

  var AR = '٠١٢٣٤٥٦٧٨٩';
  function ar(n) { return String(n).replace(/\d/g, function (d) { return AR[d]; }); }

  /* ── رسالة سريعة ── */
  var toast = document.getElementById('toast'), toastTimer;
  function say(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2800);
  }

  /* ── دعوة باسم الضيف: ?to=الاسم ── */
  var guest = (new URLSearchParams(location.search).get('to') || '').trim().slice(0, 60);
  if (guest) {
    [['opTo', 'إلى '], ['heroTo', 'أهلًا ']].forEach(function (p) {
      var el = document.getElementById(p[0]);
      var b = document.createElement('b');
      b.textContent = guest;
      el.textContent = p[1];
      el.appendChild(b);
      el.hidden = false;
    });
  }

  /* ── الموسيقى ── */
  var song = document.getElementById('song');
  var btnMusic = document.getElementById('music');
  var KEY = 'seif-nour-music';
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function wantsMusic() { try { return localStorage.getItem(KEY) !== 'off'; } catch (e) { return true; } }
  function setUI(on) {
    btnMusic.classList.toggle('on', on);
    btnMusic.setAttribute('aria-pressed', on ? 'true' : 'false');
    btnMusic.setAttribute('aria-label', on ? 'إيقاف الموسيقى' : 'تشغيل الموسيقى');
  }
  function play() {
    song.volume = 0.85;
    var p = song.play();
    if (p && p.then) p.then(function () { setUI(true); }).catch(function () { setUI(false); });
    else setUI(true);
  }
  btnMusic.addEventListener('click', function () {
    if (song.paused) { play(); store('on'); }
    else { song.pause(); setUI(false); store('off'); }
  });

  /* ── فتح الظرف ── */
  var opener = document.getElementById('opener');
  var seal = document.getElementById('seal');
  var opened = false;
  function openInvite() {
    if (opened) return;
    opened = true;
    if (wantsMusic()) play();         // الضغطة دي هي التفاعل اللي المتصفح مستنيه عشان يسمح بالصوت
    opener.classList.add('opening');
    setTimeout(function () {
      opener.classList.add('gone');
      document.body.classList.remove('locked');
      document.body.classList.add('ready');
      startPetals();
    }, 1900);
    setTimeout(function () { opener.remove(); }, 2900);
  }
  seal.addEventListener('click', openInvite);
  document.getElementById('envelope').addEventListener('click', openInvite);

  /* ── بتلات الورد ── */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function startPetals() {
    if (reduce) return;
    var box = document.getElementById('petals');
    var count = window.innerWidth < 600 ? 12 : 20;
    for (var i = 0; i < count; i++) {
      var p = document.createElement('i');
      var size = 8 + Math.random() * 9;
      p.style.left = (Math.random() * 100) + 'vw';
      p.style.width = size + 'px';
      p.style.height = (size * 1.3) + 'px';
      p.style.opacity = (0.45 + Math.random() * 0.45).toFixed(2);
      p.style.setProperty('--dx', (Math.random() * 120 - 60) + 'px');
      p.style.animationDuration = (9 + Math.random() * 9) + 's';
      p.style.animationDelay = (-Math.random() * 16) + 's';
      box.appendChild(p);
    }
  }

  /* ── العد التنازلي بالحلقات ── */
  var C = 276.46;
  var units = ['days', 'hours', 'mins', 'secs'].map(function (k) {
    var ring = document.getElementById('r-' + k);
    return {
      num: document.getElementById('cd-' + k),
      arc: ring.querySelector('.rp'),
      max: +ring.getAttribute('data-max')
    };
  });
  function tick() {
    var diff = WEDDING.getTime() - Date.now();
    if (diff <= 0) {
      document.getElementById('timer').hidden = true;
      var done = document.getElementById('timerDone');
      done.hidden = false;
      done.textContent = Date.now() > WEDDING_END.getTime()
        ? 'ألف مبروك — شكرًا لمشاركتكم فرحتنا'
        : 'النهارده ليلة الفرح — في انتظاركم';
      clearInterval(timer);
      return;
    }
    var s = Math.floor(diff / 1000);
    var vals = [Math.floor(s / 86400), Math.floor(s / 3600) % 24, Math.floor(s / 60) % 60, s % 60];
    units.forEach(function (u, i) {
      var txt = ar(vals[i]);
      if (u.num.textContent !== txt) u.num.textContent = txt;
      u.arc.style.strokeDashoffset = (C * (1 - Math.min(vals[i], u.max) / u.max)).toFixed(2);
    });
  }
  var timer = setInterval(tick, 1000);
  tick();

  /* ── الظهور عند التمرير ── */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        io.unobserve(e.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* ── التقويم: آبل تاخد ملف .ics، الباقي جوجل كاليندر ── */
  var btnCal = document.getElementById('btnCal');
  var isApple = /iPad|iPhone|iPod|Macintosh/.test(navigator.userAgent) ||
                (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (!isApple) {
    btnCal.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE' +
      '&text='     + encodeURIComponent(TITLE) +
      '&dates='    + CAL_DATES +
      '&details='  + encodeURIComponent('الساعة ٨ مساءً — يسعدنا حضوركم\n' + MAP_URL) +
      '&location=' + encodeURIComponent(PLACE);
    btnCal.removeAttribute('download');
    btnCal.target = '_blank';
    btnCal.rel = 'noopener';
  }
  btnCal.addEventListener('click', function () {
    say(isApple ? 'هيفتحلك التقويم — اضغط «إضافة»' : 'هيفتح جوجل كاليندر في تبويب جديد');
  });

  /* ── مشاركة الدعوة ── */
  var btnShare = document.getElementById('btnShare');
  var link = location.origin + location.pathname;
  var text = 'دعوة زفاف سيف ونور 🤍\n' +
    'الجمعة ٢ أكتوبر ٢٠٢٦ — الساعة ٨ مساءً\n' +
    PLACE + '\n' + link;
  btnShare.href = 'https://wa.me/?text=' + encodeURIComponent(text);
  btnShare.addEventListener('click', function (e) {
    if (navigator.share) {
      e.preventDefault();
      navigator.share({ title: TITLE, text: text }).catch(function () {});
    }
  });
})();

(() => {
  const T = document.body.dataset;          // 当前语言的按钮说明文字（来自 locales/ 里的 UI）
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const NS = 'http://www.w3.org/2000/svg';
  const headH = () => { const h = document.querySelector('.site-head'); return h ? h.offsetHeight : 0; };

  /* ---------- 画一把折扇（首屏和开场动画共用） ---------- */
  function drawFan(svg, o) {
    const { cx, cy, R, r0, n, span, cls, ribColor } = o;
    const step = span / (n - 1), h = step / 2;
    const pt = (rad, deg) => { const a = (deg - 90) * Math.PI / 180; return [cx + rad * Math.cos(a), cy + rad * Math.sin(a)]; };
    const defs = document.createElementNS(NS, 'defs');
    defs.innerHTML = `<linearGradient id="${cls}A" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c27d"/><stop offset="1" stop-color="#b38a42"/></linearGradient>
      <linearGradient id="${cls}B" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfab62"/><stop offset="1" stop-color="#977233"/></linearGradient>`;
    svg.appendChild(defs);
    const groups = [];
    const add = (deg, delay) => { const g = document.createElementNS(NS, 'g'); g.setAttribute('class', cls); g.style.setProperty('--r', deg + 'deg'); g.style.setProperty('--d', delay + 'ms'); svg.appendChild(g); groups.push(g); return g; };
    for (let i = 0; i < n; i++) {
      const g = add(-span / 2 + i * step, i * 36);
      const [ax, ay] = pt(R, -h), [bx, by] = pt(R, h), [c2x, c2y] = pt(r0, h), [dx, dy] = pt(r0, -h);
      const leaf = document.createElementNS(NS, 'path');
      leaf.setAttribute('d', `M${ax} ${ay} A${R} ${R} 0 0 1 ${bx} ${by} L${c2x} ${c2y} A${r0} ${r0} 0 0 0 ${dx} ${dy}Z`);
      leaf.setAttribute('fill', `url(#${cls}${i % 2 ? 'B' : 'A'})`);
      const [ex, ey] = pt(R - 4, 0), rib = document.createElementNS(NS, 'line');
      rib.setAttribute('x1', cx); rib.setAttribute('y1', cy); rib.setAttribute('x2', ex); rib.setAttribute('y2', ey);
      rib.setAttribute('stroke', ribColor); rib.setAttribute('stroke-width', 2); rib.setAttribute('stroke-linecap', 'round'); rib.setAttribute('opacity', .8);
      g.append(leaf, rib);
    }
    [-1, 1].forEach(side => {                // 两根大骨
      const g = add(side * (span / 2 + h), side < 0 ? 0 : (n - 1) * 36);
      const [ex, ey] = pt(R + 2, 0), rib = document.createElementNS(NS, 'line');
      rib.setAttribute('x1', cx); rib.setAttribute('y1', cy); rib.setAttribute('x2', ex); rib.setAttribute('y2', ey);
      rib.setAttribute('stroke', ribColor); rib.setAttribute('stroke-width', 6); rib.setAttribute('stroke-linecap', 'round');
      g.appendChild(rib);
    });
    const pin = document.createElementNS(NS, 'circle');
    pin.setAttribute('cx', cx); pin.setAttribute('cy', cy); pin.setAttribute('r', 7);
    pin.setAttribute('fill', '#2b152a'); pin.setAttribute('stroke', '#e0c487'); pin.setAttribute('stroke-width', 3);
    svg.appendChild(pin);
    return groups;
  }

  /* ---------- 首屏折扇 ---------- */
  const heroFan = document.getElementById('fan');
  if (heroFan) drawFan(heroFan, { cx: 260, cy: 280, R: 250, r0: 108, n: 24, span: 160, cls: 'pleat', ribColor: '#7a4a28' });
  // 首页大折扇：和小折扇一样，从闭合（全部收在正中）到打开；打开后扇叶才能点
  const bigFan = document.getElementById('bigFan');
  const openHeroFan = () => {
    if (heroFan) requestAnimationFrame(() => heroFan.classList.add('open'));
    if (bigFan) {
      requestAnimationFrame(() => requestAnimationFrame(() => bigFan.classList.add('open')));
      setTimeout(() => bigFan.classList.add('opened'), reduce ? 0 : 1500);
    }
  };

  /* ---------- 折扇开场：整个页面像折扇一样，从左下角开始一折一折打开到右下角（约 0.94 秒） ----------
     做法：先用一块纯黑幕布盖住页面，以屏幕底边中点为扇轴，把幕布从左往右一折一折“剪掉”，
     被剪掉的地方直接露出下面真正的页面（不留扇骨线或扇褶的痕迹）。 */
  const veil = document.getElementById('fanveil');
  const FOLDS = 12;           // 折数
  const FOLD_MS = 78;         // 每一折用时（12 × 78 ≈ 0.94 秒）
  let playing = false;
  function playVeil(after) {
    if (!veil || reduce) { after && after(); return; }
    playing = true;
    const W = innerWidth, H = innerHeight;
    const cx = W / 2, cy = H, R = Math.hypot(W / 2, H) + 40;          // 扇轴在屏幕底边中点
    const pt = deg => { const a = deg * Math.PI / 180; return [cx + R * Math.cos(a), cy - R * Math.sin(a)]; };
    const step = 180 / FOLDS;
    // 幕布：还没打开的部分（角度 0° ~ θ），θ 从 180°（左）减到 0°（右）
    const cover = theta => {
      if (theta <= 0.01) return 'polygon(0 0,0 0,0 0)';
      const pts = [[cx, cy]];
      for (let d = theta; d > 0; d -= 10) pts.push(pt(d));
      pts.push(pt(0));
      return 'polygon(' + pts.map(([x, y]) => `${x.toFixed(1)}px ${y.toFixed(1)}px`).join(',') + ')';
    };

    veil.style.display = '';
    veil.style.clipPath = veil.style.webkitClipPath = cover(180);
    document.documentElement.classList.add('veiled');
    after && after();                          // 幕布挡着的时候跳到目标位置

    const t0 = performance.now();
    const ease = x => 1 - Math.pow(1 - x, 3);
    const frame = now => {
      const t = now - t0, k = Math.min(FOLDS, Math.floor(t / FOLD_MS));
      // 每一折：前 65% 的时间展开，后 35% 停一下，形成“一折一折”的节奏
      const f = k >= FOLDS ? 0 : Math.min(1, ((t % FOLD_MS) / FOLD_MS) / 0.65);
      const theta = Math.max(0, 180 - (k + ease(f)) * step);
      veil.style.clipPath = veil.style.webkitClipPath = cover(theta);
      if (t < FOLDS * FOLD_MS) { requestAnimationFrame(frame); return; }
      veil.style.display = 'none';
      document.documentElement.classList.remove('veiled');
      playing = false;
      document.dispatchEvent(new Event('veil:done'));
    };
    requestAnimationFrame(frame);
  }
  document.addEventListener('veil:done', openHeroFan, { once: true });
  if (veil && !reduce) playVeil(); else openHeroFan();

  /* ---------- 手机菜单 ---------- */
  // 首页（大折扇）没有菜单栏，下面这些只在其他页面上运行
  const nav = document.getElementById('nav'), burger = document.getElementById('burger');
  const setMenu = open => { if (!nav) return; nav.classList.toggle('open', open); burger.setAttribute('aria-expanded', open); burger.setAttribute('aria-label', open ? T.menuClose : T.menuOpen); };
  if (burger) burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));

  /* ---------- 宫廷折扇下拉菜单（点小箭头也能展开，方便触屏） ---------- */
  document.querySelectorAll('.nav-group').forEach(g => {
    const btn = g.querySelector('.sub-toggle');
    btn.addEventListener('click', e => { e.stopPropagation(); const open = !g.classList.contains('open'); g.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); });
  });

  /* ---------- 菜单跳转：同一页内的栏目先播放折扇动画再显示 ---------- */
  if (nav) nav.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a) return;
    setMenu(false);
    document.querySelectorAll('.nav-group.open').forEach(g => g.classList.remove('open'));
    const url = new URL(a.href, location.href);
    const samePage = url.pathname === location.pathname && url.hash;
    if (!samePage) return;                   // 去别的页面：新页面打开时会自己播放动画
    const target = document.getElementById(url.hash.slice(1));
    if (!target) return;
    e.preventDefault();
    if (playing) return;
    playVeil(() => {
      const y = target.getBoundingClientRect().top + scrollY - headH() + 1;
      window.scrollTo({ top: y, behavior: 'instant' });
      history.replaceState(null, '', url.hash);
    });
  });

  /* ---------- 语言菜单 ---------- */
  const langBtn = document.getElementById('langBtn'), langMenu = document.getElementById('langMenu');
  const setLang = open => { langMenu.hidden = !open; langBtn.setAttribute('aria-expanded', open); };
  langBtn.addEventListener('click', e => { e.stopPropagation(); setLang(langMenu.hidden); });
  document.addEventListener('click', e => {
    if (!e.target.closest('.lang')) setLang(false);
    if (!e.target.closest('.nav-group')) document.querySelectorAll('.nav-group.open').forEach(g => { g.classList.remove('open'); g.querySelector('.sub-toggle').setAttribute('aria-expanded', false); });
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { setLang(false); setMenu(false); } });

  /* ---------- 右侧进度条 + 滚动时菜单高亮 ---------- */
  const secs = [...document.querySelectorAll('main > section[data-label]')];
  const links = [...document.querySelectorAll('.nav a[data-sec]')];
  const fill = document.getElementById('railFill') || document.createElement('div');
  const tickBox = document.getElementById('railTicks') || document.createElement('div');
  const maxScroll = () => Math.max(1, document.documentElement.scrollHeight - innerHeight);
  const fixed = T.active;                   // 宫廷折扇页、列表页：顶部菜单固定高亮这一项
  const ticks = secs.map(s => {
    const b = document.createElement('button');
    b.className = 'rail-tick'; b.type = 'button';
    b.setAttribute('aria-label', T.jumpTo + s.dataset.label);
    b.addEventListener('click', () => s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }));
    tickBox.appendChild(b); return b;
  });
  const placeTicks = () => secs.forEach((s, i) => {
    const p = Math.min(1, (s.getBoundingClientRect().top + scrollY - headH()) / maxScroll());
    ticks[i].style.top = (Math.max(0, p) * 100) + '%';
  });
  let current = null;
  const update = () => {
    const p = Math.min(1, Math.max(0, scrollY / maxScroll()));
    fill.style.transform = `scaleY(${p})`;
    const line = headH() + innerHeight * 0.35;
    let idx = -1;
    secs.forEach((s, i) => { if (s.getBoundingClientRect().top <= line) idx = i; });
    if (p > 0.995 && secs.length) idx = secs.length - 1;
    ticks.forEach((t, i) => { t.classList.toggle('passed', i < idx); t.classList.toggle('is-active', i === idx); });
    const id = idx >= 0 ? secs[idx].id : '';
    if (id === current) return;
    current = id;
    links.forEach(a => {
      const on = a.dataset.sec === id || (fixed && a.dataset.sec === fixed);
      a.classList.toggle('is-active', on); a.toggleAttribute('aria-current', on);
    });
  };
  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { update(); ticking = false; }); } }, { passive: true });
  addEventListener('resize', () => { placeTicks(); update(); });
  addEventListener('load', () => { placeTicks(); update(); });
  placeTicks(); update();

  /* ---------- 折扇展示：轮播 + 放大镜 ---------- */
  const gallery = document.getElementById('gallery');
  if (gallery) {
    const stage = document.getElementById('stage'), loupe = document.getElementById('loupe');
    const slides = [...gallery.querySelectorAll('.slide')], cards = [...gallery.querySelectorAll('.g-card')];
    const cur = document.getElementById('gCur'), bar = document.getElementById('gBar');
    const ms = (parseFloat(gallery.dataset.seconds) || 5) * 1000;
    let i = 0, timer = null, start = 0, paused = false, left = ms;

    const show = k => {
      i = (k + slides.length) % slides.length;
      slides.forEach((s, j) => { s.classList.toggle('is-active', j === i); s.setAttribute('aria-hidden', j !== i); });
      cards.forEach((c, j) => { c.hidden = j !== i; c.classList.toggle('is-active', j === i); });
      cur.textContent = String(i + 1).padStart(2, '0');
      const nxt = slides[(i + 1) % slides.length].querySelector('img'); nxt.loading = 'eager';   // 预先加载下一张
      if (loupe.classList.contains('on')) moveLoupe(lastX, lastY);
    };
    // 每 5 秒换到右边那一把；鼠标停在大图上看细节时暂停
    const tick = () => { show(i + 1); restart(); };
    const restart = () => { clearTimeout(timer); left = ms; run(); };
    const run = () => {
      if (paused) return;
      start = performance.now();
      timer = setTimeout(tick, left);
      bar.style.transition = 'none'; bar.style.transform = `scaleX(${1 - left / ms})`;
      void bar.offsetWidth;
      bar.style.transition = `transform ${left}ms linear`; bar.style.transform = 'scaleX(1)';
    };
    const pause = () => {
      if (paused) return; paused = true; clearTimeout(timer);
      left = Math.max(0, left - (performance.now() - start));
      bar.style.transition = 'none'; bar.style.transform = `scaleX(${1 - left / ms})`;
    };
    const resume = () => { if (!paused) return; paused = false; run(); };

    gallery.querySelector('.g-prev').addEventListener('click', () => { show(i - 1); restart(); if (paused) pause(); });
    gallery.querySelector('.g-next').addEventListener('click', () => { show(i + 1); restart(); if (paused) pause(); });
    gallery.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { show(i - 1); restart(); }
      if (e.key === 'ArrowRight') { show(i + 1); restart(); }
    });
    document.addEventListener('visibilitychange', () => document.hidden ? pause() : resume());

    // 手机上左右滑动切换
    let sx = null;
    stage.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', e => {
      if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 40) { show(i + (dx < 0 ? 1 : -1)); restart(); }
    });

    // 放大镜：鼠标旁边的小圆框里显示附近的扇子细节
    // EDGE：圆框边缘到鼠标的距离。原来约 78px，现在改为三分之一（约 26px）
    const ZOOM = 2.6, SIZE = 200, EDGE = 26;
    const OFF = (SIZE / 2 + EDGE) / Math.SQRT2;          // 圆心放在鼠标右上方 45° 处
    let lastX = 0, lastY = 0;
    const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
    function moveLoupe(x, y) {
      const img = slides[i].querySelector('img');
      if (!img.naturalWidth) return;
      const r = stage.getBoundingClientRect();
      const s = Math.max(r.width / img.naturalWidth, r.height / img.naturalHeight);    // 和 object-fit: cover 一致
      const w = img.naturalWidth * s, h = img.naturalHeight * s;
      const ox = (r.width - w) / 2, oy = (r.height - h) / 2;
      const px = x - r.left - ox, py = y - r.top - oy;                                 // 鼠标在图片上的位置
      if (px < 0 || py < 0 || px > w || py > h) { loupe.classList.remove('on'); return; }
      loupe.style.backgroundImage = `url("${img.currentSrc || img.src}")`;
      loupe.style.backgroundSize = `${w * ZOOM}px ${h * ZOOM}px`;
      loupe.style.backgroundPosition = `${SIZE / 2 - px * ZOOM}px ${SIZE / 2 - py * ZOOM}px`;
      // 圆框放在鼠标右上方，靠近边缘时换到另一侧
      const mx = x - r.left, my = y - r.top;
      let ccx = mx + OFF, ccy = my - OFF;                  // 圆心
      if (ccx + SIZE / 2 > r.width - 8) ccx = mx - OFF;    // 靠近右边缘：换到左边
      if (ccy - SIZE / 2 < 8) ccy = my + OFF;              // 靠近上边缘：换到下边
      const lx = ccx - SIZE / 2, ly = ccy - SIZE / 2;
      loupe.style.left = lx + 'px'; loupe.style.top = ly + 'px';
      loupe.classList.add('on');
    }
    if (fine) {
      stage.addEventListener('mousemove', e => {
        if (e.target.closest('.g-arrow')) { loupe.classList.remove('on'); return; }
        lastX = e.clientX; lastY = e.clientY; moveLoupe(lastX, lastY);
      });
      stage.addEventListener('mouseenter', pause);
      stage.addEventListener('mouseleave', () => { loupe.classList.remove('on'); resume(); });
    }
    restart();
  }
})();

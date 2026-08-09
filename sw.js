const CACHE_NAME = 'gym-tracker-v1';
const ASSETS_TO_CACHE = [
  './index.html',
  './manifest.json',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js'
];

// 安裝並快取資源
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
});

// 攔截請求並優先使用快取
self.addEventListener('fetch', (e) => {
  // 對 CSV 檔案不進行強快取，確保總是抓到最新數據
  if (e.request.url.includes('gym_capacity_log.csv')) {
    e.respondWith(fetch(e.request));
    return;
  }
  
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request))
  );
});

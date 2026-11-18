"""v5 시험 시계로 '테스트 사본'(test.html)을 만든다.

테스트 사본은 원본과 똑같고, 다음만 다르다.
  - 주소 뒤 ?t=2026-11-23T08:57:00&speed=10 으로 원하는 날짜·시각에서 시작 (KST)
  - speed 배속으로 시간이 흐름 (1 = 실제 속도)
  - 인터넷 시각 동기화를 끔 (켜 두면 가짜 시각이 실제 시각으로 되돌아감)
  - 왼쪽 아래 테스트 패널(상황 바로가기, 날짜·시각 입력, 배속)

원본을 고친 뒤에는  python make_test.py  를 다시 실행하면 된다.
"""
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "익산부송중_2학기2차시험_시험시계_v5.html"
OUT = HERE / "test.html"

SHIM = r"""
<script>
/* ===== [테스트 전용] 가짜 시계 ===== */
(function(){
  const p = new URLSearchParams(location.search);
  const t = p.get('t');
  const sp = parseFloat(p.get('speed') || '1') || 1;
  if(!t) return;
  const O = Date, realStart = O.now();
  const fakeStart = O.parse(t.length === 16 ? t + ':00+09:00' : t + '+09:00');
  if(isNaN(fakeStart)) return;
  const fnow = () => fakeStart + (O.now() - realStart) * sp;
  function D(...a){ return a.length ? new O(...a) : new O(fnow()); }
  D.prototype = O.prototype; D.now = fnow; D.parse = O.parse; D.UTC = O.UTC;
  window.Date = D;
  window.__TEST__ = { t, speed: sp };
})();
</script>
"""

PANEL = r"""
<style>
#testPanel{position:fixed;left:10px;bottom:10px;z-index:9999;font:13px/1.4 'Malgun Gothic',sans-serif;
  background:rgba(20,24,34,.94);color:#e6ecf6;border:1px solid #ffb02e;border-radius:10px;padding:10px 12px;
  box-shadow:0 8px 24px rgba(0,0,0,.5);max-width:calc(100vw - 20px)}
#testPanel b{color:#ffb02e}
#testPanel select,#testPanel input,#testPanel button{font:inherit;margin:3px 2px;padding:3px 6px;border-radius:6px;
  border:1px solid #556;background:#0f1524;color:#e6ecf6}
#testPanel button{cursor:pointer;background:#ffb02e;color:#111;border:none;font-weight:700}
#testPanel.min .body{display:none}
#testPanel .row1{display:flex;gap:8px;align-items:center;justify-content:space-between}
#testPanel #tpToggle{background:#334;color:#e6ecf6}
</style>
<div id="testPanel">
  <div class="row1"><span><b>🧪 테스트 모드</b> <span id="tpNow"></span></span><button id="tpToggle">접기</button></div>
  <div class="body">
    <div>
      <select id="tpPreset">
        <option value="">— 상황 바로가기 —</option>
        <optgroup label="3학년 11/23(월): 자율·역사·자율">
          <option value="2026-11-23T08:30">08:30 시험 시작 전</option>
          <option value="2026-11-23T08:45">08:45 조회·사전교육</option>
          <option value="2026-11-23T08:52">08:52 시험 준비 시간</option>
          <option value="2026-11-23T08:57">08:57 1교시 자율학습 준비</option>
          <option value="2026-11-23T09:20">09:20 1교시 자율학습</option>
          <option value="2026-11-23T09:50">09:50 쉬는 시간</option>
          <option value="2026-11-23T09:57">09:57 2교시 역사 배부</option>
          <option value="2026-11-23T10:30">10:30 2교시 역사 시험 중</option>
          <option value="2026-11-23T11:50">11:50 오늘 시험 종료</option>
        </optgroup>
        <optgroup label="3학년 11/24(화): 영어·자율·과학">
          <option value="2026-11-24T09:20">09:20 1교시 영어 시험 중</option>
          <option value="2026-11-24T10:57">10:57 3교시 과학 배부</option>
        </optgroup>
        <optgroup label="날짜 넘어감·기간">
          <option value="2026-11-22T23:59:50">11/22 23:59:50 → 자정 넘어 첫 시험일로 자동 전환</option>
          <option value="2026-11-23T23:59:50">11/23 23:59:50 → 다음 시험일로 자동 전환</option>
          <option value="2026-11-30T09:00">11/30 사이 기간 → 2학년 다음 시험 D-7</option>
          <option value="2026-12-10T11:44:30">12/10 11:44:30 2학년 마지막 시험 끝나는 순간</option>
          <option value="2026-12-11T09:00">12/11 → 전체 시험 종료</option>
        </optgroup>
      </select>
    </div>
    <div>
      <input type="datetime-local" id="tpTime" step="1">
      배속 <select id="tpSpeed">
        <option value="1">1배</option><option value="10">10배</option>
        <option value="60">60배</option><option value="300">300배</option>
      </select>
      <button id="tpGo">이 시각으로</button>
      <button id="tpReal" style="background:#334;color:#e6ecf6">실제 시각</button>
    </div>
  </div>
</div>
<script>
(function(){
  const T = window.__TEST__ || {};
  const $ = id => document.getElementById(id);
  if(T.t) $('tpTime').value = T.t.slice(0,19);
  $('tpSpeed').value = String(T.speed || 1);
  const go = t => { const q = new URLSearchParams({t, speed:$('tpSpeed').value}); location.search = q.toString(); };
  $('tpPreset').onchange = e => { if(e.target.value) go(e.target.value); };
  $('tpGo').onclick = () => { if($('tpTime').value) go($('tpTime').value); };
  $('tpReal').onclick = () => { location.search = ''; };
  $('tpToggle').onclick = () => { const p=$('testPanel'); p.classList.toggle('min'); $('tpToggle').textContent = p.classList.contains('min')?'펼치기':'접기'; };
  setInterval(()=>{ const d=nowKST(); $('tpNow').textContent = T.t ? `· 가상 ${d.getMonth()+1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())} (${T.speed}배)` : '· 실제 시각'; }, 250);
})();
</script>
"""

SYNC_OLD = "syncTime();\nsetInterval(syncTime, 30*60*1000);   /* 30분마다 재동기화 */"
SYNC_NEW = ("if(window.__TEST__){ document.getElementById('sync').textContent='테스트 모드 · 동기화 꺼짐'; }\n"
            "else { syncTime(); setInterval(syncTime, 30*60*1000); }")


def replace_once(html: str, old: str, new: str) -> str:
    assert html.count(old) == 1, f"원본에서 찾을 수 없음: {old[:40]!r}"
    return html.replace(old, new)


html = SRC.read_text(encoding="utf-8")
html = replace_once(html, "<head>", "<head>" + SHIM)
html = replace_once(html, "<title>시험 시계 · 익산부송중학교</title>", "<title>[테스트] 시험 시계 · 익산부송중학교</title>")
html = replace_once(html, "renderSync();\n" + SYNC_OLD, "renderSync();\n" + SYNC_NEW)
html = replace_once(html, "</body>", PANEL + "</body>")
OUT.write_text(html, encoding="utf-8")
print("만듦:", OUT.name)

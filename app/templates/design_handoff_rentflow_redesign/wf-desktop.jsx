// ────────────────────────────────────────────────────────────────
// V1: Analytics Dashboard (homepage / "Tổng quan" tab)
// V2: Hóa đơn tháng — compact table + side detail panel
// V3: Phòng & Khách — card grid by floor
// ────────────────────────────────────────────────────────────────

const ART_W = 1380;
const ART_H = 860;

// ════════════════════════════════════════════════════════════════
// V1 — DASHBOARD-FIRST  (active tab: Tổng quan)
// Stats + charts + activity feed + "rooms needing attention"
// ════════════════════════════════════════════════════════════════
function V1Dashboard() {
  const chart = [
    { label: 'T6', v: 41 }, { label: 'T7', v: 43 },
    { label: 'T8', v: 46 }, { label: 'T9', v: 45 },
    { label: 'T10', v: 51 }, { label: 'T11', v: 52, accent: true },
  ].map(d => ({ ...d, v: d.v * 1e6 }));

  return (
    <div className="wf-art" style={{ width: ART_W, height: ART_H }}>
      <TopNav active="dashboard" />

      <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 18 }}>
        {/* Greeting row */}
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
          <div>
            <div className="wf-h1" style={{ fontSize: 32 }}>Chào buổi sáng, Cô Lan 👋</div>
            <div style={{ color: 'var(--ink-2)', marginTop: 4 }}>Hôm nay là 23/11/2025 — còn <b className="wf-underline">4 phòng</b> chưa thu tiền tháng này.</div>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <div className="wf-btn"><span>📥</span> Import CSV</div>
            <div className="wf-btn wf-btn-primary"><span>＋</span> Ghi điện tháng này</div>
          </div>
        </div>

        {/* Stat row — 6 tiles */}
        <div style={{ display: 'flex', gap: 14 }}>
          <StatTile label="Tổng phòng"   value="18"   sub="15 đang thuê · 3 trống" icon="⌂" />
          <StatTile label="Chưa thu"     value="4"    sub="phòng tháng 11" accent="var(--accent)" icon="!" />
          <StatTile label="Đã thu"       value="45.2M" sub="11 phòng · 73%" accent="var(--ok)" icon="✓" />
          <StatTile label="Đóng trước"   value="3"    sub="phòng đã đóng" accent="var(--info)" icon="⤴" />
          <StatTile label="Doanh thu T11" value="52.4M" sub="↑ 4% so với T10" icon="₫" />
          <StatTile label="Tiền cọc giữ" value="132M" sub="15 phòng" icon="◇" />
        </div>

        {/* 2-column main */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 18 }}>
          {/* Chart card */}
          <div className="wf-card" style={{ padding: 18 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <div>
                <div className="wf-h3">Doanh thu 6 tháng gần nhất</div>
                <div style={{ color: 'var(--ink-2)', fontSize: 13 }}>VNĐ (triệu) · điện + dịch vụ + tiền phòng</div>
              </div>
              <div style={{ display: 'flex', gap: 6 }}>
                <span className="wf-tag" style={{ background: 'var(--ink)', color: 'var(--paper)', borderColor: 'var(--ink)' }}>6T</span>
                <span className="wf-tag">12T</span>
                <span className="wf-tag">2025</span>
              </div>
            </div>
            <SketchBarChart data={chart} height={200} accentIdx={5} />
          </div>

          {/* Status donut */}
          <div className="wf-card" style={{ padding: 18, display: 'flex', flexDirection: 'column' }}>
            <div className="wf-h3" style={{ marginBottom: 12 }}>Trạng thái tháng 11</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <SketchDonut paid={11} unpaid={4} prepaid={3} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, flex: 1 }}>
                <LegendRow color="var(--ok)" label="Đã thu" n={11} />
                <LegendRow color="var(--accent)" label="Chưa thu" n={4} />
                <LegendRow color="var(--info)" label="Đóng trước" n={3} />
              </div>
            </div>
          </div>
        </div>

        {/* Bottom row: rooms needing attention + activity */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: 18 }}>
          <div className="wf-card" style={{ padding: 18 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <div className="wf-h3">⚠ Phòng cần chú ý</div>
              <div style={{ fontSize: 13, color: 'var(--ink-2)' }}>4 phòng chưa thu T11</div>
            </div>
            {SAMPLE_ROOMS.filter(r => r.status === 'unpaid').slice(0, 3).map(r => (
              <div key={r.num} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 0', borderBottom: '1px dashed var(--ink-3)' }}>
                <div className="wf-avatar" style={{ background: 'var(--accent-soft)' }}>{r.num}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 700 }}>{r.tenant} · {r.phone}</div>
                  <div style={{ fontSize: 13, color: 'var(--ink-2)' }}>Tổng: <b>{formatVND(calcTotal(r))}đ</b> · điện {r.newR - r.oldR} kWh</div>
                </div>
                <div className="wf-btn" style={{ padding: '4px 10px', fontSize: 13 }}>⟶ Nhắc</div>
                <div className="wf-btn wf-btn-primary" style={{ padding: '4px 10px', fontSize: 13 }}>✓ Thu</div>
              </div>
            ))}
          </div>

          <div className="wf-card" style={{ padding: 18 }}>
            <div className="wf-h3" style={{ marginBottom: 12 }}>Hoạt động gần đây</div>
            {[
              { who: 'P.202', what: 'đã thanh toán', amount: '4.298.000đ', time: '2 giờ trước', kind: 'paid' },
              { who: 'P.103', what: 'đóng trước 3 tháng', amount: '11.4M', time: 'hôm qua', kind: 'prepaid' },
              { who: 'P.301', what: 'cập nhật số điện', amount: '+88 kWh', time: 'hôm qua', kind: 'meter' },
              { who: 'P.102', what: 'đã thanh toán', amount: '4.000.000đ', time: '2 ngày trước', kind: 'paid' },
            ].map((a, i) => (
              <div key={i} style={{ display: 'flex', gap: 10, padding: '8px 0', borderBottom: i < 3 ? '1px dashed var(--ink-3)' : 'none' }}>
                <div className="wf-dot" style={{ marginTop: 6, background: a.kind === 'paid' ? 'var(--ok)' : a.kind === 'prepaid' ? 'var(--info)' : 'var(--warn)' }} />
                <div style={{ flex: 1, fontSize: 14 }}>
                  <div><b>{a.who}</b> {a.what} <b style={{ color: 'var(--accent)' }}>{a.amount}</b></div>
                  <div style={{ fontSize: 12, color: 'var(--ink-3)' }}>{a.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Sticky annotations */}
      <StickyNote x={140} y={210} rotate={-2} width={210}>
        ✏️ <b>Tổng phòng</b> lấy từ API <code>/api/rooms</code> — không hardcode 18 nữa.
      </StickyNote>
      <StickyNote x={36} y={ART_H - 130} rotate={-1.5} width={240}>
        ✏️ "Phòng cần chú ý" thay cho tab <i>Chưa thu</i> trên trang chính — nút thu tiền tại chỗ, không cần vào bảng.
      </StickyNote>
    </div>
  );
}

function LegendRow({ color, label, n }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span className="wf-dot" style={{ background: color, width: 14, height: 14 }} />
      <span style={{ fontSize: 14, flex: 1 }}>{label}</span>
      <b style={{ fontFamily: 'var(--font-head)', fontSize: 20 }}>{n}</b>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════
// V2 — HÓA ĐƠN THÁNG: Compact list + side detail panel
// Fix: 12 cols → 5 cols. Detail panel for breakdown + actions.
// ════════════════════════════════════════════════════════════════
function V2BillsMasterDetail() {
  const selected = SAMPLE_ROOMS[0]; // 101 unpaid
  const elecUsage = selected.newR - selected.oldR;
  const elecFee = elecUsage * ELECTRIC_PRICE;
  const total = calcTotal(selected);

  return (
    <div className="wf-art" style={{ width: ART_W, height: ART_H }}>
      <TopNav active="bills" />

      {/* Filter bar */}
      <div style={{ padding: '14px 24px', borderBottom: '1px dashed var(--ink-3)', display: 'flex', alignItems: 'center', gap: 14, background: 'var(--paper-2)' }}>
        <div style={{ display: 'flex', gap: 2, padding: 3, border: '2px solid var(--ink)', borderRadius: 8, background: 'var(--paper)' }}>
          {['Tất cả · 15', 'Chưa thu · 4', 'Đã thu · 11', 'Đóng trước · 3'].map((t, i) => (
            <div key={t} className={'wf-tab' + (i === 1 ? ' active' : '')} style={{ fontSize: 16, padding: '5px 12px' }}>{t}</div>
          ))}
        </div>
        <div className="wf-input" style={{ width: 280, color: 'var(--ink-3)' }}>⌕ Tìm theo phòng, tên khách, SĐT…</div>
        <div className="wf-tag">Tầng: tất cả ▾</div>
        <div className="wf-tag">Sắp xếp: phòng ↑</div>
        <div style={{ flex: 1 }} />
        <div className="wf-btn"><span>📤</span> Xuất CSV</div>
        <div className="wf-btn wf-btn-primary"><span>📨</span> Gửi nhắc nhở (4)</div>
      </div>

      {/* Master + Detail */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.1fr', gap: 0, height: ART_H - 132 }}>
        {/* LEFT: compact bill list */}
        <div style={{ borderRight: '2px solid var(--ink)', overflow: 'hidden', padding: '12px 0' }}>
          {/* table header */}
          <div style={{ display: 'grid', gridTemplateColumns: '60px 1fr 110px 90px', gap: 10, padding: '6px 18px', borderBottom: '2px solid var(--ink)' }}>
            <div className="wf-label">Phòng</div>
            <div className="wf-label">Khách thuê</div>
            <div className="wf-label" style={{ textAlign: 'right' }}>Tổng</div>
            <div className="wf-label" style={{ textAlign: 'center' }}>Trạng thái</div>
          </div>
          {SAMPLE_ROOMS.filter(r => r.status !== 'empty').map((r, i) => {
            const isSel = r.num === selected.num;
            return (
              <div key={r.num} style={{
                display: 'grid',
                gridTemplateColumns: '60px 1fr 110px 90px',
                gap: 10,
                padding: '12px 18px',
                alignItems: 'center',
                background: isSel ? 'var(--accent-soft)' : 'transparent',
                borderLeft: isSel ? '4px solid var(--accent)' : '4px solid transparent',
                borderBottom: '1px dashed var(--ink-3)',
              }}>
                <div className="wf-h3" style={{ fontSize: 22, color: isSel ? 'var(--accent)' : 'var(--ink)' }}>{r.num}</div>
                <div>
                  <div style={{ fontWeight: 700 }}>{r.tenant}</div>
                  <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{r.phone || '—'}</div>
                </div>
                <div style={{ textAlign: 'right', fontFamily: 'var(--font-head)', fontSize: 18 }}>
                  {formatVND(calcTotal(r))}<span style={{ fontSize: 12 }}>đ</span>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <span className={'wf-pill ' + (r.status === 'unpaid' ? 'wf-pill-red' : r.status === 'paid' ? 'wf-pill-green' : 'wf-pill-blue')}>
                    {r.status === 'unpaid' ? 'Chưa thu' : r.status === 'paid' ? 'Đã thu' : 'Đóng trước'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* RIGHT: detail panel */}
        <div style={{ padding: '20px 28px', overflow: 'hidden', background: 'var(--paper)' }}>
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 16 }}>
            <div className="wf-avatar" style={{ width: 56, height: 56, fontSize: 24, background: 'var(--accent-soft)', borderColor: 'var(--accent)', color: 'var(--accent)' }}>{selected.num}</div>
            <div style={{ flex: 1 }}>
              <div className="wf-h2">{selected.tenant}</div>
              <div style={{ color: 'var(--ink-2)' }}>📞 {selected.phone} · Tầng {selected.floor} · ngày thuê 15/03/2024</div>
            </div>
            <span className="wf-pill wf-pill-red" style={{ fontSize: 14, padding: '5px 14px' }}>Chưa thu · 22 ngày</span>
          </div>

          {/* Electric reading — proper input, not in table */}
          <div className="wf-card-soft" style={{ padding: 14, marginBottom: 14, background: 'var(--paper-2)' }}>
            <div className="wf-label" style={{ marginBottom: 8 }}>Số điện tháng 11</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>Số cũ</div>
                <div className="wf-h2" style={{ color: 'var(--ink-3)' }}>{selected.oldR}</div>
              </div>
              <div style={{ fontSize: 26, color: 'var(--ink-3)' }}>→</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>Số mới</div>
                <div className="wf-input" style={{ fontFamily: 'var(--font-head)', fontSize: 26, padding: '4px 12px', color: 'var(--accent)' }}>{selected.newR}</div>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>Sử dụng</div>
                <div className="wf-h2" style={{ color: 'var(--info)' }}>{elecUsage} kWh</div>
              </div>
            </div>
          </div>

          {/* Breakdown */}
          <div className="wf-card-soft" style={{ padding: 16, marginBottom: 14 }}>
            <div className="wf-label" style={{ marginBottom: 10 }}>Chi tiết tháng này</div>
            {[
              ['Tiền phòng', selected.rent],
              ['Phí dịch vụ', selected.service],
              [`Tiền điện (${elecUsage} × ${formatVND(ELECTRIC_PRICE)}đ)`, elecFee],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px dashed var(--ink-3)' }}>
                <span>{k}</span>
                <span style={{ fontFamily: 'var(--font-head)', fontSize: 18 }}>{formatVND(v)}đ</span>
              </div>
            ))}
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0 0', alignItems: 'baseline' }}>
              <span className="wf-h3">Tổng cộng</span>
              <span className="wf-h1" style={{ color: 'var(--accent)' }}>{formatVND(total)}đ</span>
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
            <div className="wf-btn wf-btn-primary" style={{ justifyContent: 'center', padding: '12px' }}>✓ Đánh dấu đã thu</div>
            <div className="wf-btn" style={{ justifyContent: 'center', padding: '12px' }}>📅 Đóng trước nhiều tháng</div>
            <div className="wf-btn" style={{ justifyContent: 'center', padding: '12px' }}>🔲 Xem hóa đơn QR</div>
            <div className="wf-btn" style={{ justifyContent: 'center', padding: '12px' }}>🕒 Lịch sử phòng</div>
          </div>

          <div style={{ marginTop: 14, fontSize: 13, color: 'var(--ink-2)', display: 'flex', justifyContent: 'space-between' }}>
            <span>Tiền cọc giữ: <b>{formatVND(8000000)}đ</b></span>
            <span>Đã thuê: <b>20 tháng</b></span>
          </div>
        </div>
      </div>

      <StickyNote x={36} y={ART_H - 110} width={250}>
        ✏️ Chỉ 5 cột thay vì 12. Nhập điện + actions <b>dồn vào panel</b> bên phải → không còn lộn xộn trong bảng.
      </StickyNote>
      <StickyNote x={ART_W - 280} y={140} rotate={2} width={250}>
        ✏️ Nút <b>"Đóng trước"</b> đứng riêng — không phải bấm trạng thái 2 lần như cũ.
      </StickyNote>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════
// V3 — PHÒNG & KHÁCH: card grid by floor
// Visual, mobile-friendly, easy to scan
// ════════════════════════════════════════════════════════════════
function V3RoomCardGrid() {
  const byFloor = {};
  SAMPLE_ROOMS.forEach(r => {
    byFloor[r.floor] = byFloor[r.floor] || [];
    byFloor[r.floor].push(r);
  });
  // pad to 4 per floor for grid demo
  Object.keys(byFloor).forEach(f => {
    while (byFloor[f].length < 4) {
      byFloor[f].push({ num: f + (byFloor[f].length + 1).toString().padStart(2, '0'), status: 'empty', tenant: '— Trống —', floor: f });
    }
  });

  return (
    <div className="wf-art" style={{ width: ART_W, height: ART_H }}>
      <TopNav active="rooms" />

      {/* Sub header */}
      <div style={{ padding: '14px 24px', borderBottom: '1px dashed var(--ink-3)', display: 'flex', alignItems: 'center', gap: 14, background: 'var(--paper-2)' }}>
        <div className="wf-h2">18 phòng <span style={{ color: 'var(--ink-2)', fontSize: 18 }}>· 15 đang thuê · 3 trống</span></div>
        <div style={{ flex: 1 }} />
        <div className="wf-input" style={{ width: 260, color: 'var(--ink-3)' }}>⌕ Tìm tên khách / SĐT / phòng</div>
        <div style={{ display: 'flex', gap: 2, padding: 3, border: '2px solid var(--ink)', borderRadius: 8, background: 'var(--paper)' }}>
          {['Tất cả', 'Đang thuê', 'Trống', 'Chưa thu T11'].map((t, i) => (
            <div key={t} className={'wf-tab' + (i === 0 ? ' active' : '')} style={{ fontSize: 15, padding: '4px 12px' }}>{t}</div>
          ))}
        </div>
        <div className="wf-btn wf-btn-primary"><span>＋</span> Thêm phòng</div>
      </div>

      <div style={{ padding: 22, display: 'flex', flexDirection: 'column', gap: 22, height: ART_H - 130, overflow: 'hidden' }}>
        {[1, 2, 3].map(floor => (
          <div key={floor}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 14, marginBottom: 10 }}>
              <div className="wf-h2">Tầng {floor}</div>
              <div style={{ flex: 1, height: 2, background: 'var(--ink-3)', borderRadius: 2 }} />
              <div style={{ fontSize: 13, color: 'var(--ink-2)' }}>{(byFloor[floor] || []).filter(r => r.status !== 'empty').length}/{(byFloor[floor] || []).length} thuê</div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14 }}>
              {(byFloor[floor] || []).slice(0, 4).map(r => <RoomCard key={r.num} r={r} />)}
            </div>
          </div>
        ))}
      </div>

      <StickyNote x={ART_W - 280} y={140} rotate={2} width={260}>
        ✏️ <b>1 card / phòng</b>. Visual hơn bảng, scale tốt mobile (xếp 2 cột / 1 cột). Click → modal chỉnh sửa.
      </StickyNote>
      <StickyNote x={36} y={ART_H - 100} width={240}>
        ✏️ Mỗi card hiển thị status chip, total T11, và <b>nhập điện nhanh</b> ngay trên card.
      </StickyNote>
    </div>
  );
}

function RoomCard({ r }) {
  const empty = r.status === 'empty';
  const total = calcTotal(r);
  const statusMap = {
    unpaid:  { cls: 'wf-pill-red',   label: 'Chưa thu',  accent: 'var(--accent)' },
    paid:    { cls: 'wf-pill-green', label: 'Đã thu',    accent: 'var(--ok)' },
    prepaid: { cls: 'wf-pill-blue',  label: 'Đóng trước', accent: 'var(--info)' },
    empty:   { cls: '',              label: 'Trống',     accent: 'var(--ink-3)' },
  };
  const s = statusMap[r.status];

  return (
    <div className="wf-card" style={{ padding: 14, position: 'relative', borderColor: empty ? 'var(--ink-3)' : 'var(--ink)', background: empty ? 'var(--paper-2)' : 'var(--paper)', opacity: empty ? 0.75 : 1 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <div className="wf-h1" style={{ fontSize: 32, color: s.accent }}>{r.num}</div>
        {!empty && <span className={'wf-pill ' + s.cls} style={{ fontSize: 12 }}>{s.label}</span>}
        {empty && <span className="wf-tag">Có thể cho thuê</span>}
      </div>
      <div style={{ height: 32 }}>
        <div style={{ fontWeight: 700, fontSize: 15 }}>{r.tenant}</div>
        {!empty && <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{r.phone}</div>}
      </div>
      {!empty && (
        <>
          <div style={{ height: 1, background: 'var(--ink-3)', margin: '10px 0', opacity: 0.5 }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 8 }}>
            <span style={{ fontSize: 12, color: 'var(--ink-2)' }}>Tổng T11</span>
            <span className="wf-h3" style={{ fontSize: 18 }}>{formatVND(total)}đ</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'var(--paper-2)', border: '1.5px dashed var(--ink-3)', borderRadius: 6, padding: '4px 8px' }}>
            <span style={{ fontSize: 11, color: 'var(--ink-2)' }}>Điện:</span>
            <span style={{ fontFamily: 'var(--font-head)', fontSize: 15, color: 'var(--ink-3)' }}>{r.oldR}</span>
            <span style={{ color: 'var(--ink-3)' }}>→</span>
            <input style={{ width: 50, border: 'none', background: 'transparent', fontFamily: 'var(--font-head)', fontSize: 16, color: 'var(--accent)', outline: 'none' }} defaultValue={r.newR} readOnly />
            <span style={{ fontSize: 11, color: 'var(--ink-2)' }}>({r.newR - r.oldR})</span>
          </div>
          <div style={{ display: 'flex', gap: 4, marginTop: 8 }}>
            {r.status === 'unpaid' && <div className="wf-btn wf-btn-primary" style={{ padding: '3px 10px', fontSize: 13, flex: 1, justifyContent: 'center', boxShadow: 'none' }}>✓ Thu</div>}
            <div className="wf-btn" style={{ padding: '3px 10px', fontSize: 13, flex: 1, justifyContent: 'center', boxShadow: 'none' }}>🔲 QR</div>
            <div className="wf-btn" style={{ padding: '3px 10px', fontSize: 13, justifyContent: 'center', boxShadow: 'none' }}>⋯</div>
          </div>
        </>
      )}
      {empty && (
        <div className="wf-btn wf-btn-ghost" style={{ marginTop: 14, justifyContent: 'center', borderStyle: 'dashed', padding: 6, fontSize: 13 }}>+ Thêm khách thuê</div>
      )}
    </div>
  );
}

Object.assign(window, { V1Dashboard, V2BillsMasterDetail, V3RoomCardGrid });

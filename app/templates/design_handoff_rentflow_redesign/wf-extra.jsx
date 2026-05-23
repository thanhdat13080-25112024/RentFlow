// ────────────────────────────────────────────────────────────────
// V4: Hóa đơn — annual heatmap/timeline (12 tháng x N phòng)
// V5: Dashboard "Workflow-first" — batch actions hero
// V6: Mobile — bottom nav, card stack
// ────────────────────────────────────────────────────────────────

const ART_W2 = 1380;
const ART_H2 = 860;

// ════════════════════════════════════════════════════════════════
// V4 — ANNUAL HEATMAP
// One row per room, 12 columns = months, colored cell = status
// ════════════════════════════════════════════════════════════════
function V4Heatmap() {
  // 18 rooms, 12 months — fake some statuses
  const rooms = [];
  for (let f = 1; f <= 3; f++) {
    for (let i = 1; i <= 6; i++) {
      const num = `${f}0${i}`;
      const occupied = !(f === 1 && i === 4) && !(f === 2 && i === 6); // a couple empty
      rooms.push({ num, occupied, tenant: occupied ? sampleTenant(f, i) : '— trống —' });
    }
  }

  function cellStatus(room, month) {
    // Hypothetical current = Nov (11). Empty room → all empty.
    if (!room.occupied) return 'empty';
    if (month > 11) return 'future';
    // Some random "unpaid" for visual variety
    const seed = (parseInt(room.num) * 7 + month * 13) % 19;
    if (month === 11) {
      if (seed % 4 === 0) return 'unpaid';
      if (seed % 5 === 0) return 'prepaid';
      return 'paid';
    }
    if (seed % 11 === 0) return 'unpaid';
    if (seed % 7 === 0) return 'prepaid';
    return 'paid';
  }

  function cellColor(s) {
    return {
      paid:    'var(--ok)',
      unpaid:  'var(--accent)',
      prepaid: 'var(--info)',
      future:  'var(--paper-2)',
      empty:   'var(--paper-3)',
    }[s];
  }

  const months = Array.from({ length: 12 }, (_, i) => i + 1);

  return (
    <div className="wf-art" style={{ width: ART_W2, height: ART_H2 }}>
      <TopNav active="bills" />

      <div style={{ padding: '14px 24px', borderBottom: '1px dashed var(--ink-3)', display: 'flex', alignItems: 'center', gap: 14, background: 'var(--paper-2)' }}>
        <div className="wf-h2">Toàn cảnh năm 2025</div>
        <div className="wf-tag">◂ 2024</div>
        <div className="wf-tag" style={{ background: 'var(--ink)', color: 'var(--paper)', borderColor: 'var(--ink)' }}>2025</div>
        <div className="wf-tag">2026 ▸</div>
        <div style={{ flex: 1 }} />
        {/* Legend */}
        <div style={{ display: 'flex', gap: 12, fontSize: 13 }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}><span className="wf-dot" style={{ background: 'var(--ok)' }} /> Đã thu</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}><span className="wf-dot" style={{ background: 'var(--accent)' }} /> Chưa thu</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}><span className="wf-dot" style={{ background: 'var(--info)' }} /> Đóng trước</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}><span className="wf-dot empty" /> Trống/chưa tới</span>
        </div>
        <div className="wf-btn"><span>📤</span> Xuất Excel</div>
      </div>

      <div style={{ padding: 20, display: 'flex', gap: 20, height: ART_H2 - 130 }}>
        {/* Heatmap table */}
        <div className="wf-card" style={{ flex: 1, padding: 14, overflow: 'hidden' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '90px repeat(12, 1fr) 90px', gap: 6, alignItems: 'center' }}>
            <div className="wf-label">Phòng</div>
            {months.map(m => (
              <div key={m} className="wf-label" style={{ textAlign: 'center', color: m === 11 ? 'var(--accent)' : 'var(--ink-2)', fontWeight: m === 11 ? 700 : 400 }}>T{m}</div>
            ))}
            <div className="wf-label" style={{ textAlign: 'right' }}>Tổng năm</div>
          </div>
          <div style={{ height: 2, background: 'var(--ink)', margin: '6px 0' }} />

          {rooms.map(room => {
            // compute year total based on calc
            const yearTotal = months.reduce((sum, m) => {
              const s = cellStatus(room, m);
              if (s === 'paid' || s === 'prepaid') return sum + 4200000;
              return sum;
            }, 0);
            return (
              <div key={room.num} style={{ display: 'grid', gridTemplateColumns: '90px repeat(12, 1fr) 90px', gap: 6, alignItems: 'center', padding: '6px 0', borderBottom: '1px dashed var(--ink-3)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div className="wf-h3" style={{ fontSize: 18 }}>{room.num}</div>
                  <div style={{ fontSize: 11, color: 'var(--ink-2)' }}>{room.tenant.split(' ').slice(-2).join(' ')}</div>
                </div>
                {months.map(m => {
                  const s = cellStatus(room, m);
                  const isCurrent = m === 11;
                  return (
                    <div key={m} style={{
                      height: 22,
                      background: cellColor(s),
                      border: isCurrent ? '2px solid var(--ink)' : '1px solid var(--ink-3)',
                      borderRadius: 4,
                      position: 'relative',
                    }}>
                      {s === 'unpaid' && isCurrent && <div style={{ position: 'absolute', top: -3, right: -3, width: 8, height: 8, background: 'var(--accent)', borderRadius: 999, border: '1.5px solid var(--ink)' }} />}
                    </div>
                  );
                })}
                <div style={{ textAlign: 'right', fontFamily: 'var(--font-head)', fontSize: 16 }}>
                  {yearTotal ? `${(yearTotal/1e6).toFixed(1)}M` : '—'}
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: hover detail / popover example */}
        <div style={{ width: 280, display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="wf-card" style={{ padding: 14 }}>
            <div className="wf-label" style={{ marginBottom: 6 }}>Đã chọn ô</div>
            <div className="wf-h2">P.201 · T11/2025</div>
            <div style={{ fontSize: 13, color: 'var(--ink-2)', marginBottom: 10 }}>Phạm Thị Dung · 0986…</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14, padding: '4px 0', borderBottom: '1px dashed var(--ink-3)' }}>
              <span>Tiền phòng</span><b>3.800.000đ</b>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14, padding: '4px 0', borderBottom: '1px dashed var(--ink-3)' }}>
              <span>Dịch vụ</span><b>250.000đ</b>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14, padding: '4px 0', borderBottom: '1px dashed var(--ink-3)' }}>
              <span>Điện (75 kWh)</span><b>300.000đ</b>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14, padding: '8px 0 4px' }}>
              <span className="wf-h3" style={{ fontSize: 16 }}>Tổng</span>
              <span className="wf-h2" style={{ color: 'var(--accent)' }}>4.350.000đ</span>
            </div>
            <span className="wf-pill wf-pill-red" style={{ marginTop: 8 }}>Chưa thu · 22 ngày</span>
            <div style={{ display: 'flex', gap: 6, marginTop: 12 }}>
              <div className="wf-btn wf-btn-primary" style={{ flex: 1, justifyContent: 'center', padding: '6px', fontSize: 13 }}>✓ Thu</div>
              <div className="wf-btn" style={{ flex: 1, justifyContent: 'center', padding: '6px', fontSize: 13 }}>🔲 QR</div>
            </div>
          </div>

          <div className="wf-card" style={{ padding: 14, background: 'var(--paper-2)' }}>
            <div className="wf-h3" style={{ marginBottom: 10 }}>Doanh thu 2025</div>
            <div className="wf-h1" style={{ fontSize: 30, color: 'var(--accent)' }}>578M</div>
            <div style={{ fontSize: 13, color: 'var(--ink-2)' }}>11 tháng · 165 hóa đơn thu</div>
            <div style={{ marginTop: 10, display: 'flex', gap: 6 }}>
              {[8, 6, 7, 9, 7, 8, 9, 10, 8, 9, 11].map((h, i) => (
                <div key={i} className="wf-bar" style={{ width: 14, height: h * 4 }} />
              ))}
            </div>
          </div>
        </div>
      </div>

      <StickyNote x={36} y={ART_H2 - 80} width={280}>
        ✏️ <b>Nhìn cả năm trong 1 lưới</b> — biết ngay ai chưa thu, đóng trước, hoặc trống. Click ô = popover bên phải. Tốt cho audit.
      </StickyNote>
    </div>
  );
}

function sampleTenant(f, i) {
  const names = ['Nguyễn Văn An', 'Trần Thị Bình', 'Lê Văn Cường', 'Phạm Thị Dung', 'Hoàng Văn Em', 'Vũ Thị Giang', 'Đỗ Văn Hùng', 'Bùi Thị Lan', 'Mai Văn Khoa'];
  return names[(f * 6 + i) % names.length];
}

// ════════════════════════════════════════════════════════════════
// V5 — DASHBOARD "WORKFLOW-FIRST"
// Hero stats + big action shortcuts for monthly batch work
// ════════════════════════════════════════════════════════════════
function V5WorkflowDashboard() {
  return (
    <div className="wf-art" style={{ width: ART_W2, height: ART_H2 }}>
      <TopNav active="dashboard" />

      <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 18, height: ART_H2 - 70, overflow: 'hidden' }}>
        {/* Hero — Tháng này */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 18 }}>
          <div className="wf-card" style={{ padding: 22, background: 'var(--ink)', color: 'var(--paper)', borderColor: 'var(--ink)' }}>
            <div className="wf-label" style={{ color: 'var(--paper-3)' }}>Kỳ thu hiện tại</div>
            <div className="wf-h1" style={{ fontSize: 44, color: 'var(--paper)', marginTop: 4 }}>Tháng 11 / 2025</div>
            <div style={{ display: 'flex', gap: 28, marginTop: 18 }}>
              <div>
                <div style={{ fontSize: 12, color: 'var(--paper-3)' }}>Dự kiến</div>
                <div className="wf-h2" style={{ color: 'var(--paper)', fontSize: 26 }}>61.8M</div>
              </div>
              <div>
                <div style={{ fontSize: 12, color: 'var(--paper-3)' }}>Đã thu</div>
                <div className="wf-h2" style={{ color: 'var(--ok-soft)', fontSize: 26 }}>45.2M</div>
              </div>
              <div>
                <div style={{ fontSize: 12, color: 'var(--paper-3)' }}>Còn lại</div>
                <div className="wf-h2" style={{ color: 'var(--accent)', fontSize: 26 }}>16.6M</div>
              </div>
              <div style={{ flex: 1 }} />
              <div style={{ width: 220, alignSelf: 'flex-end' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--paper-3)' }}>
                  <span>Tiến độ thu</span><span>73%</span>
                </div>
                <div style={{ height: 12, background: 'var(--paper-3)', borderRadius: 6, marginTop: 4, overflow: 'hidden', border: '1.5px solid var(--paper)' }}>
                  <div style={{ width: '73%', height: '100%', background: 'var(--ok)' }} />
                </div>
              </div>
            </div>
          </div>

          {/* Mini status */}
          <div className="wf-card" style={{ padding: 18 }}>
            <div className="wf-h3" style={{ marginBottom: 12 }}>Phân bố trạng thái</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <SketchDonut paid={11} unpaid={4} prepaid={3} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flex: 1 }}>
                <LegendRow color="var(--ok)" label="Đã thu" n={11} />
                <LegendRow color="var(--accent)" label="Chưa thu" n={4} />
                <LegendRow color="var(--info)" label="Đóng trước" n={3} />
              </div>
            </div>
          </div>
        </div>

        {/* Quick actions — workflow shortcuts */}
        <div>
          <div className="wf-h3" style={{ marginBottom: 10 }}>🎯 Việc cần làm tháng này</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14 }}>
            <ActionCard
              icon="⚡"
              title="Ghi số điện hàng loạt"
              sub="6 phòng chưa nhập điện T11"
              cta="Mở bảng nhập"
              urgent
            />
            <ActionCard
              icon="📨"
              title="Gửi hóa đơn QR"
              sub="cho 4 phòng chưa thu"
              cta="Tạo QR + Zalo"
            />
            <ActionCard
              icon="📅"
              title="Đóng trước nhiều tháng"
              sub="P.103 hỏi đóng 3 tháng"
              cta="Mở phòng"
            />
            <ActionCard
              icon="📥"
              title="Import CSV / sao lưu"
              sub="nhập dữ liệu cũ hoặc export"
              cta="Chọn file"
            />
          </div>
        </div>

        {/* Bottom: 2 columns */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18, flex: 1, minHeight: 0 }}>
          <div className="wf-card" style={{ padding: 18, overflow: 'hidden' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <div className="wf-h3">Doanh thu 12 tháng</div>
              <div className="wf-tag">↑ 12% YoY</div>
            </div>
            <SketchBarChart data={[
              { label: 'T12·24', v: 38e6 }, { label: 'T1', v: 40e6 }, { label: 'T2', v: 39e6 },
              { label: 'T3', v: 42e6 }, { label: 'T4', v: 43e6 }, { label: 'T5', v: 44e6 },
              { label: 'T6', v: 41e6 }, { label: 'T7', v: 43e6 }, { label: 'T8', v: 46e6 },
              { label: 'T9', v: 45e6 }, { label: 'T10', v: 51e6 }, { label: 'T11', v: 52e6 },
            ]} height={180} accentIdx={11} />
          </div>

          <div className="wf-card" style={{ padding: 18, overflow: 'hidden' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <div className="wf-h3">⚠ Phòng chưa thu</div>
              <div className="wf-pill wf-pill-red">4 phòng · 16.6M</div>
            </div>
            {SAMPLE_ROOMS.filter(r => r.status === 'unpaid').slice(0, 3).map(r => (
              <div key={r.num} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', borderBottom: '1px dashed var(--ink-3)' }}>
                <div className="wf-avatar" style={{ background: 'var(--accent-soft)', borderColor: 'var(--accent)', width: 32, height: 32, fontSize: 14 }}>{r.num}</div>
                <div style={{ flex: 1, fontSize: 14 }}>
                  <div style={{ fontWeight: 700 }}>{r.tenant}</div>
                  <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{r.phone} · {formatVND(calcTotal(r))}đ</div>
                </div>
                <div className="wf-btn" style={{ padding: '3px 8px', fontSize: 12, boxShadow: 'none' }}>Nhắc</div>
                <div className="wf-btn wf-btn-primary" style={{ padding: '3px 8px', fontSize: 12, boxShadow: 'none' }}>✓</div>
              </div>
            ))}
            <div style={{ display: 'flex', justifyContent: 'center', padding: '8px 0 0' }}>
              <span style={{ fontSize: 13, color: 'var(--accent)', textDecoration: 'underline' }}>Xem tất cả 4 phòng →</span>
            </div>
          </div>
        </div>
      </div>

      <StickyNote x={ART_W2 - 280} y={210} rotate={2} width={250}>
        ✏️ <b>Workflow-first</b>: dashboard không chỉ hiện số — mà chỉ ra <i>việc cần làm</i> tháng này (ghi điện, gửi QR, thu tiền…)
      </StickyNote>
    </div>
  );
}

function ActionCard({ icon, title, sub, cta, urgent }) {
  return (
    <div className="wf-card" style={{ padding: 16, position: 'relative', borderColor: urgent ? 'var(--accent)' : 'var(--ink)', background: urgent ? 'var(--accent-soft)' : 'var(--paper)' }}>
      <div style={{ fontSize: 28, marginBottom: 6 }}>{icon}</div>
      <div className="wf-h3" style={{ fontSize: 17, marginBottom: 4 }}>{title}</div>
      <div style={{ fontSize: 13, color: 'var(--ink-2)', marginBottom: 12, minHeight: 32 }}>{sub}</div>
      <div className={'wf-btn' + (urgent ? ' wf-btn-primary' : '')} style={{ width: '100%', justifyContent: 'center', boxShadow: urgent ? '2px 2px 0 var(--ink)' : 'none', padding: '6px' }}>{cta} →</div>
      {urgent && <div className="wf-pill wf-pill-red" style={{ position: 'absolute', top: -10, right: 10, fontSize: 11 }}>cần xử lý</div>}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════
// V6 — MOBILE: 3 phone screens side by side
// ════════════════════════════════════════════════════════════════
function V6Mobile() {
  return (
    <div className="wf-art" style={{ width: 1380, height: 860, padding: 30, display: 'flex', flexDirection: 'column', gap: 18 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 16 }}>
        <div className="wf-h1" style={{ fontSize: 32 }}>📱 Mobile layout</div>
        <div style={{ color: 'var(--ink-2)' }}>Card stack + bottom nav. Bảng 12 cột hiện tại không dùng được trên điện thoại.</div>
      </div>
      <div style={{ display: 'flex', gap: 36, justifyContent: 'center', flex: 1 }}>
        <PhoneDashboard />
        <PhoneBillList />
        <PhoneBillDetail />
      </div>
    </div>
  );
}

function PhoneShell({ children, title }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10 }}>
      <div className="wf-phone">
        <div className="wf-phone-notch" />
        {children}
      </div>
      <div className="wf-h3" style={{ fontSize: 17, color: 'var(--ink-2)' }}>{title}</div>
    </div>
  );
}

function MobileNav({ active }) {
  const items = [
    { id: 'dashboard', label: 'Tổng quan', icon: '◧' },
    { id: 'rooms',     label: 'Phòng',     icon: '⌂' },
    { id: 'bills',     label: 'Hóa đơn',   icon: '₫' },
    { id: 'more',      label: 'Khác',      icon: '⋯' },
  ];
  return (
    <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, borderTop: '2px solid var(--ink)', background: 'var(--paper)', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', padding: '6px 0 14px' }}>
      {items.map(it => (
        <div key={it.id} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, color: active === it.id ? 'var(--accent)' : 'var(--ink-2)' }}>
          <span style={{ fontSize: 20 }}>{it.icon}</span>
          <span style={{ fontSize: 11, fontWeight: active === it.id ? 700 : 400 }}>{it.label}</span>
        </div>
      ))}
    </div>
  );
}

function PhoneTopBar({ title, sub }) {
  return (
    <div style={{ padding: '32px 16px 12px', borderBottom: '1px dashed var(--ink-3)', background: 'var(--paper)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div className="wf-h2" style={{ fontSize: 22 }}>{title}</div>
          {sub && <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{sub}</div>}
        </div>
        <div className="wf-tag" style={{ fontSize: 11, padding: '3px 8px' }}>◂ T11/25 ▸</div>
      </div>
    </div>
  );
}

function PhoneDashboard() {
  return (
    <PhoneShell title="Tổng quan">
      <PhoneTopBar title="Quản Lý Trọ" sub="Chào Cô Lan 👋" />
      <div style={{ padding: 14, display: 'flex', flexDirection: 'column', gap: 10, height: 'calc(100% - 130px)', overflow: 'hidden' }}>
        {/* Hero */}
        <div className="wf-card" style={{ padding: 12, background: 'var(--ink)', color: 'var(--paper)', borderColor: 'var(--ink)' }}>
          <div style={{ fontSize: 11, color: 'var(--paper-3)' }}>ĐÃ THU THÁNG 11</div>
          <div className="wf-h1" style={{ fontSize: 26, color: 'var(--paper)' }}>45.2M / 61.8M</div>
          <div style={{ height: 8, background: 'var(--paper-3)', borderRadius: 4, marginTop: 6, overflow: 'hidden' }}>
            <div style={{ width: '73%', height: '100%', background: 'var(--ok)' }} />
          </div>
          <div style={{ fontSize: 11, color: 'var(--paper-3)', marginTop: 4 }}>73% · còn 4 phòng chưa thu</div>
        </div>

        {/* 2x2 stats */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          <MiniStat label="Tổng phòng" value="18" />
          <MiniStat label="Đã thu" value="11" accent="var(--ok)" />
          <MiniStat label="Chưa thu" value="4" accent="var(--accent)" />
          <MiniStat label="Đóng trước" value="3" accent="var(--info)" />
        </div>

        {/* Chú ý */}
        <div style={{ marginTop: 4 }}>
          <div className="wf-h3" style={{ fontSize: 14, marginBottom: 6 }}>⚠ Cần thu</div>
          {SAMPLE_ROOMS.filter(r => r.status === 'unpaid').slice(0, 2).map(r => (
            <div key={r.num} className="wf-card-soft" style={{ padding: 8, marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8, borderColor: 'var(--accent)', background: 'var(--accent-soft)' }}>
              <div className="wf-avatar" style={{ width: 28, height: 28, fontSize: 12, background: 'var(--paper)', borderColor: 'var(--accent)' }}>{r.num}</div>
              <div style={{ flex: 1, fontSize: 12 }}>
                <div style={{ fontWeight: 700 }}>{r.tenant}</div>
                <div style={{ color: 'var(--ink-2)' }}>{formatVND(calcTotal(r))}đ</div>
              </div>
              <div className="wf-btn wf-btn-primary" style={{ padding: '2px 8px', fontSize: 11, boxShadow: 'none' }}>✓</div>
            </div>
          ))}
        </div>
      </div>
      <MobileNav active="dashboard" />
    </PhoneShell>
  );
}

function MiniStat({ label, value, accent }) {
  return (
    <div className="wf-card-soft" style={{ padding: 8 }}>
      <div style={{ fontSize: 10, color: 'var(--ink-2)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</div>
      <div className="wf-h2" style={{ fontSize: 22, color: accent || 'var(--ink)' }}>{value}</div>
    </div>
  );
}

function PhoneBillList() {
  return (
    <PhoneShell title="Hóa đơn tháng — card stack">
      <PhoneTopBar title="Hóa đơn T11" sub="15 phòng đang thuê" />
      <div style={{ padding: '10px 14px 8px', background: 'var(--paper)' }}>
        <div className="wf-input" style={{ fontSize: 13, color: 'var(--ink-3)', padding: '5px 10px' }}>⌕ Tìm phòng / khách</div>
        <div style={{ display: 'flex', gap: 4, padding: 3, border: '1.5px solid var(--ink)', borderRadius: 6, background: 'var(--paper-2)', marginTop: 8 }}>
          {['Tất cả', 'Chưa thu', 'Đã thu'].map((t, i) => (
            <div key={t} className={'wf-tab' + (i === 1 ? ' active' : '')} style={{ fontSize: 13, padding: '3px 8px', flex: 1, textAlign: 'center' }}>{t}</div>
          ))}
        </div>
      </div>

      <div style={{ padding: '4px 14px 70px', height: 'calc(100% - 200px)', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: 8 }}>
        {SAMPLE_ROOMS.filter(r => r.status !== 'empty').slice(0, 4).map((r, i) => (
          <MobileBillCard key={r.num} r={r} selected={i === 0} />
        ))}
      </div>
      <MobileNav active="bills" />
    </PhoneShell>
  );
}

function MobileBillCard({ r, selected }) {
  const total = calcTotal(r);
  const statusMap = {
    unpaid:  { cls: 'wf-pill-red',   label: 'Chưa thu' },
    paid:    { cls: 'wf-pill-green', label: 'Đã thu' },
    prepaid: { cls: 'wf-pill-blue',  label: 'Đóng trước' },
  };
  const s = statusMap[r.status];

  return (
    <div className="wf-card" style={{ padding: 10, position: 'relative', borderColor: selected ? 'var(--accent)' : 'var(--ink)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
        <div className="wf-h2" style={{ fontSize: 24, color: 'var(--accent)' }}>{r.num}</div>
        <div style={{ flex: 1, fontSize: 13 }}>
          <div style={{ fontWeight: 700 }}>{r.tenant}</div>
          <div style={{ color: 'var(--ink-2)', fontSize: 11 }}>{r.phone}</div>
        </div>
        <span className={'wf-pill ' + s.cls} style={{ fontSize: 11, padding: '2px 8px' }}>{s.label}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '4px 0', borderTop: '1px dashed var(--ink-3)' }}>
        <span style={{ fontSize: 11, color: 'var(--ink-2)' }}>Điện {r.newR - r.oldR} kWh</span>
        <span className="wf-h2" style={{ fontSize: 20 }}>{formatVND(total)}đ</span>
      </div>
      {selected && (
        <div style={{ display: 'flex', gap: 4, marginTop: 6 }}>
          <div className="wf-btn wf-btn-primary" style={{ flex: 1, fontSize: 11, padding: '4px', justifyContent: 'center', boxShadow: 'none' }}>✓ Thu tiền</div>
          <div className="wf-btn" style={{ flex: 1, fontSize: 11, padding: '4px', justifyContent: 'center', boxShadow: 'none' }}>🔲 QR</div>
          <div className="wf-btn" style={{ fontSize: 11, padding: '4px 8px', boxShadow: 'none' }}>⋯</div>
        </div>
      )}
    </div>
  );
}

function PhoneBillDetail() {
  const r = SAMPLE_ROOMS[0];
  const elecUsage = r.newR - r.oldR;
  return (
    <PhoneShell title="Chi tiết phòng + chỉnh sửa">
      <div style={{ padding: '32px 14px 10px', background: 'var(--accent-soft)', borderBottom: '2px solid var(--ink)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <span style={{ fontSize: 20 }}>‹</span>
          <span style={{ fontSize: 13, color: 'var(--ink-2)' }}>Hóa đơn T11</span>
          <div style={{ flex: 1 }} />
          <span style={{ fontSize: 18 }}>⋮</span>
        </div>
        <div className="wf-h1" style={{ fontSize: 36, color: 'var(--accent)' }}>P.{r.num}</div>
        <div style={{ fontWeight: 700 }}>{r.tenant}</div>
        <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{r.phone} · ngày thuê 15/03/2024</div>
      </div>

      <div style={{ padding: 12, height: 'calc(100% - 270px)', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: 10 }}>
        <div className="wf-card-soft" style={{ padding: 10, background: 'var(--paper-2)' }}>
          <div style={{ fontSize: 11, color: 'var(--ink-2)', textTransform: 'uppercase' }}>Số điện</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
            <div style={{ flex: 1, fontSize: 13 }}>Cũ: <b style={{ color: 'var(--ink-3)' }}>{r.oldR}</b></div>
            <div style={{ flex: 1, fontSize: 13 }}>Mới: <b className="wf-input" style={{ padding: '2px 8px', display: 'inline-block', color: 'var(--accent)' }}>{r.newR}</b></div>
            <div className="wf-pill wf-pill-blue" style={{ fontSize: 11, padding: '2px 6px' }}>{elecUsage} kWh</div>
          </div>
        </div>

        <div className="wf-card-soft" style={{ padding: 10 }}>
          {[['Phòng', r.rent], ['Dịch vụ', r.service], ['Điện', elecUsage * ELECTRIC_PRICE]].map(([k, v]) => (
            <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', borderBottom: '1px dashed var(--ink-3)', fontSize: 13 }}>
              <span>{k}</span><b>{formatVND(v)}đ</b>
            </div>
          ))}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', padding: '6px 0 0' }}>
            <span className="wf-h3" style={{ fontSize: 15 }}>Tổng</span>
            <span className="wf-h1" style={{ fontSize: 22, color: 'var(--accent)' }}>{formatVND(calcTotal(r))}đ</span>
          </div>
        </div>

        <div className="wf-btn wf-btn-primary" style={{ justifyContent: 'center', padding: '10px', fontSize: 15 }}>✓ Đánh dấu đã thu</div>
        <div style={{ display: 'flex', gap: 6 }}>
          <div className="wf-btn" style={{ flex: 1, justifyContent: 'center', padding: '8px', fontSize: 13 }}>📅 Đóng trước</div>
          <div className="wf-btn" style={{ flex: 1, justifyContent: 'center', padding: '8px', fontSize: 13 }}>🔲 QR</div>
        </div>
      </div>
      <MobileNav active="bills" />
    </PhoneShell>
  );
}

Object.assign(window, { V4Heatmap, V5WorkflowDashboard, V6Mobile });

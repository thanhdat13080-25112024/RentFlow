// ────────────────────────────────────────────────────────────────
// Shared sketchy primitives + sample data for all wireframe variants.
// ────────────────────────────────────────────────────────────────

// Sample data (consistent across variations so users can compare)
const SAMPLE_ROOMS = [
  { num: '101', tenant: 'Nguyễn Văn An',     phone: '0912 345 678', rent: 3500000, service: 200000, oldR: 1240, newR: 1318, status: 'unpaid',  floor: 1 },
  { num: '102', tenant: 'Trần Thị Bình',     phone: '0903 222 111', rent: 3500000, service: 200000, oldR: 980,  newR: 1052, status: 'paid',    floor: 1 },
  { num: '103', tenant: 'Lê Văn Cường',      phone: '0977 888 999', rent: 3200000, service: 200000, oldR: 1100, newR: 1140, status: 'prepaid', floor: 1 },
  { num: '104', tenant: '— Trống —',         phone: '',             rent: 0,       service: 0,      oldR: 0,    newR: 0,    status: 'empty',   floor: 1 },
  { num: '201', tenant: 'Phạm Thị Dung',     phone: '0986 543 210', rent: 3800000, service: 250000, oldR: 1456, newR: 1531, status: 'unpaid',  floor: 2 },
  { num: '202', tenant: 'Hoàng Văn Em',      phone: '0922 333 444', rent: 3800000, service: 250000, oldR: 1023, newR: 1098, status: 'paid',    floor: 2 },
  { num: '203', tenant: 'Vũ Thị Giang',      phone: '0911 222 333', rent: 3500000, service: 250000, oldR: 1334, newR: 1402, status: 'unpaid',  floor: 2 },
  { num: '301', tenant: 'Đỗ Văn Hùng',       phone: '0966 777 888', rent: 4000000, service: 250000, oldR: 1701, newR: 1789, status: 'paid',    floor: 3 },
];

const ELECTRIC_PRICE = 4000;

function formatVND(n) {
  if (!n) return '0';
  return n.toLocaleString('vi-VN');
}

function calcTotal(r) {
  if (r.status === 'empty') return 0;
  const elec = (r.newR - r.oldR) * ELECTRIC_PRICE;
  return r.rent + r.service + elec;
}

// ────────────────────────────────────────────────────────────────
// Top navigation bar — reused across all desktop variants
// ────────────────────────────────────────────────────────────────
function TopNav({ active = 'dashboard', month = 11, year = 2025, showSearch = true, width }) {
  const tabs = [
    { id: 'dashboard', label: 'Tổng quan' },
    { id: 'rooms',     label: 'Phòng & Khách' },
    { id: 'bills',     label: 'Hóa đơn tháng' },
    { id: 'revenue',   label: 'Doanh thu' },
    { id: 'settings',  label: 'Cài đặt' },
  ];
  return (
    <div style={{ borderBottom: '2px solid var(--ink)', background: 'var(--paper)', padding: '14px 28px', display: 'flex', alignItems: 'center', gap: 24 }}>
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{ width: 36, height: 36, border: '2px solid var(--ink)', borderRadius: 8, background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '2px 2px 0 var(--ink)' }}>
          <span style={{ fontFamily: 'var(--font-head)', fontSize: 22, color: 'white' }}>⌂</span>
        </div>
        <div className="wf-h3" style={{ letterSpacing: '0.02em' }}>Quản&nbsp;Lý&nbsp;Trọ</div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginLeft: 12 }}>
        {tabs.map(t => (
          <div key={t.id} className={'wf-tab' + (active === t.id ? ' active' : '')}>{t.label}</div>
        ))}
      </div>

      <div style={{ flex: 1 }} />

      {/* Search */}
      {showSearch && (
        <div className="wf-input" style={{ display: 'flex', alignItems: 'center', gap: 8, width: 230, color: 'var(--ink-3)', whiteSpace: 'nowrap', flexShrink: 0 }}>
          <span>⌕</span>
          <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>Tìm phòng, khách…</span>
          <span style={{ marginLeft: 'auto', fontFamily: 'monospace', fontSize: 11, color: 'var(--ink-3)' }}>⌘K</span>
        </div>
      )}

      {/* Month nav */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, border: '2px solid var(--ink)', borderRadius: 8, padding: '4px 6px', background: 'var(--paper-2)', flexShrink: 0 }}>
        <div style={{ width: 26, height: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1.5px solid var(--ink)', borderRadius: 5, background: 'var(--paper)' }}>‹</div>
        <div className="wf-head" style={{ fontSize: 19, padding: '0 10px' }}>Th.{month}/{year}</div>
        <div style={{ width: 26, height: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1.5px solid var(--ink)', borderRadius: 5, background: 'var(--paper)' }}>›</div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────────────────────
// Sticky note annotation
// ────────────────────────────────────────────────────────────────
function StickyNote({ children, x, y, rotate = -1.5, width = 200, side = 'left' }) {
  return (
    <div className="wf-note" style={{
      position: 'absolute',
      left: x, top: y,
      width,
      transform: `rotate(${rotate}deg)`,
      zIndex: 5,
    }}>{children}</div>
  );
}

// ────────────────────────────────────────────────────────────────
// Sketchy stat tile
// ────────────────────────────────────────────────────────────────
function StatTile({ label, value, sub, accent, icon = '◧' }) {
  return (
    <div className="wf-card" style={{ padding: '14px 16px', flex: 1, minWidth: 0 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
        <div className="wf-label">{label}</div>
        <div style={{ width: 28, height: 28, borderRadius: 6, border: '1.5px solid var(--ink)', background: accent || 'var(--paper-2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: accent ? 'white' : 'var(--ink)' }}>{icon}</div>
      </div>
      <div className="wf-h1" style={{ fontSize: 32, color: accent === 'var(--accent)' ? 'var(--accent)' : 'var(--ink)' }}>{value}</div>
      {sub && <div style={{ fontSize: 13, color: 'var(--ink-2)', marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

// ────────────────────────────────────────────────────────────────
// Sketchy bar chart (revenue trend)
// ────────────────────────────────────────────────────────────────
function SketchBarChart({ data, height = 160, accentIdx = -1 }) {
  const max = Math.max(...data.map(d => d.v));
  return (
    <div style={{ position: 'relative', height, display: 'flex', alignItems: 'flex-end', gap: 12, padding: '0 8px', borderBottom: '2px solid var(--ink)' }}>
      {data.map((d, i) => {
        const h = (d.v / max) * (height - 30);
        return (
          <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
            <div className="wf-mono" style={{ fontSize: 10, color: 'var(--ink-2)' }}>{(d.v/1e6).toFixed(0)}M</div>
            <div className={'wf-bar' + (i === accentIdx ? ' accent' : (d.dim ? ' soft' : ''))} style={{
              width: '70%',
              height: h,
              border: '1.5px solid var(--ink)',
            }} />
            <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>{d.label}</div>
          </div>
        );
      })}
    </div>
  );
}

// ────────────────────────────────────────────────────────────────
// Sketchy donut (paid vs unpaid)
// ────────────────────────────────────────────────────────────────
function SketchDonut({ paid = 12, unpaid = 4, prepaid = 2 }) {
  const total = paid + unpaid + prepaid;
  const r = 60;
  const c = 2 * Math.PI * r;
  const seg = (n) => (n / total) * c;
  let offset = 0;
  const segments = [
    { len: seg(paid),    color: 'var(--ok)' },
    { len: seg(unpaid),  color: 'var(--accent)' },
    { len: seg(prepaid), color: 'var(--info)' },
  ];
  return (
    <div style={{ position: 'relative', width: 160, height: 160 }}>
      <svg viewBox="0 0 160 160" width="160" height="160">
        <circle cx="80" cy="80" r={r} fill="none" stroke="var(--paper-3)" strokeWidth="22" />
        {segments.map((s, i) => {
          const el = (
            <circle key={i} cx="80" cy="80" r={r} fill="none"
              stroke={s.color} strokeWidth="22"
              strokeDasharray={`${s.len} ${c}`}
              strokeDashoffset={-offset}
              transform="rotate(-90 80 80)"
            />
          );
          offset += s.len;
          return el;
        })}
        <circle cx="80" cy="80" r={r} fill="none" stroke="var(--ink)" strokeWidth="1.5" opacity="0.4" />
      </svg>
      <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div className="wf-h2" style={{ fontSize: 28 }}>{Math.round(paid/total*100)}%</div>
        <div style={{ fontSize: 12, color: 'var(--ink-2)' }}>đã thu</div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────────────────────
// Expose to other Babel scripts
// ────────────────────────────────────────────────────────────────
Object.assign(window, {
  SAMPLE_ROOMS, ELECTRIC_PRICE, formatVND, calcTotal,
  TopNav, StickyNote, StatTile, SketchBarChart, SketchDonut,
});

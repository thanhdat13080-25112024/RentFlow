// RentFlow web — shared data + components for the marketing/listings site.

function WIcon({ name, size = 20, color, strokeWidth = 1.75, style = {} }) {
  return <i data-lucide={name} style={{ width: size, height: size, display: 'inline-flex', color: color || 'currentColor', ...style }} />;
}

const WEB_LISTINGS = [
  { id: 'w1', title: 'Sunlit 2-bedroom near West Lake', area: 'Tây Hồ', price: 6500000, beds: 2, baths: 1, m2: 68, rating: 4.9, tag: 'Verified', seed: 'rfweb11' },
  { id: 'w2', title: 'Quiet studio with balcony', area: 'Hai Bà Trưng', price: 9200000, beds: 1, baths: 1, m2: 42, rating: 4.8, tag: 'New', seed: 'rfweb22' },
  { id: 'w3', title: 'Family flat with garden view', area: 'Cầu Giấy', price: 12800000, beds: 3, baths: 2, m2: 96, rating: 4.95, tag: 'Verified', seed: 'rfweb33' },
  { id: 'w4', title: 'Loft above a coffee lane', area: 'Đống Đa', price: 7400000, beds: 1, baths: 1, m2: 55, rating: 4.7, tag: 'Pet friendly', seed: 'rfweb44' },
  { id: 'w5', title: 'Bright corner unit, river side', area: 'Long Biên', price: 8100000, beds: 2, baths: 1, m2: 61, rating: 4.85, tag: 'Verified', seed: 'rfweb55' },
  { id: 'w6', title: 'Townhouse with rooftop', area: 'Ba Đình', price: 18500000, beds: 4, baths: 3, m2: 140, rating: 4.92, tag: 'New', seed: 'rfweb66' },
];

function WButton({ children, variant = 'primary', size = 'md', icon, onClick, style = {} }) {
  const [press, setPress] = React.useState(false);
  const variants = {
    primary: { background: 'var(--accent)', color: 'var(--accent-on)', border: '1px solid var(--accent)' },
    secondary: { background: 'var(--surface)', color: 'var(--ink-1)', border: '1px solid var(--line-strong)' },
    ghost: { background: 'transparent', color: 'var(--ink-1)', border: '1px solid transparent' },
    invert: { background: 'var(--paper)', color: 'var(--ink)', border: '1px solid var(--paper)' },
  };
  return (
    <button onClick={onClick} onMouseDown={() => setPress(true)} onMouseUp={() => setPress(false)} onMouseLeave={() => setPress(false)}
      style={{
        fontFamily: 'var(--font-sans)', fontWeight: 700, cursor: 'pointer', borderRadius: 'var(--r-md)',
        display: 'inline-flex', alignItems: 'center', gap: 8, transition: 'all var(--dur) var(--ease)',
        transform: press ? 'scale(.98)' : 'scale(1)', whiteSpace: 'nowrap',
        fontSize: size === 'lg' ? 17 : 15, padding: size === 'lg' ? '15px 26px' : '11px 20px',
        ...variants[variant], ...style,
      }}>
      {children}{icon && <WIcon name={icon} size={18} />}
    </button>
  );
}

function WNav({ view, setView }) {
  const link = (id, label) => (
    <button onClick={() => setView(id)} style={{
      background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'var(--font-sans)',
      fontSize: 16, fontWeight: view === id ? 700 : 500,
      color: view === id ? 'var(--ink)' : 'var(--ink-2)', padding: '6px 0',
    }}>{label}</button>
  );
  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 30, background: 'rgba(240,240,236,.82)',
      backdropFilter: 'blur(14px)', borderBottom: '1px solid var(--line)',
    }}>
      <div style={{ maxWidth: 1240, margin: '0 auto', padding: '0 40px', height: 76, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div onClick={() => setView('home')} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
          <img src="../../assets/rentflow-wordmark.png" alt="rentflow" style={{ height: 26, display: 'block' }} />
        </div>
        <nav style={{ display: 'flex', gap: 34, alignItems: 'center' }}>
          {link('browse', 'Browse')}
          {link('home', 'How it works')}
          {link('home', 'List your home')}
          {link('home', 'Help')}
        </nav>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <WButton variant="ghost">Sign in</WButton>
          <WButton variant="primary" icon="arrow-right">Get started</WButton>
        </div>
      </div>
    </header>
  );
}

function WListingCard({ item, onOpen }) {
  const [hover, setHover] = React.useState(false);
  const [fav, setFav] = React.useState(false);
  return (
    <div onClick={onOpen} onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        background: 'var(--surface)', border: '1px solid var(--line)', borderRadius: 'var(--r-lg)',
        overflow: 'hidden', cursor: 'pointer', transition: 'all var(--dur) var(--ease)',
        boxShadow: hover ? 'var(--shadow-md)' : 'var(--shadow-sm)',
        transform: hover ? 'translateY(-3px)' : 'none',
      }}>
      <div style={{ position: 'relative', height: 210, background: 'var(--paper-2)' }}>
        <img src={`https://picsum.photos/seed/${item.seed}/720/440`} alt=""
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(.92)' }} />
        <span style={{
          position: 'absolute', top: 14, left: 14, fontFamily: 'var(--font-cond)', fontWeight: 700,
          fontSize: 12, letterSpacing: '.07em', textTransform: 'uppercase', background: 'var(--surface)',
          color: item.tag === 'Verified' ? 'var(--success)' : 'var(--accent-strong)',
          padding: '5px 11px', borderRadius: 'var(--r-sm)',
        }}>{item.tag}</span>
        <div onClick={(e) => { e.stopPropagation(); setFav(!fav); }} style={{
          position: 'absolute', top: 14, right: 14, width: 40, height: 40, borderRadius: 'var(--r-pill)',
          background: 'rgba(251,251,249,.92)', backdropFilter: 'blur(4px)', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
        }}>
          <WIcon name="heart" size={19} color={fav ? 'var(--danger)' : 'var(--ink-1)'} style={fav ? { fill: 'var(--danger)' } : {}} />
        </div>
      </div>
      <div style={{ padding: '17px 19px 19px' }}>
        <div style={{ fontFamily: 'var(--font-cond)', fontWeight: 700, fontSize: 27, color: 'var(--ink)', lineHeight: 1 }}>
          ₫{item.price.toLocaleString('en-US')}
          <span style={{ fontFamily: 'var(--font-sans)', fontWeight: 400, fontSize: 15, color: 'var(--ink-3)' }}>/mo</span>
        </div>
        <div style={{ fontWeight: 700, fontSize: 18, color: 'var(--ink-1)', marginTop: 8 }}>{item.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 5, color: 'var(--ink-3)', fontSize: 14, marginTop: 4 }}>
          <WIcon name="map-pin" size={14} />{item.area}, Hà Nội
        </div>
        <div style={{ display: 'flex', gap: 16, marginTop: 14, paddingTop: 14, borderTop: '1px solid var(--line)', fontFamily: 'var(--font-cond)', fontWeight: 500, fontSize: 15, color: 'var(--ink-2)', whiteSpace: 'nowrap' }}>
          <span><b style={{ color: 'var(--ink-1)' }}>{item.beds}</b> bed</span>
          <span><b style={{ color: 'var(--ink-1)' }}>{item.baths}</b> bath</span>
          <span><b style={{ color: 'var(--ink-1)' }}>{item.m2}</b> m²</span>
          <span style={{ marginLeft: 'auto' }}><b style={{ color: 'var(--ink-1)' }}>{item.rating}</b> ★</span>
        </div>
      </div>
    </div>
  );
}

function WFooter() {
  const col = (title, links) => (
    <div>
      <div className="rf-overline" style={{ marginBottom: 16 }}>{title}</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
        {links.map(l => <a key={l} href="#" onClick={e => e.preventDefault()} style={{ color: 'var(--ink-2)', fontSize: 15, textDecoration: 'none' }}>{l}</a>)}
      </div>
    </div>
  );
  return (
    <footer style={{ background: 'var(--ink)', color: 'var(--on-dark)', padding: '64px 40px 40px' }}>
      <div style={{ maxWidth: 1240, margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: 40 }}>
          <div>
            <img src="../../assets/rentflow-mark-white.png" alt="" style={{ height: 40, marginBottom: 16 }} />
            <p style={{ color: 'rgba(240,240,236,.7)', fontSize: 15, lineHeight: 1.6, maxWidth: 280, margin: 0 }}>
              Streamline housing. Find, tour, and lease a home in Hà Nội — calmly.
            </p>
          </div>
          {col('Renters', ['Browse homes', 'Saved homes', 'Book a tour', 'How it works'])}
          {col('Hosts', ['List your home', 'Host dashboard', 'Pricing', 'Resources'])}
          {col('Company', ['About', 'Careers', 'Privacy', 'Contact'])}
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 48, paddingTop: 24, borderTop: '1px solid rgba(240,240,236,.16)' }}>
          <span style={{ fontFamily: 'var(--font-cond)', fontWeight: 700, letterSpacing: '.12em', fontSize: 13, color: 'rgba(240,240,236,.6)' }}>EST 2026 · HÀ NỘI, VNA</span>
          <span style={{ color: 'rgba(240,240,236,.6)', fontSize: 14 }}>© 2026 RentFlow</span>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { WIcon, WEB_LISTINGS, WButton, WNav, WListingCard, WFooter });

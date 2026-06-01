// RentFlow web — page sections and views.

// Big search hero
function WHero({ onSearch }) {
  const [seg, setSeg] = React.useState('Rent');
  return (
    <section style={{ maxWidth: 1240, margin: '0 auto', padding: '72px 40px 40px' }}>
      <div className="rf-overline" style={{ marginBottom: 20 }}>Hà Nội · 1,200+ verified homes</div>
      <h1 style={{
        fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 76, lineHeight: .98,
        letterSpacing: '-.02em', color: 'var(--ink)', margin: 0, maxWidth: 900,
      }}>Find a home you'll<br />actually love.</h1>
      <p className="rf-lead" style={{ marginTop: 22, maxWidth: 560 }}>
        Streamline the search, the tour, and the lease — all in one calm, focused place.
      </p>

      {/* search bar */}
      <div style={{
        marginTop: 36, background: 'var(--surface)', border: '1px solid var(--line-strong)',
        borderRadius: 'var(--r-lg)', boxShadow: 'var(--shadow-md)', padding: 10,
        display: 'flex', alignItems: 'center', gap: 4, maxWidth: 880,
      }}>
        <div style={{ display: 'inline-flex', background: 'var(--paper-2)', borderRadius: 'var(--r-pill)', padding: 4, gap: 2, marginRight: 6 }}>
          {['Rent', 'Buy', 'Short stay'].map(s => (
            <button key={s} onClick={() => setSeg(s)} style={{
              fontFamily: 'var(--font-sans)', fontWeight: 700, fontSize: 14, border: 'none',
              padding: '9px 16px', borderRadius: 'var(--r-pill)', cursor: 'pointer',
              background: seg === s ? 'var(--surface)' : 'transparent',
              color: seg === s ? 'var(--ink)' : 'var(--ink-2)', boxShadow: seg === s ? 'var(--shadow-sm)' : 'none',
            }}>{s}</button>
          ))}
        </div>
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 10, padding: '0 12px' }}>
          <WIcon name="search" size={20} color="var(--ink-3)" />
          <span style={{ color: 'var(--ink-3)', fontSize: 17 }}>Neighborhood, street, or area in Hà Nội</span>
        </div>
        <WButton variant="primary" size="lg" icon="arrow-right" onClick={onSearch}>Search</WButton>
      </div>

      {/* trust row */}
      <div style={{ display: 'flex', gap: 32, marginTop: 28, color: 'var(--ink-2)', fontSize: 15 }}>
        {[['shield-check', 'Verified listings'], ['calendar-check', 'Two-tap tours'], ['file-check', 'Digital leases']].map(([ic, t]) => (
          <span key={t} style={{ display: 'flex', alignItems: 'center', gap: 8 }}><WIcon name={ic} size={18} color="var(--accent)" />{t}</span>
        ))}
      </div>
    </section>
  );
}

// Featured listings band
function WFeatured({ onOpen, onBrowse }) {
  return (
    <section style={{ maxWidth: 1240, margin: '0 auto', padding: '40px 40px 24px' }}>
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', marginBottom: 24 }}>
        <div>
          <div className="rf-overline" style={{ marginBottom: 8 }}>Newly listed</div>
          <h2 className="rf-h2">Homes in Tây Hồ &amp; nearby</h2>
        </div>
        <WButton variant="secondary" icon="arrow-right" onClick={onBrowse}>See all homes</WButton>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
        {WEB_LISTINGS.slice(0, 3).map(item => <WListingCard key={item.id} item={item} onOpen={() => onOpen(item)} />)}
      </div>
    </section>
  );
}

// How it works
function WHowItWorks() {
  const steps = [
    { icon: 'search', title: 'Search calmly', body: 'Filter verified homes by area, budget, and what matters to you — no clutter.' },
    { icon: 'calendar', title: 'Book a tour', body: 'Pick a time in two taps. We confirm with the host and remind you before.' },
    { icon: 'file-check', title: 'Sign & move in', body: 'Apply, sign the lease digitally, and pay your deposit securely in-app.' },
  ];
  return (
    <section style={{ background: 'var(--surface)', borderTop: '1px solid var(--line)', borderBottom: '1px solid var(--line)', marginTop: 32 }}>
      <div style={{ maxWidth: 1240, margin: '0 auto', padding: '72px 40px' }}>
        <div className="rf-overline" style={{ marginBottom: 10 }}>How RentFlow works</div>
        <h2 className="rf-h2" style={{ marginBottom: 44, maxWidth: 620 }}>Three calm steps from searching to keys.</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 32 }}>
          {steps.map((s, i) => (
            <div key={i}>
              <div style={{
                width: 56, height: 56, borderRadius: 'var(--r-md)', background: 'var(--accent-tint)',
                display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 18,
              }}><WIcon name={s.icon} size={26} color="var(--accent-strong)" /></div>
              <div style={{ fontFamily: 'var(--font-cond)', fontWeight: 700, fontSize: 15, color: 'var(--ink-3)', letterSpacing: '.06em' }}>0{i + 1}</div>
              <h3 className="rf-h4" style={{ margin: '6px 0 10px' }}>{s.title}</h3>
              <p className="rf-body" style={{ margin: 0, color: 'var(--ink-2)' }}>{s.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// CTA band
function WCta() {
  return (
    <section style={{ maxWidth: 1240, margin: '0 auto', padding: '80px 40px' }}>
      <div style={{
        background: 'var(--ink)', borderRadius: 'var(--r-xl)', padding: '64px 56px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 40,
      }}>
        <div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 48, lineHeight: 1.02, color: 'var(--on-dark)', margin: 0, maxWidth: 560 }}>
            Have a home to rent out?
          </h2>
          <p style={{ color: 'rgba(240,240,236,.72)', fontSize: 19, marginTop: 14, maxWidth: 480 }}>
            List it on RentFlow and reach renters who are ready to move. Free to start.
          </p>
        </div>
        <WButton variant="invert" size="lg" icon="arrow-right" style={{ flexShrink: 0 }}>List your home</WButton>
      </div>
    </section>
  );
}

// ---- Browse view (search results) ----
function WBrowse({ onOpen }) {
  const [filter, setFilter] = React.useState('All');
  const chips = ['All', 'Furnished', '2+ beds', 'Pet friendly', 'Near lake', 'Under ₫10M'];
  return (
    <div style={{ maxWidth: 1240, margin: '0 auto', padding: '40px 40px 24px' }}>
      <div className="rf-overline" style={{ marginBottom: 8 }}>Rent in Hà Nội</div>
      <h1 className="rf-h1" style={{ marginBottom: 24 }}>{WEB_LISTINGS.length} homes available</h1>
      {/* filter bar */}
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 28 }}>
        {chips.map(c => (
          <button key={c} onClick={() => setFilter(c)} style={{
            fontFamily: 'var(--font-sans)', fontWeight: 600, fontSize: 14, padding: '10px 16px',
            borderRadius: 'var(--r-pill)', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6,
            background: filter === c ? 'var(--ink)' : 'var(--surface)',
            color: filter === c ? 'var(--paper)' : 'var(--ink-1)',
            border: '1px solid ' + (filter === c ? 'var(--ink)' : 'var(--line-strong)'),
          }}>{c === 'All' && <WIcon name="sliders-horizontal" size={15} />}{c}</button>
        ))}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
        {WEB_LISTINGS.map(item => <WListingCard key={item.id} item={item} onOpen={() => onOpen(item)} />)}
      </div>
    </div>
  );
}

// ---- Detail modal ----
function WDetailModal({ item, onClose }) {
  const amenities = [['wifi', 'Fast Wi-Fi'], ['wind', 'Air con'], ['car', 'Parking'], ['washing-machine', 'Laundry'], ['sun', 'Balcony'], ['shield-check', 'Verified host']];
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 60, display: 'flex', alignItems: 'flex-start', justifyContent: 'center', overflow: 'auto', padding: '48px 24px' }}>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, background: 'rgba(26,28,29,.5)', backdropFilter: 'blur(2px)' }} />
      <div style={{ position: 'relative', width: 'min(960px, 100%)', background: 'var(--paper)', borderRadius: 'var(--r-xl)', overflow: 'hidden', boxShadow: 'var(--shadow-lg)' }}>
        <div style={{ position: 'relative', height: 380, background: 'var(--paper-2)' }}>
          <img src={`https://picsum.photos/seed/${item.seed}/1200/700`} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(.92)' }} />
          <button onClick={onClose} style={{
            position: 'absolute', top: 18, right: 18, width: 44, height: 44, borderRadius: 'var(--r-pill)',
            background: 'rgba(251,251,249,.92)', border: 'none', cursor: 'pointer', display: 'flex',
            alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(4px)',
          }}><WIcon name="x" size={22} color="var(--ink-1)" /></button>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 40, padding: '32px 40px 40px' }}>
          <div>
            <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, fontWeight: 700, fontSize: 13, padding: '5px 11px', borderRadius: 'var(--r-pill)', background: 'var(--success-tint)', color: 'var(--success)' }}><WIcon name="badge-check" size={14} />Verified</span>
            </div>
            <h2 className="rf-h2" style={{ marginBottom: 6 }}>{item.title}</h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--ink-3)', fontSize: 16 }}>
              <WIcon name="map-pin" size={16} />{item.area}, Hà Nội · <b style={{ color: 'var(--ink-1)' }}>{item.rating}</b> ★
            </div>
            <div style={{ display: 'flex', gap: 12, margin: '24px 0' }}>
              {[['bed', item.beds + ' bed'], ['bath', item.baths + ' bath'], ['ruler', item.m2 + ' m²']].map(([ic, lb]) => (
                <div key={lb} style={{ flex: 1, background: 'var(--surface)', border: '1px solid var(--line)', borderRadius: 'var(--r-md)', padding: '16px', textAlign: 'center' }}>
                  <WIcon name={ic} size={20} color="var(--accent)" />
                  <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--ink-1)', marginTop: 6 }}>{lb}</div>
                </div>
              ))}
            </div>
            <p className="rf-body">A calm corner home with great morning light, a small balcony, and an easy walk to the lake path. Quiet street, verified host, ready this month.</p>
            <div className="rf-overline" style={{ margin: '20px 0 14px' }}>What's included</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
              {amenities.map(([ic, lb]) => <div key={lb} style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--ink-1)', fontSize: 15 }}><WIcon name={ic} size={19} color="var(--ink-2)" />{lb}</div>)}
            </div>
          </div>
          {/* booking card */}
          <div style={{ alignSelf: 'start', position: 'sticky', top: 0, background: 'var(--surface)', border: '1px solid var(--line)', borderRadius: 'var(--r-lg)', padding: 24, boxShadow: 'var(--shadow-sm)' }}>
            <div style={{ fontFamily: 'var(--font-cond)', fontWeight: 700, fontSize: 34, color: 'var(--ink)', lineHeight: 1 }}>
              ₫{item.price.toLocaleString('en-US')}<span style={{ fontFamily: 'var(--font-sans)', fontWeight: 400, fontSize: 16, color: 'var(--ink-3)' }}>/mo</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 20 }}>
              <WButton variant="primary" icon="calendar" style={{ justifyContent: 'center' }}>Book a tour</WButton>
              <WButton variant="secondary" icon="message-circle" style={{ justifyContent: 'center' }}>Message host</WButton>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 18, color: 'var(--ink-3)', fontSize: 14 }}>
              <WIcon name="shield-check" size={16} color="var(--accent)" />Deposit protected by RentFlow
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { WHero, WFeatured, WHowItWorks, WCta, WBrowse, WDetailModal });

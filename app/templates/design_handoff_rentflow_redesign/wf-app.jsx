// Main app: design canvas + tweaks panel

const ACCENT_OPTIONS = {
  'Coral marker (mặc định)': '#dc4a3f',
  'Xanh dương': '#2a5a9e',
  'Xanh ngọc': '#1a8472',
  'Indigo / tím': '#5044c4',
  'Đỏ tươi': '#c41a3f',
};

const FONT_OPTIONS = {
  'Patrick Hand (gọn)':         "'Patrick Hand', cursive",
  'Caveat (chữ ký)':            "'Caveat', cursive",
  'Architects Daughter (kỹ sư)': "'Architects Daughter', cursive",
  'Kalam (mềm)':                "'Kalam', cursive",
};

const HEAD_FONT_OPTIONS = {
  'Caveat':            "'Caveat', cursive",
  'Patrick Hand':      "'Patrick Hand', cursive",
  'Architects Daughter': "'Architects Daughter', cursive",
  'Kalam':             "'Kalam', cursive",
};

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#dc4a3f",
  "bodyFont": "'Patrick Hand', cursive",
  "headFont": "'Patrick Hand', cursive",
  "showNotes": true
}/*EDITMODE-END*/;

function applyTheme(t) {
  document.documentElement.style.setProperty('--accent', t.accent);
  document.documentElement.style.setProperty('--font-sketch', t.bodyFont);
  document.documentElement.style.setProperty('--font-head', t.headFont);
  // Update accent-soft based on accent
  const soft = hexToSoft(t.accent);
  document.documentElement.style.setProperty('--accent-soft', soft);
  // toggle sticky notes
  document.querySelectorAll('.wf-note').forEach(n => {
    n.style.display = t.showNotes ? 'block' : 'none';
  });
}

function hexToSoft(hex) {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, 0.18)`;
}

function WireframeApp() {
  const [tweaks, setTweak] = useTweaks(TWEAK_DEFAULTS);

  React.useEffect(() => {
    applyTheme(tweaks);
  }, [tweaks]);

  return (
    <>
      <DesignCanvas minScale={0.15}>
        <DCSection id="overview" title="6 hướng thiết kế lại UI" subtitle="Mỗi artboard giải quyết một nhóm pain point khác nhau · click để focus · kéo để sắp xếp lại">

          <DCArtboard id="v1" label="A · Tổng quan dạng Analytics Dashboard" width={ART_W} height={ART_H}>
            <V1Dashboard />
          </DCArtboard>

          <DCArtboard id="v5" label="B · Tổng quan Workflow-first" width={ART_W} height={ART_H}>
            <V5WorkflowDashboard />
          </DCArtboard>

          <DCArtboard id="v2" label="C · Hóa đơn — Master/Detail (5 cột)" width={ART_W} height={ART_H}>
            <V2BillsMasterDetail />
          </DCArtboard>

          <DCArtboard id="v3" label="D · Phòng & Khách — lưới card theo tầng" width={ART_W} height={ART_H}>
            <V3RoomCardGrid />
          </DCArtboard>

          <DCArtboard id="v4" label="E · Hóa đơn — Heatmap cả năm" width={ART_W} height={ART_H}>
            <V4Heatmap />
          </DCArtboard>

          <DCArtboard id="v6" label="F · Mobile — Card stack + Bottom nav" width={1380} height={860}>
            <V6Mobile />
          </DCArtboard>

        </DCSection>
      </DesignCanvas>

      <TweaksPanel title="Tweaks · Wireframe">
        <TweakSection label="Hand-drawn look">
          <TweakColor
            label="Accent"
            value={tweaks.accent}
            onChange={(v) => setTweak('accent', v)}
            options={Object.values(ACCENT_OPTIONS)}
          />
          <TweakSelect
            label="Font chữ thân"
            value={tweaks.bodyFont}
            onChange={(v) => setTweak('bodyFont', v)}
            options={Object.entries(FONT_OPTIONS).map(([k, v]) => ({ label: k, value: v }))}
          />
          <TweakSelect
            label="Font tiêu đề"
            value={tweaks.headFont}
            onChange={(v) => setTweak('headFont', v)}
            options={Object.entries(HEAD_FONT_OPTIONS).map(([k, v]) => ({ label: k, value: v }))}
          />
        </TweakSection>
        <TweakSection label="Hiển thị">
          <TweakToggle
            label="Sticky note ghi chú"
            value={tweaks.showNotes}
            onChange={(v) => setTweak('showNotes', v)}
          />
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<WireframeApp />);

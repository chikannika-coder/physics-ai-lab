"""fix_sidebar.py — แก้ sidebar stats"""
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "physics_ai_app_v4.py"

content = TARGET.read_text(encoding="utf-8")

OLD = '''    kb = load_kb()
    st.markdown("### 📈 สถิติ")
    st.metric("สมการใน KB", len(kb.get("equations", [])))
    st.metric("เวอร์ชัน", kb.get("version", "0.0.0"))
    st.metric("ทรัพยากร", len(kb.get("resources", [])))

    st.markdown("---")
    st.caption("Physics AI Lab v4.0 | 2026")'''

NEW = '''    kb = load_kb()
    n_eq = len(kb.get("equations", []))
    n_res = len(kb.get("resources", []))
    kb_ver = kb.get("version", "0.0.0")

    st.markdown("### 📈 สถิติ")
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
        <div style="font-size: 0.85rem; opacity: 0.8;">สมการใน KB</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{n_eq}</div>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
        <div style="font-size: 0.85rem; opacity: 0.8;">เวอร์ชัน</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{kb_ver}</div>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
        <div style="font-size: 0.85rem; opacity: 0.8;">ทรัพยากร</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{n_res}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Physics AI Lab v4.0 | 2026")'''

if OLD in content:
    content = content.replace(OLD, NEW)
    TARGET.write_text(content, encoding="utf-8")
    print("[OK] แก้ sidebar stats")
    print("รันใหม่: py -3 -m streamlit run physics_ai_app_v4.py")
else:
    print("[SKIP] ไม่พบโค้ดเดิม")
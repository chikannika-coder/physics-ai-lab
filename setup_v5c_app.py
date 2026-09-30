"""setup_v5c_app.py - เพิ่ม 3 เมนู"""
from pathlib import Path

R = Path(__file__).parent
SRC = R / "physics_ai_app_v4.py"
DST = R / "physics_ai_app_v5.py"

if not SRC.exists():
    print(f"[ERR] ไม่พบ {SRC}"); exit(1)

c = SRC.read_text(encoding="utf-8")

# เพิ่มเมนู
OLD = '''        "📖 Example Projects",
        "📊 Analytics",'''
NEW = '''        "📖 Example Projects",
        "🔧 Physics Devices",
        "🎥 Equation Animator",
        "➕ Add Knowledge",
        "📊 Analytics",'''
if OLD in c:
    c = c.replace(OLD, NEW)
    print("[OK] เพิ่ม 3 เมนู")
else:
    print("[WARN] sidebar")

# เพิ่ม handlers ก่อน footer
FOOTER = '''st.markdown("---")
st.caption("Physics AI Lab v4.0 | 2026 | Made with ❤️ for Thai students")'''

HANDLERS = '''elif page == "🔧 Physics Devices":
    st.markdown("## 🔧 อุปกรณ์ฟิสิกส์จาก ทบ.")
    try:
        from physics_devices import DEVICES
    except ImportError:
        st.error("ไม่พบ physics_devices.py - รัน setup_v5a_devices.py")
        DEVICES = {}
    if DEVICES:
        cats = sorted(set(d["category"] for d in DEVICES.values()))
        cat = st.selectbox("หมวด", ["ทั้งหมด"] + cats)
        filt = {k:v for k,v in DEVICES.items() if cat=="ทั้งหมด" or v["category"]==cat}
        sel = st.selectbox("เลือกอุปกรณ์", list(filt.keys()),
            format_func=lambda k: f"{filt[k]['name_th']} - {filt[k]['name_en']}")
        if sel:
            d = filt[sel]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"### {d['name_th']}")
                st.markdown(f"**{d['name_en']}** | {d['category']}")
                st.markdown(f"**หลักการ:** {d['principle']}")
                st.latex(d['formula'])
                st.markdown(f"**การใช้งาน:** {d['real_use']}")
            with c2:
                g = OUTPUT_DIR / "devices" / f"device_{sel}.gif"
                if g.exists(): st.image(str(g), use_column_width=True)
                else: st.info("ยังไม่มี GIF - รัน py -3 physics_devices.py")
        st.markdown("---")
        st.markdown("### 📋 ทั้งหมด")
        for k, d in DEVICES.items():
            g = OUTPUT_DIR / "devices" / f"device_{k}.gif"
            st.markdown(f"{'✅' if g.exists() else '⏳'} **{d['name_th']}**")

elif page == "🎥 Equation Animator":
    st.markdown("## 🎥 Equation Animator")
    try:
        from equation_animator import animate_equation, detect_type
        ok = True
    except ImportError:
        st.error("ไม่พบ equation_animator.py - รัน setup_v5b_animator.py")
        ok = False
    if ok:
        t1, t2 = st.tabs(["สร้างใหม่", "ดูทั้งหมด"])
        with t1:
            fm = st.text_input("สมการ", "y = A*sin(k*x - w*t)")
            nm = st.text_input("ชื่อ", "my_eq")
            du = st.slider("วินาที", 2, 10, 3)
            if st.button("🎬 สร้าง", type="primary"):
                with st.spinner("..."):
                    tt = detect_type(fm)
                    st.info(f"ประเภท: **{tt}**")
                    try:
                        p = animate_equation(fm, nm, du, 25)
                        st.success("สร้างเสร็จ!"); st.image(p, use_column_width=True)
                    except Exception as e: st.error(f"{e}")
        with t2:
            ed = OUTPUT_DIR / "equations"
            if ed.exists():
                gifs = sorted(ed.glob("*.gif"))
                if gifs:
                    cols = st.columns(2)
                    for i, g in enumerate(gifs):
                        with cols[i%2]:
                            st.markdown(f"**{g.stem}**")
                            st.image(str(g), use_column_width=True)
                else: st.info("รัน py -3 equation_animator.py ก่อน")

elif page == "➕ Add Knowledge":
    st.markdown("## ➕ เพิ่มความรู้ใหม่")
    kb = load_kb()
    for k in ["equations","resources","devices","history"]:
        kb.setdefault(k, [])
    ch = st.radio("ประเภท",
        ["📐 สมการ","🔧 อุปกรณ์","🖼️ รูป","💻 โค้ด","🎬 Animation"],
        horizontal=True)
    st.markdown("---")

    if ch == "📐 สมการ":
        with st.form("f1"):
            c1, c2 = st.columns(2)
            with c1:
                i = st.text_input("ID","new_eq")
                nth = st.text_input("ชื่อไทย","สมการใหม่")
                nen = st.text_input("ชื่ออังกฤษ","New Eq")
                cat = st.selectbox("หมวด",["mechanics","electricity","thermodynamics","waves","optics","quantum","other"])
            with c2:
                lx = st.text_input("LaTeX", r"E = mc^2")
                fm = st.text_input("สูตร", "E = m * c**2")
                lv = st.selectbox("ระดับ",["ม.ต้น","ม.ปลาย","มหาวิทยาลัย"])
            vj = st.text_area("ตัวแปร (JSON)", '{"E":"พลังงาน"}')
            if st.form_submit_button("💾 เพิ่ม", type="primary"):
                try:
                    kb["equations"].append({"id":i,"name_th":nth,"name_en":nen,
                        "latex":lx,"formula":fm,"variables":json.loads(vj),
                        "category":cat,"level":lv,"domain":[cat]})
                    kb["history"].append({"date":datetime.now().strftime("%Y-%m-%d %H:%M"),
                                          "action":"added_equation","id":i})
                    save_kb(kb); st.success(f"เพิ่ม '{nth}' สำเร็จ!"); st.rerun()
                except json.JSONDecodeError: st.error("JSON ผิด")

    elif ch == "🔧 อุปกรณ์":
        with st.form("f2"):
            i = st.text_input("ID","new_dev")
            nth = st.text_input("ชื่อไทย","อุปกรณ์ใหม่")
            nen = st.text_input("ชื่ออังกฤษ","New Device")
            cat = st.selectbox("หมวด",["mechanics","electricity","thermodynamics","optics","waves","quantum","other"])
            pr = st.text_area("หลักการ","")
            fm = st.text_input("สมการ","F = ma")
            ru = st.text_input("การใช้งาน","")
            if st.form_submit_button("💾 เพิ่ม"):
                kb["devices"].append({"id":i,"name_th":nth,"name_en":nen,
                    "category":cat,"principle":pr,"formula":fm,"real_use":ru})
                save_kb(kb); st.success(f"เพิ่ม '{nth}' สำเร็จ!")

    elif ch == "🖼️ รูป":
        with st.form("f3"):
            i = st.text_input("ID","img_001")
            t = st.text_input("ชื่อ","รูปใหม่")
            d = st.text_area("คำอธิบาย","")
            tg = st.text_input("Tags","physics")
            up = st.file_uploader("อัปโหลด", type=["png","jpg","jpeg"])
            if st.form_submit_button("💾 เพิ่ม"):
                if up:
                    ud = R / "uploads"; ud.mkdir(exist_ok=True)
                    (ud/up.name).write_bytes(up.read())
                    kb["resources"].append({"id":i,"type":"image","title":t,
                        "path":f"uploads/{up.name}","description":d,
                        "tags":[x.strip() for x in tg.split(",")]})
                    save_kb(kb); st.success("เพิ่มสำเร็จ!"); st.rerun()

    elif ch == "💻 โค้ด":
        with st.form("f4"):
            i = st.text_input("ID","code_001")
            t = st.text_input("ชื่อ","โค้ดใหม่")
            lg = st.selectbox("ภาษา",["python","arduino","javascript","other"])
            body = st.text_area("Code","print('hello')", height=200)
            tg = st.text_input("Tags","physics")
            if st.form_submit_button("💾 เพิ่ม"):
                kb["resources"].append({"id":i,"type":"code","title":t,
                    "language":lg,"code":body,
                    "tags":[x.strip() for x in tg.split(",")]})
                save_kb(kb); st.success("เพิ่มสำเร็จ!")

    elif ch == "🎬 Animation":
        with st.form("f5"):
            i = st.text_input("ID","anim_001")
            t = st.text_input("ชื่อ","Animation ใหม่")
            d = st.text_area("คำอธิบาย","")
            tg = st.text_input("Tags","physics")
            up = st.file_uploader("อัปโหลด GIF", type=["gif"])
            if st.form_submit_button("💾 เพิ่ม"):
                if up:
                    ud = R / "uploads"; ud.mkdir(exist_ok=True)
                    (ud/up.name).write_bytes(up.read())
                    kb["resources"].append({"id":i,"type":"animation","title":t,
                        "path":f"uploads/{up.name}","description":d,
                        "tags":[x.strip() for x in tg.split(",")]})
                    save_kb(kb); st.success("เพิ่มสำเร็จ!"); st.rerun()

    st.markdown("---")
    st.markdown("### 📊 สรุป")
    c1, c2, c3 = st.columns(3)
    c1.metric("สมการ", len(kb["equations"]))
    c2.metric("อุปกรณ์", len(kb.get("devices",[])))
    c3.metric("ทรัพยากร", len(kb["resources"]))

'''

if FOOTER in c:
    c = c.replace(FOOTER, HANDLERS + FOOTER)
    print("[OK] เพิ่ม 3 handlers")
else:
    print("[WARN] footer")

DST.write_text(c, encoding="utf-8")
print(f"[OK] สร้าง: {DST}")
print("next: py -3 -m streamlit run physics_ai_app_v5.py")
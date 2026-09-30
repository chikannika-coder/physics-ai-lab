"""example_projects.py"""
EXAMPLE_PROJECTS = [
    {'id': 'pendulum_ai', 'title': 'AI ค้นพบสมการลูกตุ้ม', 'level': 'ม.ปลาย',
     'duration': '4 สัปดาห์',
     'description': 'ใช้ PySR ค้นหาสมการ T = 2*pi*sqrt(L/g)',
     'objectives': ['เข้าใจกระบวนการวิทยาศาสตร์', 'ใช้ Symbolic Regression', 'เปรียบเทียบสมการ'],
     'equations': ['pendulum'], 'animations': ['pendulum'],
     'deliverable': 'รายงาน + วิดีโอ 2 นาที'},
    {'id': 'heat_dhamma', 'title': 'สมการความร้อนกับอนิจจัง', 'level': 'ม.ปลาย',
     'duration': '6 สัปดาห์',
     'description': 'ใช้ PINN แก้สมการความร้อน เปรียบเทียบกับอนิจจัง',
     'objectives': ['เข้าใจสมการความร้อน', 'ใช้ PINN', 'เชื่อมโยงวิทยาศาสตร์กับพุทธ'],
     'equations': ['heat_conduction'], 'animations': ['heat'],
     'deliverable': 'รายงาน + animation'},
    {'id': 'quantum_packet', 'title': 'Quantum Wave Packet', 'level': 'มหาวิทยาลัย',
     'duration': '8 สัปดาห์',
     'description': 'ใช้ Symbolic Regression ค้นหา wave packet',
     'objectives': ['เข้าใจ Schrodinger', 'ใช้ PySR', 'Visualize'],
     'equations': ['schrodinger'], 'animations': ['quantum'],
     'deliverable': 'รายงาน + poster'},
    {'id': 'satiarm_bio', 'title': 'SatiARM วัด HRV', 'level': 'ม.ปลาย',
     'duration': '10 สัปดาห์',
     'description': 'ใช้แขนกลนำการฝึกสติ วัด HRV',
     'objectives': ['ออกแบบการทดลอง', 'ใช้ FSR + PPG', 'วิเคราะห์สถิติ'],
     'equations': ['heat_conduction'], 'animations': ['robot_hand'],
     'deliverable': 'รายงานวิจัย + GitHub'},
    {'id': 'fluid_flow', 'title': 'AI วิเคราะห์การไหล', 'level': 'มหาวิทยาลัย',
     'duration': '8 สัปดาห์',
     'description': 'ใช้ Symbolic Regression ค้นหา Poiseuille',
     'objectives': ['เข้าใจ Navier-Stokes', 'ใช้ PySR', 'ประยุกต์'],
     'equations': ['navier_stokes'], 'animations': ['wave'],
     'deliverable': 'รายงาน + กราฟ'},
]

def get_project(pid):
    for p in EXAMPLE_PROJECTS:
        if p['id'] == pid: return p
    return None

if __name__ == '__main__':
    for p in EXAMPLE_PROJECTS:
        print('=' * 60)
        print(f"  {p['title']}")
        print(f"  ระดับ: {p['level']}  |  เวลา: {p['duration']}")
        print('=' * 60)
        print(f"  {p['description']}")
        for o in p['objectives']: print(f'    - {o}')
        print()

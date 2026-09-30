# Deploy Streamlit Cloud

## 1. GitHub
- https://github.com/signup
- สร้าง repo: physics-ai-lab
- อัปโหลด: physics_ai_app.py, physics_knowledge.json, physics_knowledge.py,
  physics_symbolic_v4.py, advanced_analytics.py, animation_engine.py,
  example_projects.py, requirements.txt

## 2. requirements.txt
streamlit
pandas
numpy
matplotlib
scipy
scikit-learn
PyWavelets
pysr
pyserial

## 3. Streamlit Cloud
https://streamlit.io/cloud > New app > เลือก repo > Deploy

## 4. รอ build 3-5 นาที
URL: https://your-app.streamlit.app

## 5. Update
git add . && git commit -m 'Update' && git push

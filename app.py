# app.py
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import math
import random

st.set_page_config(page_title="기계공학 미니게임 - 기어 맞추기", layout="centered")
st.title("⚙️ 기계공학 미니게임: 기어 맞추기 ⚙️")

# 초기 상태 저장
if "level" not in st.session_state:
    st.session_state.level = 1
if "gear_angles" not in st.session_state:
    st.session_state.gear_angles = [0, 0, 0]
if "gears" not in st.session_state:
    st.session_state.gears = []
if "goal_angle" not in st.session_state:
    st.session_state.goal_angle = 0

def generate_gears(level):
    gears = [
        {'x': 1, 'y': 2, 'r': 0.5},
        {'x': 3, 'y': 2, 'r': 0.8},
        {'x': 5, 'y': 2, 'r': 0.4}
    ]
    # 레벨마다 약간씩 위치 변경
    for g in gears:
        g['y'] += random.uniform(-0.5,0.5)
    goal_angle = 6 + level*0.5
    return gears, goal_angle

if not st.session_state.gears:
    st.session_state.gears, st.session_state.goal_angle = generate_gears(st.session_state.level)

def draw_gears():
    fig, ax = plt.subplots(figsize=(8,4))
    ax.set_xlim(0,6)
    ax.set_ylim(0,4)
    ax.set_aspect('equal')
    ax.axis('off')
    
    colors = ['blue','red','green']
    for i, g in enumerate(st.session_state.gears):
        c = Circle((g['x'], g['y']), g['r'], fill=False, color=colors[i], lw=3)
        ax.add_patch(c)
        ax.add_patch(FancyArrow(g['x'], g['y'],
                                g['r']*math.cos(st.session_state.gear_angles[i]),
                                g['r']*math.sin(st.session_state.gear_angles[i]),
                                width=0.05, color=colors[i]))
    
    if abs(st.session_state.gear_angles[2]) >= st.session_state.goal_angle:
        st.success(f"🎉 성공! 레벨 {st.session_state.level} 완료 🎉")
    
    st.pyplot(fig)

def rotate_left():
    st.session_state.gear_angles[0] -= 0.2
    st.session_state.gear_angles[1] += 0.2 * (st.session_state.gears[0]['r']/st.session_state.gears[1]['r'])
    st.session_state.gear_angles[2] -= 0.2 * (st.session_state.gears[0]['r']/st.session_state.gears[2]['r'])

def rotate_right():
    st.session_state.gear_angles[0] += 0.2
    st.session_state.gear_angles[1] -= 0.2 * (st.session_state.gears[0]['r']/st.session_state.gears[1]['r'])
    st.session_state.gear_angles[2] += 0.2 * (st.session_state.gears[0]['r']/st.session_state.gears[2]['r'])

def next_level():
    st.session_state.level += 1
    st.session_state.gear_angles = [0,0,0]
    st.session_state.gears, st.session_state.goal_angle = generate_gears(st.session_state.level)

# UI 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⭠ 회전"):
        rotate_left()
with col2:
    draw_gears()
with col3:
    if st.button("회전 ⭢"):
        rotate_right()

if abs(st.session_state.gear_angles[2]) >= st.session_state.goal_angle:
    if st.button("다음 레벨 ▶"):
        next_level()
        draw_gears()

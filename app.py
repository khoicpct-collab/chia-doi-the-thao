# app.py - Flow Simulator Pro Main App
import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import json
import time
import sys
import os

# Thêm utils vào path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from physics_engine import RealisticPhysics
from drawing_tools import DrawingCanvas
from export_tools import ExportManager

# Cấu hình trang
st.set_page_config(
    page_title="Flow Simulator Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FlowSimulatorPro:
    def __init__(self):
        self.physics_engine = RealisticPhysics()
        self.drawing_tools = DrawingCanvas()
        self.export_manager = ExportManager()
        
        # Khởi tạo session state
        if 'design_image' not in st.session_state:
            st.session_state.design_image = None
        if 'flow_paths' not in st.session_state:
            st.session_state.flow_paths = []
        if 'material_properties' not in st.session_state:
            st.session_state.material_properties = {}
        if 'simulation_data' not in st.session_state:
            st.session_state.simulation_data = {}
        if 'current_simulation' not in st.session_state:
            st.session_state.current_simulation = None

    def main_interface(self):
        """Giao diện chính của ứng dụng"""
        
        # Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0;">🏭 Flow Simulator Pro</h1>
            <p style="color: white; margin: 0; font-size: 1.2rem;">Mô phỏng dòng chảy nguyên liệu chân thực</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.sidebar.title("🧭 Điều hướng")
        app_mode = st.sidebar.selectbox(
            "Chọn chế độ",
            ["🎨 Thiết kế hệ thống", "⚙️ Cài đặt vật lý", "🎬 Mô phỏng", "📊 Kết quả & Xuất file"]
        )
        
        # Route đến các trang
        if app_mode == "🎨 Thiết kế hệ thống":
            self.design_interface()
        elif app_mode == "⚙️ Cài đặt vật lý":
            self.physics_interface()
        elif app_mode == "🎬 Mô phỏng":
            self.simulation_interface()
        else:
            self.export_interface()

    def design_interface(self):
        """Giao diện thiết kế hệ thống"""
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            self.upload_panel()
            self.equipment_templates()
            self.material_selection()
            
        with col2:
            self.drawing_canvas()
            
        # Quick actions
        st.sidebar.markdown("---")
        if st.sidebar.button("🚀 Chuyển đến Mô phỏng", use_container_width=True):
            st.session_state.current_page = "🎬 Mô phỏng"
            st.rerun()

    def upload_panel(self):
        """Panel upload bản vẽ"""
        st.header("📤 Upload bản vẽ")
        
        uploaded_file = st.file_uploader(
            "Tải lên bản vẽ hệ thống",
            type=['png', 'jpg', 'jpeg', 'svg'],
            help="Upload bản vẽ 2D/3D của hệ thống"
        )
        
        if uploaded_file is not None:
            # Xử lý ảnh
            image = Image.open(uploaded_file)
            st.session_state.design_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            st.success(f"✅ Đã upload: {uploaded_file.name}")
            st.image(image, caption="Bản vẽ đã upload", use_column_width=True)
            
            # Hiển thị thông tin
            st.info(f"**Kích thước:** {image.size[0]} x {image.size[1]} pixels")

    def equipment_templates(self):
        """Templates cho các loại thiết bị"""
        st.header("🏗️ Loại thiết bị")
        
        equipment_type = st.selectbox(
            "Chọn loại thiết bị",
            ["Vít tải (Screw Conveyor)", "Băng tải (Belt Conveyor)", "Ống dẫn (Piping)", 
             "Phễu (Hopper)", "Máy trộn (Mixer)", "Tùy chỉnh"]
        )
        
        # Hiển thị template tương ứng
        templates = {
            "Vít tải (Screw Conveyor)": self.screw_conveyor_template,
            "Băng tải (Belt Conveyor)": self.belt_conveyor_template,
            "Ống dẫn (Piping)": self.piping_template,
            "Phễu (Hopper)": self.hopper_template
        }
        
        if equipment_type in templates:
            templates[equipment_type]()
            
        st.session_state.equipment_type = equipment_type

    def screw_conveyor_template(self):
        """Template cho vít tải"""
        st.subheader("⚙️ Thông số vít tải")
        
        col1, col2 = st.columns(2)
        
        with col1:
            screw_diameter = st.number_input("Đường kính vít (mm)", 100, 1000, 300)
            screw_pitch = st.number_input("Bước vít (mm)", 50, 500, 150)
            rotation_speed = st.slider("Tốc độ quay (RPM)", 10, 200, 60)
            
        with col2:
            screw_length = st.number_input("Chiều dài vít (mm)", 1000, 10000, 3000)
            material_flow = st.selectbox("Hướng dòng chảy", ["Trái → Phải", "Phải → Trái"])
            inclination = st.slider("Góc nghiêng (°)", 0, 90, 0)
        
        st.session_state.equipment_params = {
            'type': 'screw_conveyor',
            'diameter': screw_diameter,
            'pitch': screw_pitch,
            'speed': rotation_speed,
            'length': screw_length,
            'flow_direction': material_flow,
            'inclination': inclination
        }

    def material_selection(self):
        """Lựa chọn vật liệu"""
        st.header("🌾 Vật liệu")
        
        material_type = st.selectbox(
            "Chọn vật liệu vận chuyển",
            ["Lúa mì", "Ngô", "Gạo", "Cám", "Nhựa viên", "Cát", "Bột mì", "Xi măng", "Tùy chỉnh..."]
        )
        
        # Hiển thị đặc tính vật liệu
        material_props = self.physics_engine.get_material_properties(material_type)
        
        st.subheader("📊 Đặc tính vật liệu")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Mật độ", f"{material_props['density']} kg/m³")
            st.metric("Góc nghỉ", f"{material_props['angle_of_repose']}°")
            
        with col2:
            st.metric("Ma sát", f"{material_props['friction']}")
            st.metric("Đàn hồi", f"{material_props['restitution']}")
        
        st.session_state.material_properties = material_props

    def drawing_canvas(self):
        """Canvas vẽ đường dẫn"""
        st.header("🎨 Vẽ đường dẫn dòng chảy")
        
        if st.session_state.design_image is None:
            st.warning("⚠️ Vui lòng upload bản vẽ trước khi vẽ đường dẫn")
            return
            
        # Toolbar vẽ
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            draw_tool = st.selectbox("Công cụ", ["Đường thẳng", "Đường cong", "Đường xoắn", "Tự do"])
        
        with col2:
            brush_size = st.slider("Kích thước", 1, 10, 3)
            
        with col3:
            line_color = st.color_picker("Màu đường", "#FF0000")
            
        with col4:
            if st.button("🗑️ Xóa tất cả"):
                st.session_state.flow_paths = []
                st.rerun()
        
        # Sử dụng streamlit-drawable-canvas
        try:
            from streamlit_drawable_canvas import st_canvas
            
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=brush_size,
                stroke_color=line_color,
                background_image=Image.fromarray(
                    cv2.cvtColor(st.session_state.design_image, cv2.COLOR_BGR2RGB)
                ) if st.session_state.design_image is not None else None,
                height=500,
                width=700,
                drawing_mode="freedraw" if draw_tool == "Tự do" else "line",
                key="design_canvas",
            )
            
            if canvas_result.json_data is not None:
                self.process_canvas_data(canvas_result.json_data)
                
        except ImportError:
            st.error("Thư viện vẽ chưa được cài đặt. Sử dụng phiên bản đơn giản.")
            self.simple_drawing_interface()

    def process_canvas_data(self, canvas_data):
        """Xử lý dữ liệu từ canvas"""
        if canvas_data["objects"]:
            for obj in canvas_data["objects"]:
                if obj["type"] == "path":
                    points = [(p["x"], p["y"]) for p in obj["path"]]
                    st.session_state.flow_paths.append({
                        "points": points,
                        "type": "custom",
                        "color": obj["stroke"],
                        "width": obj["strokeWidth"]
                    })

    def physics_interface(self):
        """Giao diện cài đặt vật lý"""
        st.header("⚙️ Cài đặt Vật lý & Môi trường")
        
        tab1, tab2, tab3 = st.tabs(["🎯 Vật lý dòng chảy", "🌡️ Môi trường", "🔧 Nâng cao"])
        
        with tab1:
            self.flow_physics_settings()
            
        with tab2:
            self.environment_settings()
            
        with tab3:
            self.advanced_physics_settings()

    def flow_physics_settings(self):
        """Cài đặt vật lý dòng chảy"""
        st.subheader("🎯 Vật lý dòng chảy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            flow_speed = st.slider("Tốc độ dòng chảy", 0.1, 5.0, 1.0, 0.1)
            particle_count = st.slider("Số lượng hạt", 10, 500, 100)
            particle_size = st.slider("Kích thước hạt (mm)", 1, 50, 10)
            
        with col2:
            density_variation = st.slider("Biến thiên mật độ", 0.0, 1.0, 0.2)
            cohesion = st.slider("Lực kết dính", 0.0, 1.0, 0.1)
            turbulence = st.slider("Độ nhiễu loạn", 0.0, 1.0, 0.3)
        
        st.session_state.physics_settings = {
            'flow_speed': flow_speed,
            'particle_count': particle_count,
            'particle_size': particle_size,
            'density_variation': density_variation,
            'cohesion': cohesion,
            'turbulence': turbulence
        }

    def simulation_interface(self):
        """Giao diện mô phỏng"""
        st.header("🎬 Mô phỏng Thời gian Thực")
        
        if not st.session_state.flow_paths:
            st.error("❌ Chưa có đường dẫn nào được vẽ. Vui lòng quay lại trang thiết kế.")
            return
            
        # Control panel
        self.simulation_controls()
        
        # Simulation display
        self.simulation_display()
        
        # Real-time statistics
        self.real_time_stats()

    def simulation_controls(self):
        """Điều khiển mô phỏng"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("▶️ Bắt đầu", type="primary", use_container_width=True):
                self.start_simulation()
                
        with col2:
            if st.button("⏸️ Tạm dừng", use_container_width=True):
                self.pause_simulation()
                
        with col3:
            if st.button("⏹️ Dừng", use_container_width=True):
                self.stop_simulation()
                
        with col4:
            simulation_speed = st.selectbox("Tốc độ", [0.5, 1.0, 2.0, 5.0], index=1)
            
        with col5:
            st.metric("Trạng thái", "Đang chạy" if st.session_state.current_simulation else "Dừng")

    def simulation_display(self):
        """Hiển thị mô phỏng"""
        simulation_placeholder = st.empty()
        
        if st.session_state.current_simulation:
            # Hiển thị animation real-time
            self.update_simulation_display(simulation_placeholder)
        else:
            # Hiển thị preview
            if st.session_state.design_image and st.session_state.flow_paths:
                self.show_design_preview(simulation_placeholder)

    def update_simulation_display(self, placeholder):
        """Cập nhật hiển thị mô phỏng"""
        # Tạo frame animation
        fig = self.create_animation_frame()
        placeholder.pyplot(fig)
        plt.close()

    def create_animation_frame(self):
        """Tạo frame animation"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Hiển thị ảnh nền
        if st.session_state.design_image is not None:
            ax.imshow(cv2.cvtColor(st.session_state.design_image, cv2.COLOR_BGR2RGB))
        
        # Hiển thị particles
        if st.session_state.current_simulation:
            for particle in st.session_state.current_simulation['particles']:
                ax.scatter(particle['x'], particle['y'], 
                          s=particle['size']*10, 
                          c=particle['color'], 
                          alpha=particle['alpha'])
        
        ax.set_title("Mô phỏng dòng chảy - Đang chạy")
        ax.axis('off')
        
        return fig

    def real_time_stats(self):
        """Thống kê thời gian thực"""
        st.subheader("📊 Thống kê vận hành")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Lưu lượng", "125 kg/h", "+5.2%")
            
        with col2:
            st.metric("Tốc độ", "45 rpm", "-2.1%")
            
        with col3:
            st.metric("Hiệu suất", "92%", "+1.5%")
            
        with col4:
            st.metric("Thời gian", "2:45", "Đang chạy")

    def export_interface(self):
        """Giao diện xuất file"""
        st.header("📤 Xuất Kết quả & Báo cáo")
        
        export_format = st.selectbox(
            "Định dạng xuất",
            ["GIF Animation", "MP4 Video", "PowerPoint", "PDF Report", "Interactive HTML", "3D Model"]
        )
        
        if st.button("🚀 Tạo báo cáo", type="primary"):
            with st.spinner("Đang tạo báo cáo..."):
                report_path = self.export_manager.generate_report(
                    st.session_state.simulation_data,
                    export_format
                )
                
                st.success("✅ Báo cáo đã sẵn sàng!")
                
                # Hiển thị preview
                if export_format in ["GIF Animation", "MP4 Video"]:
                    st.video(report_path)
                elif export_format == "PDF Report":
                    st.pdf(report_path)
                
                # Download button
                with open(report_path, "rb") as f:
                    st.download_button(
                        "📥 Tải về báo cáo",
                        f,
                        file_name=f"simulation_report.{export_format.split()[0].lower()}",
                        mime="application/octet-stream"
                    )

    def start_simulation(self):
        """Bắt đầu mô phỏng"""
        st.session_state.current_simulation = {
            'particles': self.initialize_particles(),
            'start_time': time.time(),
            'running': True
        }

    def initialize_particles(self):
        """Khởi tạo particles"""
        particles = []
        particle_count = st.session_state.physics_settings.get('particle_count', 100)
        
        for i in range(particle_count):
            particles.append({
                'id': i,
                'x': np.random.uniform(100, 500),
                'y': np.random.uniform(100, 400),
                'size': np.random.uniform(5, 15),
                'color': '#FF6B35',
                'alpha': np.random.uniform(0.6, 1.0),
                'velocity': [np.random.uniform(-2, 2), np.random.uniform(-1, 1)]
            })
        
        return particles

    def pause_simulation(self):
        """Tạm dừng mô phỏng"""
        if st.session_state.current_simulation:
            st.session_state.current_simulation['running'] = False

    def stop_simulation(self):
        """Dừng mô phỏng"""
        st.session_state.current_simulation = None

# Chạy ứng dụng
if __name__ == "__main__":
    app = FlowSimulatorPro()
    app.main_interface()

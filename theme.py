from nicegui import ui
from contextlib import contextmanager

@contextmanager
def frame(page_title: str):
    """Custom page frame with header, drawer, and footer."""
    
    # 1. Global Styles & Fonts (Outfit Font)
    ui.add_head_html("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
        
        <style>
            body {
                font-family: 'Outfit', sans-serif;
                background-color: #f8fafc;
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f1f1; 
            }
            ::-webkit-scrollbar-thumb {
                background: #cbd5e1; 
                border-radius: 5px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #94a3b8; 
            }

            /* Glassmorphism Utility */
            .glass {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            /* Gradient Text */
            .text-gradient {
                background: linear-gradient(135deg, #0e4d92 0%, #0077b6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Card Hover Effect */
            .hover-card {
                transition: all 0.3s ease;
            }
            .hover-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            }
        </style>
    """)

    # 2. Initialize AOS (Animate On Scroll)
    ui.add_body_html("""
        <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
        <script>
            AOS.init({
                duration: 800,
                once: true,
                offset: 50
            });
        </script>
    """)

    ui.colors(primary='#0e4d92', secondary='#0077b6', accent='#4caf50', positive='#21ba45')
    
    # Header
    with ui.header().classes('bg-white/90 backdrop-blur-md text-slate-800 shadow-sm items-center h-20 px-8 border-b border-slate-100'):
        ui.icon('public', size='md').classes('mr-2 text-primary')
        ui.label('Plastic Pollution Awareness').classes('text-xl font-bold mr-auto text-primary tracking-tight')
        
        # Desktop Navigation
        with ui.row().classes('hidden md:flex gap-8'):
            def nav_link(text, target):
                ui.link(text, target).classes('text-slate-600 no-underline hover:text-primary font-semibold transition-colors')
            
            nav_link('Home', '/')
            nav_link('Types', '/types')
            nav_link('Impact', '/impact')
            nav_link('Stats', '/stats')
            nav_link('Solutions', '/solutions')
            
            # CTA Button
            ui.button('Upload Image', on_click=lambda: ui.open('/upload')).classes('bg-primary text-white px-6 rounded-full shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all')

        # Mobile Menu Button
        with ui.button(icon='menu', color='primary').classes('md:hidden').props('flat round'):
            ui.on('click', lambda: drawer.toggle())

    # Mobile Drawer
    with ui.left_drawer(value=False).classes('bg-white p-6') as drawer:
        ui.label('Menu').classes('text-2xl font-bold text-primary mb-8')
        with ui.column().classes('w-full gap-6'):
            def drawer_link(text, target, icon):
                with ui.link(target=target).classes('w-full no-underline text-slate-700 hover:text-primary flex items-center gap-4 group'):
                    ui.icon(icon).classes('text-slate-400 group-hover:text-primary transition-colors')
                    ui.label(text).classes('text-lg font-medium')
            
            drawer_link('Home', '/', 'home')
            drawer_link('Types', '/types', 'category')
            drawer_link('Impact', '/impact', 'analytics')
            drawer_link('Stats', '/stats', 'query_stats')
            drawer_link('Solutions', '/solutions', 'lightbulb')
            drawer_link('Upload', '/upload', 'cloud_upload')

    # Footer
    with ui.footer().classes('bg-slate-900 text-white items-center justify-center h-16'):
        with ui.row().classes('gap-2 items-center opacity-70'):
            ui.label('© 2024 Plastic Pollution Awareness').classes('text-sm font-light')
            ui.label('•').classes('text-sm')
            ui.label('Built with NiceGUI').classes('text-sm font-semibold')

    # Main Content Container
    with ui.column().classes('w-full min-h-screen bg-slate-50 p-0 m-0 gap-0'):
        with ui.column().classes('w-full flex-grow items-center p-0 m-0'):
            yield

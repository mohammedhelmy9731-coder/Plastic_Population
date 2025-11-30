from nicegui import ui, app, run
import random

# --- إعدادات الخادم ---
# تقديم الملفات الثابتة (مثل الصور) من المجلد الحالي
app.add_static_files('/assets', '.')

def setup_ui():
    """
    إعداد الواجهة العامة للموقع: الألوان، الخطوط، والأنماط (CSS).
    """
    # 1. تكوين الألوان الرئيسية للموقع
    ui.colors(primary='#38bdf8', secondary='#22c55e', accent='#a855f7', dark='#020617')

    # 2. إضافة ملفات CSS و JavaScript الخارجية
    # مكتبة AOS (Animate On Scroll) المسؤولة عن حركات الظهور عند النزول
    ui.add_head_html('<link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet">')
    ui.add_head_html('<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>')

    # 3. كتابة كود CSS مخصص داخل بايثون
    ui.add_head_html('''
        <style>
            /* --- استيراد الخطوط --- */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Grotesk:wght@300;500;700&display=swap');
            
            /* --- إعدادات الصفحة الأساسية --- */
            body {
                font-family: 'Inter', sans-serif;
                /* خلفية متدرجة تحاكي أعماق المحيط */
                background: linear-gradient(to bottom, #0f172a, #020617, #000000);
                color: #f8fafc;
                overflow-x: hidden; /* منع التمرير الأفقي */
                /* تم إزالة cursor: none لضمان ظهور الماوس دائماً */
            }
            
            h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif; }

            /* --- شريط التمرير المخصص (Scrollbar) --- */
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: #0f172a; }
            ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #475569; }

            /* --- تأثير الزجاج (Glassmorphism) --- */
            /* يستخدم لإنشاء بطاقات شفافة مع تمويه للخلفية */
            .glass-card {
                background: rgba(255, 255, 255, 0.03); /* شفافية عالية */
                backdrop-filter: blur(16px); /* تمويه الخلفية */
                border: 1px solid rgba(255, 255, 255, 0.05); /* حدود خفيفة */
                border-radius: 24px; /* زوايا دائرية */
                transition: all 0.3s ease; /* حركة سلسة عند التفاعل */
            }
            
            /* تأثير عند مرور الماوس على البطاقة */
            .glass-card:hover {
                transform: translateY(-5px) scale(1.02); /* رفع وتكبير بسيط */
                background: rgba(255, 255, 255, 0.08); /* زيادة السطوع */
                border-color: rgba(56, 189, 248, 0.3); /* توهج الحدود */
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); /* ظل */
            }

            /* --- تأثير توهج النص --- */
            .text-glow { text-shadow: 0 0 20px rgba(56, 189, 248, 0.5); }

            /* --- تأثيرات الخلفية المتحركة (Caustics) --- */
            body::before {
                content: "";
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: 
                    radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(34, 197, 94, 0.05) 0%, transparent 30%);
                z-index: -2;
                pointer-events: none;
            }

            /* --- الماوس التفاعلي (Custom Cursor) --- */
            /* دائرة تتبع الماوس كزينة إضافية، مع بقاء الماوس الأصلي ظاهراً */
            .cursor-outline {
                position: fixed; top: 0; left: 0;
                width: 40px; height: 40px; 
                border: 1px solid rgba(56, 189, 248, 0.5);
                border-radius: 50%; 
                z-index: 9999; 
                pointer-events: none; /* يسمح بالنقر من خلالها */
                transform: translate(-50%, -50%);
            }
            
            /* حالة التفاعل: تكبير الدائرة عند المرور على عناصر قابلة للنقر */
            .cursor-outline.cursor-hover {
                width: 60px; height: 60px;
                background-color: rgba(56, 189, 248, 0.1);
                border-color: rgba(56, 189, 248, 0.8);
                box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
            }

            /* --- شريط التقدم العلوي --- */
            .scroll-progress {
                position: fixed; top: 0; left: 0; width: 0%; height: 4px;
                background: linear-gradient(90deg, #0ea5e9, #22c55e, #eab308);
                z-index: 10000; transition: width 0.1s;
            }
            
            /* مسافة إضافية للتمرير السلس */
            .section-scroll-target { scroll-margin-top: 5rem; }
            
            /* تأثير زجاجي ضبابي على روابط القائمة */
            .nav-item {
                position: relative;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            
            .nav-item::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 8px;
                opacity: 0;
                transform: scale(0.9);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: -1;
            }
            
            .nav-item:hover::before {
                opacity: 1;
                transform: scale(1);
                box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
            }
            
            .nav-item:hover {
                transform: translateY(-2px);
            }
        </style>
    ''')

    # 4. إضافة كود JavaScript للتحكم في الحركات
    ui.add_body_html('''
        <div class="cursor-outline"></div>
        <div class="scroll-progress"></div>
        <script>
            // تهيئة مكتبة AOS للحركات عند التمرير
            AOS.init({
                duration: 1000, // مدة الحركة (1 ثانية)
                once: false,    // تكرار الحركة كلما ظهر العنصر
                mirror: true    // تفعيل الحركة عند الصعود أيضاً
            });
            
            // --- منطق الماوس التفاعلي ---
            const cursorOutline = document.querySelector('.cursor-outline');
            
            // تحريك الدائرة مع الماوس
            window.addEventListener('mousemove', e => {
                const posX = e.clientX;
                const posY = e.clientY;
                
                // استخدام animate لحركة ناعمة ومتأخرة قليلاً (Trailing Effect)
                if (cursorOutline) {
                    cursorOutline.animate({
                        left: `${posX}px`,
                        top: `${posY}px`
                    }, {duration: 500, fill: "forwards"});
                }
            });

            // --- تأثير التفاعل (Hover) ---
            const addHoverEffect = () => {
                // تحديد العناصر التي يجب أن يتفاعل معها الماوس
                const selectors = 'a, button, .cursor-pointer, .q-btn, .nav-item, .glass-card, input';
                const interactiveElements = document.querySelectorAll(selectors);
                
                interactiveElements.forEach(el => {
                    el.addEventListener('mouseenter', () => {
                        if (cursorOutline) cursorOutline.classList.add('cursor-hover');
                    });
                    el.addEventListener('mouseleave', () => {
                        if (cursorOutline) cursorOutline.classList.remove('cursor-hover');
                    });
                });
            };
            
            // تشغيل دالة التفاعل ومراقبة أي عناصر جديدة تضاف للصفحة
            addHoverEffect();
            const observer = new MutationObserver(addHoverEffect);
            observer.observe(document.body, { childList: true, subtree: true });

            // --- شريط التقدم ---
            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                const progressBar = document.querySelector(".scroll-progress");
                if (progressBar) progressBar.style.width = scrolled + "%";
            });
        </script>
    ''')

# --- الصفحة الرئيسية ---
@ui.page('/')
def index_page():
    setup_ui() # استدعاء إعدادات الواجهة
    
    # --- القائمة العلوية (Header) ---
    with ui.header().classes('bg-slate-900/20 backdrop-blur-md h-20 px-4 md:px-8 flex items-center justify-between fixed w-full z-50 border-b border-white/10'):
        # الشعار
        with ui.row().classes('items-center gap-2 cursor-pointer').on('click', lambda: ui.run_javascript('window.scrollTo({top:0, behavior:"smooth"})')):
            ui.icon('public', color='primary', size='md').classes('animate-pulse')
            ui.label('ECO').classes('text-2xl md:text-3xl font-black text-white tracking-tighter')
            ui.label('VISION').classes('text-2xl md:text-3xl font-light text-primary tracking-tighter')
        
        # روابط التنقل - إخفاء على الموبايل (يمكن إضافة قائمة همبرغر لاحقاً) أو جعلها قابلة للتمرير
        with ui.row().classes('hidden md:flex gap-8'):
            def nav_link(text, target_id):
                # رابط يتفاعل مع الماوس وينقل المستخدم لقسم معين
                ui.label(text).classes('nav-item text-white hover:text-primary transition-colors duration-300 font-bold text-lg uppercase tracking-widest cursor-pointer').on('click', lambda tid=target_id: ui.run_javascript(f'document.getElementById("{tid}").scrollIntoView({{behavior:"smooth"}})'))
            nav_link('Home', 'home')
            nav_link('Types', 'types')
            nav_link('Crisis', 'crisis')
            nav_link('Impact', 'impact')
            nav_link('Solutions', 'solutions')
            nav_link('AI Tools', 'ai-tools')

    # --- المحتوى الرئيسي ---
    with ui.column().classes('w-full min-h-screen p-0 m-0 gap-0'):
        
        # 1. قسم البداية (Home Section)
        with ui.element('section').classes('w-full min-h-screen flex items-center justify-center relative overflow-hidden section-scroll-target') as home:
            home.props('id="home"')
            with ui.column().classes('items-center text-center max-w-5xl z-10 px-4 relative'):
                # نصوص متحركة باستخدام AOS (fade-down, zoom-in)
                ui.label('THE PLASTIC ERA').classes('text-primary font-bold tracking-[0.5em] text-xs md:text-sm mb-4').props('data-aos="fade-down"')
                ui.label('IS ENDING NOW').classes('text-4xl md:text-6xl lg:text-8xl font-black text-white mb-6 leading-tight text-glow').props('data-aos="zoom-in"')
                ui.label('Join the revolution to cleanse our oceans and reclaim our future through AI-driven solutions.').classes('text-base md:text-xl text-slate-400 max-w-2xl mb-12').props('data-aos="fade-up"')
                
                # أزرار الإجراءات
                with ui.row().classes('gap-4 md:gap-6 flex-wrap justify-center').props('data-aos="fade-up"'):
                    ui.button('Explore Data', on_click=lambda: ui.run_javascript('document.getElementById("impact").scrollIntoView({behavior:"smooth"})')).classes('bg-primary text-black font-bold text-base md:text-lg px-6 md:px-8 py-3 md:py-4 rounded-full hover:scale-105 transition-transform shadow-[0_0_20px_rgba(56,189,248,0.4)]')
                    ui.button('AI Tools', on_click=lambda: ui.run_javascript('document.getElementById("ai-tools").scrollIntoView({behavior:"smooth"})')).classes('border border-white/20 text-white font-bold text-base md:text-lg px-6 md:px-8 py-3 md:py-4 rounded-full hover:bg-white/10 transition-colors')

        # 2. قسم أنواع التلوث (Pollution Types) - المربعات المطلوبة
        with ui.element('section').classes('w-full min-h-screen py-24 relative section-scroll-target overflow-hidden') as types:
            types.props('id="types"')
            with ui.column().classes('max-w-7xl mx-auto px-6 w-full relative z-10'):
                ui.label('WATER POLLUTION').classes('text-primary font-bold tracking-widest mb-2').props('data-aos="fade-down"')
                ui.label('TYPES OF CONTAMINATION').classes('text-5xl font-bold text-white mb-16').props('data-aos="fade-down"')
                
                # شبكة المربعات (Cards Grid)
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                    def pollution_card(title, desc, icon, color, delay):
                        # بطاقة زجاجية (Glass Card) مع تأثيرات AOS و Hover
                        with ui.card().classes('glass-card p-8 relative overflow-hidden group').props(f'data-aos="fade-up" data-aos-delay="{delay}"'):
                            # توهج خلفي
                            ui.element('div').classes(f'absolute -top-12 -right-12 w-40 h-40 bg-{color}-500/10 rounded-full blur-[60px] group-hover:bg-{color}-500/30 transition-all duration-700')
                            
                            # أيقونة
                            with ui.row().classes('w-full justify-between items-start mb-6'):
                                with ui.element('div').classes(f'p-3 rounded-2xl bg-{color}-500/10 group-hover:bg-{color}-500/20 transition-colors duration-300'):
                                    ui.icon(icon, size='3xl', color=color).classes('group-hover:scale-110 group-hover:rotate-6 transition-transform duration-500')
                                ui.icon('arrow_outward', size='sm', color='slate-500').classes('opacity-0 group-hover:opacity-100 -translate-y-2 group-hover:translate-y-0 transition-all duration-300')

                            # نصوص
                            ui.label(title).classes('text-2xl font-bold text-white mb-3 group-hover:text-white transition-colors')
                            ui.label(desc).classes('text-slate-400 leading-relaxed text-sm')
                            
                            # خط سفلي متحرك
                            ui.element('div').classes(f'absolute bottom-0 left-0 w-full h-[2px] bg-gradient-to-r from-{color}-500 to-transparent transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left')

                    # إنشاء المربعات ببيانات مختلفة وتأخير زمني للحركة
                    pollution_card('Chemical Waste', 'Industrial runoff containing mercury, lead, and toxic solvents.', 'science', 'purple', '0')
                    pollution_card('Plastic Debris', 'Microplastics and single-use items choking marine life.', 'local_drink', 'blue', '100')
                    pollution_card('Oil Spills', 'Devastating slicks from tanker accidents and drilling operations.', 'water_drop', 'gray', '200')
                    pollution_card('Sewage', 'Untreated wastewater introducing harmful bacteria and pathogens.', 'waves', 'green', '300')
                    pollution_card('Thermal Pollution', 'Heated water discharge disrupting aquatic ecosystems.', 'thermostat', 'red', '400')
                    pollution_card('Radioactive Waste', 'Long-lasting contamination from nuclear facilities.', 'warning', 'yellow', '500')

        # 3. قسم الأزمة (Crisis Section)
        with ui.element('section').classes('w-full min-h-screen py-24 relative section-scroll-target overflow-hidden') as crisis:
            crisis.props('id="crisis"')
            with ui.column().classes('max-w-7xl mx-auto px-6 w-full relative z-10'):
                ui.label('THE ENEMY').classes('text-primary font-bold tracking-widest mb-2').props('data-aos="fade-right"')
                ui.label('KNOW YOUR PLASTICS').classes('text-3xl md:text-5xl font-bold text-white mb-16').props('data-aos="fade-right"')
                with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full'):
                    def crisis_card(title, desc, image_url, delay):
                        # بطاقة تعرض صورة ومعلومات
                        with ui.card().classes('glass-card h-full p-0 flex flex-col gap-0 overflow-hidden group hover:scale-105 transition-transform duration-500').props(f'data-aos="fade-up" data-aos-delay="{delay}"'):
                            ui.image(image_url).classes('w-full h-48 object-cover transition-transform duration-500')
                            with ui.column().classes('p-6 gap-4'):
                                ui.label(title).classes('text-2xl font-bold text-white')
                                ui.label(desc).classes('text-slate-400 leading-relaxed')
                    crisis_card('Microplastics', '< 5mm particles in water, food, air', 'https://images.unsplash.com/photo-1618477388954-7852f32655ec?auto=format&fit=crop&w=500&q=60', '0')
                    crisis_card('Single-Use', 'Used once, lasting forever', 'https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&w=500&q=60', '100')
                    crisis_card('Ghost Gear', 'Abandoned fishing nets', 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=500&q=60', '200')
                    crisis_card('Mega-Debris', 'Great Pacific Patch', 'https://images.unsplash.com/photo-1621451537084-482c73073a0f?auto=format&fit=crop&w=500&q=60', '300')

        # 3. قسم التأثير (Impact Section) - إحصائيات ورسوم بيانية
        with ui.element('section').classes('w-full min-h-screen section-padding relative section-scroll-target overflow-hidden') as impact:
            impact.props('id="impact"')
            with ui.column().classes('max-w-7xl mx-auto px-6 w-full relative z-10'):
                ui.label('THE CONSEQUENCES').classes('text-secondary font-bold tracking-widest mb-2').props('data-aos="fade-left"')
                ui.label('ENVIRONMENTAL IMPACT').classes('text-3xl md:text-5xl font-bold text-white mb-16').props('data-aos="fade-left"')
                # بطاقات الإحصائيات
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-8 mb-16 w-full'):
                    def stat_card(val, label, icon, color, delay):
                        with ui.card().classes(f'glass-card flex-1 p-8 items-center text-center border-t-4 border-{color}-500').props(f'data-aos="zoom-in" data-aos-delay="{delay}"'):
                            ui.icon(icon, size='4xl', color=color).classes('mb-4')
                            ui.label(val).classes('text-5xl font-black text-white text-glow mb-2')
                            ui.label(label).classes('text-slate-400 text-lg')
                    stat_card('400M', 'Tonnes/Year', 'factory', 'blue', '0')
                    stat_card('1000', 'Years to Decay', 'schedule', 'red', '100')
                    stat_card('1M+', 'Marine Deaths', 'water_drop', 'green', '200')
                # الرسوم البيانية (ECharts)
                ui.label('DATA VISUALIZATION').classes('text-3xl font-bold text-white mb-8').props('data-aos="fade-up"')
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full h-auto'):
                    with ui.card().classes('flex-1 glass-card p-6').props('data-aos="fade-right"'):
                        ui.label('Waste by Sector').classes('text-xl font-bold text-white mb-4')
                        ui.echart({'tooltip':{'trigger':'item'},'legend':{'top':'5%','left':'center','textStyle':{'color':'#fff'}},'series':[{'type':'pie','radius':['40%','70%'],'itemStyle':{'borderRadius':10,'borderColor':'#1e293b','borderWidth':2},'label':{'show':False},'data':[{'value':36,'name':'Packaging','itemStyle':{'color':'#38bdf8'}},{'value':16,'name':'Construction','itemStyle':{'color':'#f472b6'}},{'value':14,'name':'Textiles','itemStyle':{'color':'#a78bfa'}},{'value':34,'name':'Other','itemStyle':{'color':'#94a3b8'}}]}]}).classes('w-full h-64')
                    with ui.card().classes('flex-1 glass-card p-6').props('data-aos="fade-left"'):
                        ui.label('Top Polluting Countries').classes('text-xl font-bold text-white mb-4')
                        ui.echart({'tooltip':{'trigger':'axis','axisPointer':{'type':'shadow'}},'grid':{'left':'3%','right':'4%','bottom':'3%','containLabel':True},'xAxis':[{'type':'category','data':['China','USA','India','Brazil','Japan'],'axisLabel':{'color':'#fff'}}],'yAxis':[{'type':'value','axisLabel':{'color':'#fff'}}],'series':[{'name':'Waste','type':'bar','barWidth':'60%','data':[60,38,24,12,9],'itemStyle':{'color':'#22c55e'}}]}).classes('w-full h-64')

        # 4. قسم الحلول (Solutions Section)
        with ui.element('section').classes('w-full min-h-screen section-padding relative section-scroll-target overflow-hidden') as solutions:
            solutions.props('id="solutions"')
            with ui.column().classes('max-w-7xl mx-auto px-6 w-full relative z-10'):
                ui.label('THE CURE').classes('text-accent font-bold tracking-widest mb-2').props('data-aos="fade-up"')
                ui.label('INNOVATION & ACTION').classes('text-3xl md:text-5xl font-bold text-white mb-16').props('data-aos="fade-up"')
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-8 w-full'):
                    def solution_card(title, desc, icon, color, delay):
                        with ui.card().classes(f'glass-card p-8 border-t-4 border-{color}-500').props(f'data-aos="flip-up" data-aos-delay="{delay}"'):
                            ui.icon(icon, size='4xl', color=color).classes('mb-6')
                            ui.label(title).classes('text-2xl font-bold text-white mb-4')
                            ui.label(desc).classes('text-slate-400 leading-relaxed')
                    solution_card('Reduce', 'Minimize waste at source', 'remove_circle_outline', 'green', '0')
                    solution_card('Bio-Materials', 'Mushroom & algae alternatives', 'spa', 'teal', '100')
                    solution_card('AI Sorting', 'Advanced robotics', 'smart_toy', 'purple', '200')

        # 5. قسم أدوات الذكاء الاصطناعي (AI Tools Section)
        with ui.element('section').classes('w-full min-h-screen py-24 relative section-scroll-target overflow-hidden') as ai_tools:
            ai_tools.props('id="ai-tools"')
            with ui.column().classes('max-w-7xl mx-auto px-6 w-full items-center text-center relative z-10'):
                ui.label('FUTURE TECH').classes('text-primary font-bold tracking-widest mb-2').props('data-aos="fade-down"')
                ui.label('AI POWERED TOOLS').classes('text-5xl font-bold text-white mb-16').props('data-aos="fade-down"')
                
                with ui.row().classes('w-full gap-8 justify-center flex-wrap md:flex-nowrap'):
                    # بطاقة الشات بوت
                    with ui.card().classes('w-full md:w-1/2 h-auto md:h-96 glass-card p-8 flex flex-col items-center justify-center gap-6 hover:border-primary transition-colors group').props('data-aos="fade-right"'):
                        ui.icon('smart_toy', size='6xl', color='accent').classes('mb-4 group-hover:scale-110 transition-transform')
                        ui.label('EcoBot Assistant').classes('text-3xl font-bold text-white text-center')
                        ui.label('Ask anything about recycling, pollution, or sustainability.').classes('text-slate-400 text-lg text-center')
                        ui.button('Start Chat', on_click=lambda: ui.navigate.to('/chatbot', new_tab=True)).classes('bg-accent text-white px-8 py-2 rounded-full hover:bg-accent/80')

                    # بطاقة تحليل الصور
                    with ui.card().classes('w-full md:w-1/2 h-auto md:h-96 glass-card p-8 flex flex-col items-center justify-center gap-6 hover:border-primary transition-colors group').props('data-aos="fade-left"'):
                        ui.icon('center_focus_strong', size='6xl', color='primary').classes('mb-4 group-hover:scale-110 transition-transform')
                        ui.label('Waste Analyzer').classes('text-3xl font-bold text-white text-center')
                        ui.label('Upload an image to identify plastic types and recycling methods.').classes('text-slate-400 text-lg text-center')
                        ui.button('Start Analysis', on_click=lambda: ui.navigate.to('/analyze', new_tab=True)).classes('bg-primary text-black px-8 py-2 rounded-full hover:bg-primary/80 font-bold')

    # تذييل الصفحة (Footer)
    with ui.element('footer').classes('w-full bg-black/50 backdrop-blur-md py-12 border-t border-white/10'):
        with ui.column().classes('w-full max-w-7xl mx-auto px-6 items-center text-center'):
            ui.label('ECO VISION').classes('text-2xl font-bold text-white mb-4 tracking-tighter')
            ui.label('Designed for a cleaner future.').classes('text-slate-500 mb-8')
            ui.label('© 2024 Plastic Pollution Initiative').classes('text-slate-700 text-sm')

# --- مكون الكاميرا (Camera Component) ---
def camera_capture_dialog(on_capture):
    import uuid
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-lg p-0 overflow-hidden bg-black border border-white/20'):
        # معرف فريد للفيديو
        vid_id = f'cam-{uuid.uuid4().hex}'
        
        # عنصر الفيديو
        ui.html(f'<video id="{vid_id}" autoplay playsinline class="w-full aspect-square bg-black object-cover"></video>', sanitize=False)
        
        # تشغيل الكاميرا (دالة JS)
        async def start_camera_js():
            await ui.run_javascript(f'''
                const video = document.getElementById("{vid_id}");
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
                    alert("Camera API not supported. Please use HTTPS or localhost.");
                    return;
                }}
                
                // Try simple constraint first for maximum compatibility
                navigator.mediaDevices.getUserMedia({{ video: true }})
                .then(stream => {{
                    video.srcObject = stream;
                    video.play();
                }})
                .catch(err => {{
                    console.error("Camera Error:", err);
                    alert("Camera Error: " + err.message);
                }});
            ''')

        # تشغيل عند الفتح
        dialog.on('open', start_camera_js)

        # إيقاف الكاميرا عند الإغلاق
        dialog.on('close', lambda: ui.run_javascript(f'''
            const video = document.getElementById("{vid_id}");
            if (video && video.srcObject) {{
                video.srcObject.getTracks().forEach(track => track.stop());
            }}
        '''))

        # أزرار التحكم
        with ui.row().classes('w-full p-6 justify-center gap-8 bg-slate-900/80 backdrop-blur'):
            ui.button(icon='refresh', on_click=start_camera_js).props('round flat color=yellow').classes('w-12 h-12').tooltip('Retry Camera')
            ui.button(icon='close', on_click=dialog.close).props('round flat color=red').classes('w-12 h-12')
            
            async def capture():
                # التقاط الصورة وتحويلها إلى Base64
                base64_img = await ui.run_javascript(f'''
                    const video = document.getElementById("{vid_id}");
                    if (video.readyState < 2) {{ // HAVE_CURRENT_DATA
                        return null;
                    }}
                    const canvas = document.createElement("canvas");
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(video, 0, 0);
                    return canvas.toDataURL("image/jpeg", 0.8);
                ''')
                
                if not base64_img:
                    ui.notify('Camera not ready or stream empty. Please wait or click Retry.', type='warning')
                    return
                
                if base64_img:
                    dialog.close()
                    import inspect
                    result = on_capture(base64_img)
                    if inspect.iscoroutine(result):
                        await result

            ui.button(icon='camera_alt', on_click=capture).props('round color=white text-color=black size=lg').classes('shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:scale-110 transition-transform')
    
    dialog.open()

# --- صفحة التحليل (Analysis Page) ---
@ui.page('/analyze')
def analysis_page():
    from analysis import classifier
    from nicegui import run
    import time
    import os

    setup_ui() # استدعاء نفس التنسيق
    
    # سجل للأخطاء (مخفي) - تم إزالته
    # log = ui.log().classes('w-full h-20 bg-black/50 text-xs font-mono text-green-400 p-2 rounded hidden')

    with ui.column().classes('w-full min-h-screen items-center p-4 md:p-8 gap-8'):
        # عنوان الصفحة
        with ui.column().classes('items-center text-center'):
            ui.label('AI POLLUTION ANALYZER').classes('text-4xl md:text-6xl font-black text-white tracking-tighter text-glow mb-2')
            ui.label('Upload an image to detect pollution type and get solutions.').classes('text-slate-400 text-lg')

        # منطقة المحتوى
        with ui.row().classes('w-full max-w-7xl gap-8 items-start justify-center flex-wrap md:flex-nowrap'):
            
            # --- العمود الأيسر: الرفع والتحكم ---
            with ui.card().classes('w-full md:w-5/12 glass-card p-8 items-center gap-6 border-t-4 border-primary'):
                ui.label('1. IMAGE UPLOAD').classes('text-xl font-bold text-primary tracking-widest self-start')
                
                # حالة لحفظ مسار الملف
                state = {'file_path': None}

                # تسمية الحالة
                status_label = ui.label('Status: Waiting for image...').classes('text-yellow-400 font-mono text-sm bg-black/30 p-2 rounded w-full text-center')

                # معاينة الصورة (مخفية في البداية)
                preview = ui.image().classes('w-full aspect-square object-cover rounded-2xl border-2 border-white/20 shadow-lg hidden')

                # زر التحليل
                async def run_analysis():
                    current_file = state['file_path']
                    # log.push(f"Analyze clicked. State file: {current_file}")
                    
                    if not current_file: 
                        status_label.text = 'Status: No image found!'
                        status_label.classes(remove='text-yellow-400 text-green-400', add='text-red-400')
                        ui.notify('Please upload an image first!', type='warning')
                        return
                    
                    # التحقق من وجود الملف
                    if not os.path.exists(current_file):
                        status_label.text = f'Status: File {os.path.basename(current_file)} missing!'
                        ui.notify('Error: Image file not found on server.', type='negative')
                        return

                    if not classifier.model:
                        status_label.text = 'Status: Model not loaded!'
                        ui.notify('Error: AI Model not loaded.', type='negative')
                        return

                    status_label.text = 'Status: Analyzing...'
                    status_label.classes(remove='text-red-400 text-green-400', add='text-yellow-400')
                    
                    analyze_btn.loading = True
                    results_placeholder.classes('hidden')
                    results_content.classes('hidden')
                    loading_spinner.classes(remove='hidden')
                    
                    try:
                        # log.push(f"Analyzing: {current_file}")
                        
                        # تشغيل التحليل في عملية منفصلة لتجنب تجميد الواجهة
                        result = await run.io_bound(classifier.predict, current_file)
                        
                        if result:
                            display_result(result)
                            status_label.text = 'Status: Analysis Complete'
                            status_label.classes(remove='text-yellow-400', add='text-green-400')
                        else:
                            status_label.text = 'Status: Analysis Failed'
                            status_label.classes(remove='text-yellow-400', add='text-red-400')
                            ui.notify('Analysis failed.', type='negative')
                    except Exception as e:
                        status_label.text = f'Status: Error - {str(e)}'
                        # log.push(f"Error: {e}")
                        ui.notify(f'Error: {str(e)}', type='negative')
                    finally:
                        analyze_btn.loading = False
                        loading_spinner.classes('hidden')

                # analyze_btn moved to bottom
                
                # مكون الرفع
                async def on_upload(e):
                    import inspect
                    # log.classes(remove='hidden') # Keep log hidden
                    # log.push("Upload started...")
                    
                    try:
                        content_source = None
                        source_name = "Unknown"

                        # 1. محاولة الوصول للمحتوى بالطريقة القياسية
                        if hasattr(e, 'content'):
                            content_source = e.content
                            source_name = 'content'
                        # 2. محاولة الوصول عبر 'file'
                        elif hasattr(e, 'file'):
                            content_source = e.file
                            source_name = 'file'
                        
                        if content_source is None:
                            # log.push(f"ERROR: No content/file found. Dir: {dir(e)}")
                            status_label.text = "Status: Upload Error - No content"
                            status_label.classes(remove='text-yellow-400 text-green-400', add='text-red-400')
                            return

                        # log.push(f"Found source '{source_name}' of type: {type(content_source)}")

                        # توليد اسم ملف فريد
                        filename_base = f'upload_{int(time.time())}.jpg'
                        filename_abs = os.path.abspath(filename_base)
                        
                        with open(filename_abs, 'wb') as f:
                            # قراءة البيانات (قد تكون متزامنة أو غير متزامنة)
                            if hasattr(content_source, 'read'):
                                if hasattr(content_source, 'seek'):
                                    content_source.seek(0)
                                
                                data = content_source.read()
                                if inspect.iscoroutine(data):
                                    data = await data
                                f.write(data)
                                
                            elif isinstance(content_source, bytes):
                                f.write(content_source)
                            elif hasattr(content_source, 'file'): 
                                nested = content_source.file
                                if hasattr(nested, 'read'):
                                    if hasattr(nested, 'seek'):
                                        nested.seek(0)
                                    data = nested.read()
                                    if inspect.iscoroutine(data):
                                        data = await data
                                    f.write(data)
                                else:
                                    f.write(nested)
                            else:
                                # log.push(f"Unknown content type: {type(content_source)}")
                                raise ValueError(f"Cannot read content from {type(content_source)}")
                        
                        # log.push(f"File saved: {filename_abs}")
                        
                        # تحديث الحالة
                        state['file_path'] = filename_abs
                        
                        # تحديث المعاينة
                        preview.set_source(f'/assets/{filename_base}')
                        preview.classes(remove='hidden')
                        
                        status_label.text = f'Status: Image Uploaded'
                        status_label.classes(remove='text-yellow-400 text-red-400', add='text-green-400')
                        
                        e.sender.reset()
                        ui.notify('Image uploaded!', type='positive')
                    except Exception as err:
                        error_msg = str(err)
                        print(f"DEBUG: Upload Error: {error_msg}")
                        # log.push(f"Upload Error: {error_msg}")
                        status_label.text = f'Status: Upload Error - {error_msg}'
                        status_label.classes(remove='text-yellow-400 text-green-400', add='text-red-400')
                        ui.notify(f'Upload failed: {error_msg}', type='negative')

                # زر الكاميرا
                async def handle_camera_capture(base64_img):
                    import base64
                    
                    try:
                        # إزالة الترويسة إذا وجدت
                        if ',' in base64_img:
                            base64_img = base64_img.split(',')[1]
                        
                        img_data = base64.b64decode(base64_img)
                        
                        filename_base = f'capture_{int(time.time())}.jpg'
                        filename_abs = os.path.abspath(filename_base)
                        
                        with open(filename_abs, 'wb') as f:
                            f.write(img_data)
                        
                        # تحديث الحالة
                        state['file_path'] = filename_abs
                        
                        # تحديث المعاينة
                        preview.set_source(f'/assets/{filename_base}')
                        preview.classes(remove='hidden')
                        
                        status_label.text = 'Status: Image Captured'
                        status_label.classes(remove='text-yellow-400 text-red-400', add='text-green-400')
                        ui.notify('Image captured successfully!', type='positive')
                        
                    except Exception as e:
                        ui.notify(f'Capture failed: {str(e)}', type='negative')

                # Input Section
                with ui.row().classes('w-full gap-4'):
                    # Upload (Flex 1)
                    ui.upload(on_upload=on_upload, auto_upload=True, label='UPLOAD IMAGE').props('accept=".jpg, .jpeg, .png" color=primary flat bordered').classes('flex-1 text-lg font-bold h-32 border-2 border-dashed border-primary/50 hover:bg-primary/10 transition-colors')
                    
                    # Camera (Fixed width)
                    with ui.column().classes('justify-center'):
                         ui.button('CAMERA', icon='camera_alt', on_click=lambda: camera_capture_dialog(handle_camera_capture)).classes('h-32 px-8 text-lg font-bold bg-slate-800 text-white hover:bg-slate-700 border border-white/10 rounded-xl')

                # Analyze Button (Full width)
                analyze_btn = ui.button('RUN AI ANALYSIS', on_click=run_analysis).classes('w-full h-16 text-xl font-black rounded-xl bg-gradient-to-r from-primary to-secondary hover:scale-105 transition-transform shadow-[0_0_20px_rgba(56,189,248,0.4)] mt-4')

            # --- العمود الأيمن: النتائج ---
            with ui.card().classes('w-full md:w-6/12 glass-card p-8 gap-6 min-h-[600px] border-t-4 border-secondary relative'):
                ui.label('2. DIAGNOSTIC REPORT').classes('text-xl font-bold text-secondary tracking-widest self-start')
                
                # 1. حالة الانتظار
                with ui.column().classes('w-full h-full items-center justify-center text-slate-600 gap-6 absolute inset-0 z-10') as results_placeholder:
                    ui.icon('science', size='8xl').classes('opacity-20')
                    ui.label('Waiting for analysis data...').classes('text-xl font-medium')

                # 2. حالة التحميل
                with ui.column().classes('w-full h-full items-center justify-center gap-6 absolute inset-0 z-20 hidden bg-black/50 backdrop-blur-sm') as loading_spinner:
                    ui.spinner(size='4xl', color='primary', type='dots')
                    ui.label('Processing Image...').classes('text-2xl font-bold text-white animate-pulse')

                # 3. محتوى النتائج
                with ui.column().classes('w-full gap-6 hidden z-10') as results_content:
                    # الرأس: الفئة والثقة
                    with ui.row().classes('w-full items-center justify-between bg-white/5 p-6 rounded-2xl border border-white/10'):
                        with ui.column().classes('gap-1'):
                            ui.label('DETECTED POLLUTION').classes('text-xs font-bold text-slate-400 tracking-widest uppercase')
                            lbl_class = ui.label('PLASTIC').classes('text-4xl md:text-5xl font-black text-white text-glow')
                        
                        with ui.column().classes('items-end gap-1'):
                            ui.label('CONFIDENCE').classes('text-xs font-bold text-slate-400 tracking-widest uppercase')
                            lbl_conf = ui.label('98%').classes('text-4xl font-bold text-primary')

                    # تبويبات التفاصيل
                    with ui.tabs().classes('w-full text-white bg-transparent') as tabs:
                        ui.tab('Causes', icon='warning').classes('text-lg')
                        ui.tab('Solutions', icon='healing').classes('text-lg')
                        
                    with ui.tab_panels(tabs, value='Causes').classes('w-full bg-transparent text-slate-300'):
                        with ui.tab_panel('Causes').classes('p-0 pt-4'):
                            causes_container = ui.column().classes('w-full gap-4')
                        with ui.tab_panel('Solutions').classes('p-0 pt-4'):
                            solutions_container = ui.column().classes('w-full gap-4')

                def display_result(data):
                    results_placeholder.classes('hidden')
                    results_content.classes(remove='hidden')
                    
                    # تحديث الرأس
                    lbl_class.text = data['class']
                    lbl_conf.text = f"{int(data['confidence'] * 100)}%"
                    
                    # تحديث الأسباب
                    causes_container.clear()
                    with causes_container:
                        for cause in data['details']['causes']:
                            with ui.row().classes('w-full items-start gap-4 bg-red-500/10 p-4 rounded-xl border border-red-500/20'):
                                ui.icon('error_outline', color='red-400', size='md').classes('mt-1')
                                ui.label(cause).classes('text-lg leading-relaxed flex-1')

                    # تحديث الحلول
                    solutions_container.clear()
                    with solutions_container:
                        for sol in data['details']['solutions']:
                            with ui.row().classes('w-full items-start gap-4 bg-green-500/10 p-4 rounded-xl border border-green-500/20'):
                                ui.icon('check_circle_outline', color='green-400', size='md').classes('mt-1')
                                ui.label(sol).classes('text-lg leading-relaxed flex-1')
                    
                    ui.notify('Analysis Completed Successfully!', type='positive')

# --- صفحة الشات بوت (Chatbot Page) ---
@ui.page('/chatbot')
def chatbot_page():
    """
    صفحة الشات بوت الذكي - تفتح في تبويب جديد
    تستخدم Google Gemini API للإجابة على الأسئلة
    """
    import google.generativeai as genai
    from PIL import Image
    import io
    import base64
    
    # 1. إعداد Google Gemini API
    GEMINI_API_KEY = "AIzaSyDGJklT3afgLQzIzWBuPZhbm8kEn58t84o"
    genai.configure(api_key=GEMINI_API_KEY)
    
    # إنشاء نموذج Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # سجل المحادثة (لحفظ السياق)
    chat_history = []
    chat_state = {'image': None}
    
    setup_ui()  # استخدام نفس التنسيق
    
    # CSS إضافي للشات بوت - تصميم عصري ومحسن
    ui.add_head_html('''
        <style>
            /* خلفية الصفحة */
            body {
                background: linear-gradient(to bottom, #0f172a, #1e293b);
                overflow: hidden; /* لمنع سكرول الصفحة نفسها */
            }
            
            /* حاوية الشات */
            .chat-container {
                scroll-behavior: smooth;
                padding-bottom: 100px !important; /* مساحة للإدخال */
            }
            
            /* تنسيق الرسائل */
            .chat-message {
                animation: slideIn 0.3s ease-out forwards;
                opacity: 0;
                transform: translateY(20px);
                max-width: 80%;
                padding: 1rem 1.5rem;
                font-size: 1.05rem;
                line-height: 1.6;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            
            @keyframes slideIn {
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* رسالة المستخدم */
            .user-message {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                border-radius: 20px 20px 0 20px;
                margin-left: auto;
            }
            
            /* رسالة البوت */
            .bot-message {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #e2e8f0;
                border-radius: 20px 20px 20px 0;
                margin-right: auto;
            }
            
            /* منطقة الإدخال العائمة */
            .input-area {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                width: 90%;
                max-width: 800px;
                z-index: 100;
                background: rgba(15, 23, 42, 0.8);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 8px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            }

            /* مؤشر الكتابة */
            .typing-dot {
                display: inline-block;
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background-color: #94a3b8;
                margin: 0 2px;
                animation: typing 1.4s infinite ease-in-out both;
            }
            
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes typing {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }
        </style>
    ''')
    
    # حاوية الصفحة الكاملة
    with ui.column().classes('w-full h-screen p-0 gap-0'):
        
        # --- رأس الصفحة ---
        with ui.row().classes('w-full p-4 items-center justify-between bg-slate-900/50 backdrop-blur border-b border-white/10 z-10'):
            with ui.row().classes('items-center gap-3'):
                with ui.element('div').classes('w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center shadow-lg'):
                    ui.icon('smart_toy', color='white', size='sm')
                with ui.column().classes('gap-0'):
                    ui.label('EcoBot AI').classes('text-white font-bold text-lg leading-none')
                    ui.label('مساعدك البيئي الذكي').classes('text-slate-400 text-xs')
            
            ui.button(icon='close', on_click=lambda: ui.navigate.to('/', new_tab=False)).props('flat round dense').classes('text-slate-400 hover:text-white hover:bg-white/10')

        # --- منطقة الرسائل (تأخذ باقي المساحة) ---
        chat_container = ui.column().classes('w-full flex-1 overflow-y-auto p-4 gap-6 chat-container')
        
        # رسالة ترحيبية
        with chat_container:
            with ui.row().classes('w-full justify-start'):
                with ui.row().classes('items-end gap-2'):
                    # أيقونة البوت
                    with ui.element('div').classes('w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center flex-shrink-0'):
                        ui.icon('smart_toy', color='green', size='xs')
                    # الرسالة
                    with ui.column().classes('bot-message chat-message'):
                        ui.label('مرحباً بك! 👋').classes('text-lg font-bold text-white mb-1')
                        ui.label('أنا هنا لمساعدتك في كل ما يخص البيئة والاستدامة. تفضل بسؤالي!').classes('text-slate-300')

        # --- منطقة الإدخال (عائمة في الأسفل) ---
        with ui.column().classes('input-area gap-2'):
            
            # معاينة الصورة الملتقطة
            preview_row = ui.row().classes('w-full hidden items-center gap-2 px-4')
            with preview_row:
                with ui.card().classes('w-20 h-20 p-0 relative border border-white/20'):
                    img_preview = ui.image().classes('w-full h-full object-cover rounded')
                    ui.button(icon='close', on_click=lambda: clear_image()).classes('absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full z-10 p-0 min-h-0 text-xs')
                ui.label('Image attached').classes('text-xs text-slate-400')

            def clear_image():
                chat_state['image'] = None
                preview_row.classes(add='hidden')

            async def handle_chat_camera(base64_img):
                if ',' in base64_img:
                    base64_data = base64_img.split(',')[1]
                else:
                    base64_data = base64_img
                
                chat_state['image'] = base64_data
                img_preview.set_source(base64_img)
                preview_row.classes(remove='hidden')

            with ui.row().classes('w-full items-end gap-2'):
                # زر الكاميرا
                ui.button(icon='camera_alt', on_click=lambda: camera_capture_dialog(handle_chat_camera)).props('round flat color=slate-400').classes('mb-1 hover:text-white hover:bg-white/10')

                # زر الميكروفون (تسجيل الصوت)
                async def toggle_recording():
                    if chat_state.get('recording', False):
                        # Stop recording
                        chat_state['recording'] = False
                        mic_btn.props('color=slate-400 icon=mic')
                        mic_btn.classes(remove='animate-pulse text-red-500')
                        
                        audio_b64 = await ui.run_javascript('''
                            if (window.mediaRecorder && window.mediaRecorder.state !== 'inactive') {
                                window.mediaRecorder.stop();
                                return new Promise(resolve => {
                                    window.mediaRecorder.onstop = () => {
                                        const blob = new Blob(window.audioChunks, { type: 'audio/webm' });
                                        const reader = new FileReader();
                                        reader.readAsDataURL(blob);
                                        reader.onloadend = () => resolve(reader.result);
                                    };
                                });
                            }
                            return null;
                        ''')
                        
                        if audio_b64:
                            # معالجة الصوت وإرساله
                            if ',' in audio_b64:
                                audio_data = audio_b64.split(',')[1]
                            else:
                                audio_data = audio_b64
                                
                            # عرض رسالة صوتية في الشات
                            with chat_container:
                                with ui.row().classes('w-full justify-end'):
                                    with ui.column().classes('user-message chat-message items-center gap-2'):
                                        ui.icon('mic', color='white', size='sm')
                                        ui.label('Voice Message').classes('text-xs text-slate-300')
                            
                            ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')
                            
                            # إرسال لـ Gemini
                            try:
                                with chat_container:
                                    typing_row = ui.row().classes('w-full justify-start')
                                    with typing_row:
                                        with ui.row().classes('items-end gap-2'):
                                            with ui.element('div').classes('w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center flex-shrink-0'):
                                                ui.icon('smart_toy', color='green', size='xs')
                                            with ui.element('div').classes('bot-message chat-message py-3 px-4 flex items-center gap-1'):
                                                ui.html('<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>', sanitize=False)
                                
                                ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')

                                context = "أنت مساعد بيئي. المستخدم أرسل رسالة صوتية. استمع إليها وأجب."
                                response = await run.io_bound(model.generate_content, [context, {'mime_type': 'audio/webm', 'data': base64.b64decode(audio_data)}])
                                bot_reply = response.text
                                
                                typing_row.delete()
                                
                                with chat_container:
                                    with ui.row().classes('w-full justify-start'):
                                        with ui.row().classes('items-end gap-2'):
                                            with ui.element('div').classes('w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center flex-shrink-0'):
                                                ui.icon('smart_toy', color='green', size='xs')
                                            with ui.column().classes('bot-message chat-message'):
                                                ui.markdown(bot_reply).classes('text-slate-300 markdown-body')
                                
                                ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')
                                
                            except Exception as e:
                                if 'typing_row' in locals(): typing_row.delete()
                                ui.notify(f'Error processing audio: {str(e)}', type='negative')

                    else:
                        # Start recording
                        chat_state['recording'] = True
                        mic_btn.props('color=red icon=stop')
                        mic_btn.classes(add='animate-pulse text-red-500')
                        
                        await ui.run_javascript('''
                            navigator.mediaDevices.getUserMedia({ audio: true })
                                .then(stream => {
                                    window.mediaRecorder = new MediaRecorder(stream);
                                    window.audioChunks = [];
                                    window.mediaRecorder.ondataavailable = event => {
                                        window.audioChunks.push(event.data);
                                    };
                                    window.mediaRecorder.start();
                                })
                                .catch(err => alert("Microphone access denied: " + err));
                        ''')

                mic_btn = ui.button(icon='mic', on_click=toggle_recording).props('round flat color=slate-400').classes('mb-1 hover:text-white hover:bg-white/10')

                # حقل الإدخال
                user_input = ui.textarea(placeholder='اكتب رسالتك هنا...').props('borderless autogrow rows=1 input-class="text-white max-h-32"').classes('flex-1 text-lg px-4 py-2 bg-transparent text-white')
                
                # دالة الإرسال
                async def send_message():
                    message = user_input.value.strip()
                    if not message and not chat_state['image']: return
                    
                    # 1. عرض رسالة المستخدم
                    with chat_container:
                        with ui.row().classes('w-full justify-end'):
                            with ui.row().classes('items-end gap-2'):
                                # الرسالة
                                with ui.column().classes('user-message chat-message'):
                                    if chat_state['image']:
                                        ui.image(img_preview.source).classes('w-48 rounded-lg mb-2')
                                    if message:
                                        ui.label(message).classes('text-white')
                                # أيقونة المستخدم
                                with ui.element('div').classes('w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0'):
                                    ui.icon('person', color='white', size='xs')
                    
                    # مسح الحقل والسكرول
                    user_input.value = ''
                    current_image = chat_state['image'] # Capture current image
                    clear_image()
                    
                    ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')
                    
                    # 2. مؤشر الكتابة
                    with chat_container:
                        typing_row = ui.row().classes('w-full justify-start')
                        with typing_row:
                            with ui.row().classes('items-end gap-2'):
                                with ui.element('div').classes('w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center flex-shrink-0'):
                                    ui.icon('smart_toy', color='green', size='xs')
                                with ui.element('div').classes('bot-message chat-message py-3 px-4 flex items-center gap-1'):
                                    ui.html('<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>', sanitize=False)
                    
                    ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')
                    
                    # 3. استدعاء Gemini
                    try:
                        context = "أنت مساعد بيئي ودود ومحترف. أجب باللغة العربية.\n\n"
                        
                        content = [context + message]
                        if current_image:
                            img_bytes = base64.b64decode(current_image)
                            image = Image.open(io.BytesIO(img_bytes))
                            content.append(image)
                        
                        # print(f"Sending to Gemini: {message} + Image: {bool(current_image)}")
                        response = await run.io_bound(model.generate_content, content)
                        bot_reply = response.text
                        # print("Response received")
                        
                        # حذف المؤشر
                        typing_row.delete()
                        
                        # عرض الرد
                        with chat_container:
                            with ui.row().classes('w-full justify-start'):
                                with ui.row().classes('items-end gap-2'):
                                    with ui.element('div').classes('w-8 h-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center flex-shrink-0'):
                                        ui.icon('smart_toy', color='green', size='xs')
                                    with ui.column().classes('bot-message chat-message'):
                                        ui.markdown(bot_reply).classes('text-slate-300 markdown-body')
                        
                    except Exception as e:
                        typing_row.delete()
                        print(f"Error: {e}")
                        ui.notify(f'خطأ: {str(e)}', type='negative')
                    
                    # سكرول نهائي
                    ui.run_javascript('var el = document.querySelector(".chat-container"); el.scrollTop = el.scrollHeight;')
    
                # زر الإرسال
                ui.button(icon='send', on_click=send_message).props('round flat color=blue').classes('mb-1 hover:bg-blue-500/20')
                
                # Enter للإرسال (Shift+Enter لسطر جديد)
                user_input.on('keydown.enter.prevent', lambda e: send_message() if not e.args['shiftKey'] else None)



if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='EcoVision - Plastic Pollution', favicon='🌍', dark=True)

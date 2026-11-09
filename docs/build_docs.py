# -*- coding: utf-8 -*-
"""生成任务三的两个交付物：项目复盘报告（docx）+ 答辩 PPT（pptx）"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from pptx import Presentation
from pptx.util import Inches, Pt as PPt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

OUT_DIR = r"D:\Projects\personal-homepage\docs"
os.makedirs(OUT_DIR, exist_ok=True)

NAME = "韦林非凡"
SID = "1244030126"
TEAM = "韦林非凡（队长）、邱梓明、徐伟淞、钟富宁"
TEACHER = "陶成蹊"

# ============================================================
# 一、复盘报告 docx
# ============================================================
doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)
sec.left_margin = Cm(2.8); sec.right_margin = Cm(2.8)

st = doc.styles["Normal"]
st.font.name = "宋体"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(6)


def title(t, size=18):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(t); r.font.name = "黑体"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    r.font.size = Pt(size); r.bold = True
    p.paragraph_format.space_after = Pt(10)


def sub(t, size=11):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(t); r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(4)


def h2(t):
    p = doc.add_paragraph()
    r = p.add_run(t); r.font.name = "黑体"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    r.font.size = Pt(14); r.bold = True
    p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(6)


def para(t):
    p = doc.add_paragraph(t)
    p.paragraph_format.first_line_indent = Pt(24)
    return p


def bullet(t):
    p = doc.add_paragraph(t, style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    return p


title("个人介绍静态主页 · 项目复盘报告")
sub("《Web 前端开发》课程项目 · 任务三（页面集成、优化部署与复盘）")
sub("团队：%s　　姓名：%s　　学号：%s　　指导教师：%s" % (TEAM, NAME, SID, TEACHER))
sub("线上地址：https://tomoririri.github.io/-/　　（GitHub Pages · main 分支自动部署）")

h2("一、这个项目做了什么")

para("这次做的是一份个人介绍静态主页。它只有一页，但要在一页里把该有的东西都放进去："
     "我是谁、会什么、做过什么、怎么联系我。技术上有两个明确的要求，一是语义化，"
     "二是组件化——页头、导航、页脚不能每页写一遍。")

para("最终交付的是一套可复用的组件，加上一个用这些组件搭起来的演示页面。"
     "整个站点没有用任何框架，没有构建步骤，双击 html 就能跑（组件引入需要本地起个 http 服务）。")

h2("二、组件是怎么拆的")

para("拆组件这件事，一开始我想得比较简单：把 header 和 footer 各切一块不就完了。"
     "实际动手才发现，真正要先定的是「什么算一个组件」。")

para("我最后定的标准是：一段结构如果会在多个页面重复出现，并且只靠 CSS 变量和固定类名就能改样式，"
     "它才配单独成为一个组件。按这个标准，页头和导航拆成了两个文件——"
     "因为有的页面需要 Logo，有的页面只想要一条导航。")

bullet("header.html：品牌区 + 导航 + 汉堡按钮，整站通用")
bullet("nav.html：只含导航，页头之外的地方（比如侧栏）也能用")
bullet("footer.html：版权、站内链接、年份（年份由脚本自动写，不用每年手改）")
bullet("common.css：设计令牌 + 三个组件的样式 + 响应式")
bullet("common.js：导航开关、菜单外点击收起、ESC 收起、视口变化复位")

h2("三、样式统一靠什么守住")

para("老师反复强调「全站风格统一」。我的做法是先把设计令牌定死在 :root 里，组件里只许引用变量，"
     "不许写死颜色值。主色 #2F6BFF、正文色 #4A5462、间距基数 8px、圆角 12px，"
     "这些数字直接来自设计阶段的说明书。")

para("好处很直接：后面想换主色，改一行就够。坏处也有——一开始不习惯，总想直接写 #2F6BFF，"
     "写着写着就绕回去了。后来我给自己定了个规矩，提交前搜一遍十六进制色值，"
     "除了 :root 里那几行，别处出现就算错。")

h2("四、响应式踩的三个坑")

para("第一个坑是导航。桌面端横排没问题，一到手机就挤成一团。改成抽屉式之后又出了新问题："
     "菜单打开时页面能跟着滚，底下的内容会跟着动。后来给 body 加了个状态类，锁住滚动才干净。")

para("第二个坑是「从手机宽度拉回桌面」。菜单如果是在手机尺寸下打开的，拉宽之后它还是展开状态，"
     "但按钮已经藏起来了，关不掉。解决办法是监听断点变化，跨过去就复位。")

para("第三个坑是无障碍。一开始菜单只有视觉上的展开收起，键盘用户按 Tab 到汉堡按钮之后，"
     "不知道菜单是开还是关。加了 aria-expanded 和 aria-controls 之后，屏幕阅读器才读得出来。"
     "顺手还加了跳到主内容的链接——用键盘的人才用得上，但他们真的需要。")

h2("五、验证做了什么")

para("交付前我按四个维度自查了一遍。语义化方面，全站没有一坨 div，分区标签都用上了，"
     "装饰性图标加了 aria-hidden，图片都有 alt。响应式方面，在 768px 和 480px 两个断点各看了一遍，"
     "导航、卡片、页脚都没有溢出或者重叠。")

para("代码复用方面，页面里没有一行重复的样式，三个组件在演示页里是引入的，不是复制的。"
     "还原度方面，颜色、间距、圆角全部对齐设计令牌。")

h2("六、还差什么")

para("诚实地说，有三件事没做到位。")

para("一是没做真正的多页验证。这次只做了首页，组件复用的好处是「理论上」的，"
     "没有一个真实的第二页来证明它确实省事。如果时间够，我想再加一个作品详情页，"
     "那才叫验证。")

para("二是打包方式比较土。纯静态站没有构建工具，组件是靠 fetch 在运行时拼进去的，"
     "直接双击 html 打开会失败，必须起本地服务。这在部署之后没有问题，但对第一次拿到代码的人不友好。"
     "下次我会补一个说明或者换一种引入方式。")

para("三是性能只做了常识级优化。没有做图片懒加载，没有算首屏时间，也没有跑 Lighthouse。"
     "页面现在很轻是「因为它本来就小」，不是因为我优化过。")

h2("七、学到了什么")

para("最大的收获不是会写 Flexbox，而是明白了「先定规则再写代码」省事。"
     "令牌先定好，后面写样式基本不用纠结颜色；命名先按 BEM 定好，"
     "改一个组件的时候不会担心碰到别的。")

para("第二个收获是：能被别人复用的代码，不是「我觉得通用」，而是「我在第二个地方真的用过」。"
     "这次只有一页，所以复用的说服力其实不够。这是我下一步最想补的。")

para("最后一条，关于验收。以前我写完就交了，这次按评分维度一条条对着检查，"
     "发现了两处自己没注意到的问题：手机端点开菜单以后点链接，菜单不会自动收起来。"
     "这种问题自己用鼠标点的时候不会碰到，但手机上一定会碰到。")

doc.save(os.path.join(OUT_DIR, "%s-项目复盘报告.docx" % NAME))

# ============================================================
# 二、答辩 PPT
# ============================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

PRIMARY = RGBColor(0x2F, 0x6B, 0xFF)
INK = RGBColor(0x1B, 0x20, 0x27)
BODY = RGBColor(0x4A, 0x54, 0x62)
MUTED = RGBColor(0x8A, 0x94, 0xA3)
SOFT = RGBColor(0xF6, 0xF8, 0xFB)

BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def text(slide, s, left, top, width, height, size=18, color=BODY, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); r.text = s
    r.font.size = PPt(size); r.font.bold = bold; r.font.color.rgb = color
    r.font.name = "微软雅黑"
    return box


def bullets(slide, items, left, top, width, height, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = PPt(10)
        r = p.add_run(); r.text = "· " + it
        r.font.size = PPt(size); r.font.color.rgb = BODY; r.font.name = "微软雅黑"
    return box


def bar(slide, color=PRIMARY, left=Inches(0.9), top=Inches(1.35), w=Inches(1.1)):
    sh = slide.shapes.add_shape(1, left, top, w, PPt(6))
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()


# 1 封面
s = add_slide()
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = SOFT; bg.line.fill.background()
text(s, "个人介绍静态主页", Inches(0.9), Inches(2.2), Inches(11), Inches(1.0), 44, INK, True)
text(s, "基于组件化与语义化的前端实践", Inches(0.9), Inches(3.3), Inches(11), Inches(0.6), 22, BODY)
text(s, "线上演示：https://tomoririri.github.io/-/", Inches(0.9), Inches(4.85), Inches(11), Inches(0.4), 14, PRIMARY)
text(s, "团队 %s　　姓名 %s　　学号 %s　　指导教师 %s" % (TEAM, NAME, SID, TEACHER),
     Inches(0.9), Inches(4.4), Inches(11), Inches(0.5), 14, MUTED)

# 2 项目目标
s = add_slide()
text(s, "这个项目要解决什么", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "做一份个人介绍静态主页：我是谁、会什么、做过什么、怎么联系",
    "技术上只提两个要求：语义化标签、组件化复用",
    "不用框架、不用构建工具，纯手写 HTML / CSS / JS",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.5), 20)

# 3 组件拆分
s = add_slide()
text(s, "组件是怎么拆的", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
text(s, "判断标准：会在多处重复出现，并且只靠变量和固定类名就能改样式",
     Inches(0.9), Inches(1.75), Inches(11.4), Inches(0.5), 16, MUTED)
bullets(s, [
    "header.html —— 品牌区 + 导航 + 汉堡按钮，整站通用",
    "nav.html —— 只含导航，页头之外也能用",
    "footer.html —— 版权与站内链接，年份由脚本写入",
    "common.css —— 设计令牌 + 组件样式 + 响应式",
    "common.js —— 菜单开关、点击外部收起、ESC 收起、断点复位",
], Inches(0.9), Inches(2.5), Inches(11.4), Inches(4.0), 18)

# 4 设计令牌
s = add_slide()
text(s, "风格统一靠设计令牌守住", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "主色 #2559D6　正文 #4A5462　弱化 #6B7583（都过 WCAG AA 4.5:1）",
    "底色 #FFFFFF / #F6F8FB　间距基数 8px　圆角 12px",
    "全部定义在 :root，组件里只引用变量，不写死色值",
    "自查规矩：提交前搜一遍十六进制，除了 :root 那几行，别处出现就算错",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.6), 18)

# 5 响应式
s = add_slide()
text(s, "响应式踩的三个坑", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "菜单打开时页面还能滚，底下内容跟着动 —— 给 body 加状态类锁滚动",
    "从手机宽度拉回桌面，菜单还展开着但按钮已经藏了 —— 监听断点变化复位",
    "只有视觉上的开合，键盘用户不知道状态 —— 补 aria-expanded 与 aria-controls",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.6), 18)

# 6 无障碍
s = add_slide()
text(s, "顺手做的无障碍", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "跳到主内容的链接：键盘用户按 Tab 第一下就能跳过导航",
    "焦点可见：不靠浏览器默认，自己画一圈 outline",
    "装饰图标 aria-hidden，内容图片都有 alt",
    "尊重系统的「减少动态效果」偏好",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.6), 18)

# 7 不足
s = add_slide()
text(s, "还差什么", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "只有一个首页，组件复用的好处还停留在「理论上」",
    "组件靠 fetch 运行时拼入，直接双击 html 打不开，需要本地服务",
    "性能只做了常识级优化，没跑过 Lighthouse，也没做懒加载",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.6), 18)

# 8 收获
s = add_slide()
text(s, "学到的三件事", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "先定规则再写代码：令牌和命名定好，后面基本不用纠结",
    "能复用的代码不是「我觉得通用」，是「我在第二个地方真的用过」",
    "按维度验收能发现问题：手机点开菜单再点链接，菜单不会自动收起，这个用鼠标点不出来",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.8), 18)

# 9 项目结构
s = add_slide()
text(s, "项目结构", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
tree = [
    "personal-homepage/",
    "├─ index.html            演示页，用 data-include 引入组件",
    "├─ components/",
    "│   ├─ header.html       品牌 + 导航 + 汉堡按钮",
    "│   ├─ nav.html          只含导航，可单独复用",
    "│   └─ footer.html       版权与站内链接",
    "├─ css/",
    "│   └─ common.css        设计令牌 + 组件样式 + 响应式",
    "├─ js/",
    "│   ├─ common.js         菜单开关、断点复位、年份",
    "│   └─ include.js        纯静态的组件引入",
    "└─ docs/                 复盘报告与答辩 PPT",
]
box = s.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.4), Inches(4.6))
tf = box.text_frame; tf.word_wrap = True
for i, line in enumerate(tree):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = PPt(2)
    r = p.add_run(); r.text = line
    r.font.size = PPt(14); r.font.name = "Consolas"
    r.font.color.rgb = INK if i == 0 else BODY

# 10 分工
s = add_slide()
text(s, "小组分工", Inches(0.9), Inches(0.8), Inches(11), Inches(0.7), 30, INK, True)
bar(s)
bullets(s, [
    "韦林非凡（队长）—— 前端实现与统筹：组件拆分、样式令牌、响应式、无障碍，文档与答辩",
    "邱梓明 —— 测试与验收：多端检查、问题记录",
    "徐伟淞 —— 需求与内容：文案梳理、文档校对",
    "钟富宁 —— 视觉与素材：截图、图标与版式核对",
], Inches(0.9), Inches(2.0), Inches(11.4), Inches(3.2), 18)
text(s, "（分工按小组记录整理，答辩时按实际情况说明）",
     Inches(0.9), Inches(5.6), Inches(11.4), Inches(0.5), 14, MUTED)

# 11 结尾
s = add_slide()
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = SOFT; bg.line.fill.background()
text(s, "谢谢老师", Inches(0.9), Inches(2.9), Inches(11), Inches(0.9), 40, INK, True, PP_ALIGN.CENTER)
text(s, "请提问", Inches(0.9), Inches(3.9), Inches(11), Inches(0.6), 20, MUTED, False, PP_ALIGN.CENTER)

prs.save(os.path.join(OUT_DIR, "%s-项目答辩.pptx" % NAME))

print("docx:", os.path.join(OUT_DIR, "%s-项目复盘报告.docx" % NAME))
print("pptx:", os.path.join(OUT_DIR, "%s-项目答辩.pptx" % NAME))

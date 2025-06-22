from nicegui import ui
from sqlalchemy.orm import Session
from sqlalchemy import or_
import math
from database import Base
from models.user import User
from database import SessionLocal


class MyRichTable():

    def __init__(model: Base):
        pass

filter_inputs = {}
def get_model_columns(model: Base):
    """返回模型所有字段名及类型，排除关系字段"""
    return [(c.name, str(c.type)) for c in model.__table__.columns]

def refresh_table():
        # nonlocal current_page, order_by, order_desc, visible_columns

        # 读筛选条件
        filters = {k: v.value for k, v in filter_inputs.items()}

        # 读列显示状态
        # visible_columns = [k for k, cb in col_checkboxes.items() if cb.value]

        # 读分页和排序状态
        # current_page = table.page
        # page_size = table.rows_per_page
        # order_by = table.sort_field
        # order_desc = table.sort_order == 'desc'

        # 查询数据
        # data, total = query_model(session, model, filters, current_page, page_size, order_by, order_desc)

        # 更新列和行
        table.columns = [c for c in table_columns if c['name'] in visible_columns]
        table.rows = data_to_rows(data, columns, visible_columns)

def create_filter_inputs(columns, batch=4):
    """根据字段动态创建筛选输入框，返回字典{字段名: input控件}"""
    inputs = {}
    row = None
    for i in range(0,len(columns),batch):
        with ui.row().style('margin-bottom: 8px;') as row:
            for j, (name, _) in enumerate(columns[i:i+batch]):
                inp = ui.input(label=name).style('width: 300px;').props('clearable')
                inp.on('keydown.enter',refresh_table) 
                inputs[name] = inp
    return inputs

def query_model(session: Session, model, filters, page, page_size, order_by, order_desc):
    q = session.query(model)
    # 模糊查询条件组合
    # conditions = []
    # for field, value in filters.items():
    #     if value:
    #         conditions.append(getattr(model, field).like(f'%{value}%'))
    # if conditions:
    #     q = q.filter(*conditions)
    # # 排序
    # if order_by:
    #     col = getattr(model, order_by)
    #     q = q.order_by(col.desc() if order_desc else col.asc())
    # total = q.count()
    # 分页
    # results = q.offset((page-1)*page_size).limit(page_size).all()
    results = q.all()
    total = len(results)
    return results, total

def data_to_rows(data, columns, visible_columns):
    """转成表格展示行，只包含可见列"""
    rows = []
    for item in data:
        row = []
        # print('item',getattr(item, 'username'))
        row = {col_name[0]: getattr(item, col_name[0]) for col_name in columns}
        # for col_name, _ in columns:
        #     if col_name in visible_columns:
        #         val = getattr(item, col_name)
        #         row.append({str(val) if val is not None else '')
        rows.append(row)
    return rows



def build_table_ui(model):
    columns = get_model_columns(model)  # 所有列
    visible_columns = set([c[0] for c in columns])  # 默认都显示
    page_size = 10
    current_page = 1
    order_by = None
    order_desc = False

    session = SessionLocal()

    # 顶部筛选区
    filter_inputs = create_filter_inputs(columns)
    # 中间按钮区
    with ui.row().classes('gap-2 my-2').style('justify-content: flex-end; width: 100%') as button_row:
        btn_query = ui.button('查询',icon='search',on_click=refresh_table)
        ui.button('新增')
        ui.button('修改')
        ui.button('删除')
        ui.button('导入')
        ui.button('导出')
        ui.button('对比')

    ui.separator()

    # 下方列控制复选框
    with ui.expansion('列显示/隐藏'):
        col_checkboxes = {}
        with ui.row():
            for col_name, _ in columns:
                cb = ui.checkbox(col_name, value=True)
                col_checkboxes[col_name] = cb

    # 表格初始化
    table_columns = [{'name': c[0], 'label': c[0], 'field': c[0], 'sortable':True ,'alignment':'align'} for c in columns]
    table = ui.table(
        columns=[c for c in table_columns if c['name'] in visible_columns],
        rows=[],
        row_key='name',
        selection='multiple',
        pagination=20
    ).classes('w-full')

    # for filter_input in filter_inputs:
        # filter_inputs[filter_input].bind_value(table,'filter')
        # filter_inputs = create_filter_inputs(columns)

    # 初始化页码
    # update_table()


    
        # table.total = total

    # 查询按钮绑定
    btn_query.on('click', lambda e: refresh_table())

    # 初始加载
    # refresh_table()

    # 表格排序分页监听
    def on_sort(event):
        refresh_table()
    def on_page(event):
        refresh_table()

    # table.on('sort', on_sort)
    # table.on('page', on_page)

    # 双击行进入详情页
    # @table.on('row_dblclick')
    def on_row_dblclick(event):
        index = event.args['row']
        data, _ = query_model(session, model, {k: v.value for k, v in filter_inputs.items()}, current_page, page_size, order_by, order_desc)
        item = data[index]
        ui.notify(f'进入详情页：{item}')  # 你可以替换成真正的跳转逻辑

    return ui.column()

# 启动界面示例
# ui.page('/table')(lambda: build_table_ui(MyModel))

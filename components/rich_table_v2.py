from nicegui import ui
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from database import SessionLocal
from sqlalchemy import func

class RichTable:
    def __init__(self, model, rows_per_page=10):
        self.model = model
        self.model_columns = inspect(model).columns
        print('model_columns',self.model_columns)
        print(f'{list(self.model_columns)=}')
        self.rows_per_page = rows_per_page
        self.current_page = 1
        self.filters = {}

        with ui.column().classes('w-full'):

            self._build_filter_inputs()

            self._build_buttons()
            ui.separator()
            self._build_table()

    def _build_filter_inputs(self):
        self.inputs = {}
        self.input_row = ui.row().classes('w-full')
        columns = list(self.model_columns)
        batch = 4
        for i in range(0,len(columns),batch):
            with ui.row().style('margin-bottom: 8px;') as row:
                for j, col in enumerate(columns[i:i+batch]):
                    inp = ui.input(label=col.name).style('width: 300px;').props('clearable')
                    # inp.on('keydown.enter',refresh_table) 
                    self.inputs[col.name] = inp

    def _build_buttons(self):
        with ui.row().classes('my-2').style('justify-content: flex-end; width: 100%') :
            ui.button('查询',icon='search', on_click=self.query_data)
            ui.button('新增',icon='add', on_click=self.create_data)
            ui.button('导入',icon='upload', on_click=self.create_data)
            ui.button('导出',icon='download', on_click=self.create_data)
            ui.button('修改',icon='update', on_click=self.modify_data)
            ui.button('删除',icon='delete', on_click=self.delete_data)
            ui.button('刷新',icon='refresh', on_click=self.refresh_data)

    def _build_table(self):
        self.table = ui.table(
            columns=[{'name': col.name, 'label': col.name, 'field': col.name, 'sortable': True}
                     for col in self.model_columns],
            rows=[],
            row_key='name',
            selection='multiple',
            pagination=self.rows_per_page,
            on_pagination_change=self.on_page_change,
            # pagination=True,
            # rows_per_page=self.rows_per_page,
        ).classes('w-full').props('max-pages:100')

        # self.table.on('update:page', self.on_page_change)
        self.refresh_data()

    def get_filter_conditions(self):
        conditions = []
        for name, input_box in self.inputs.items():
            value = input_box.value
            if value:
                col = getattr(self.model, name)
                if isinstance(col.type, String):
                    conditions.append(col.like(f"%{value}%"))
                else:
                    try:
                        conditions.append(col == type(col.type.python_type)(value))
                    except:
                        continue
        return conditions

    def query_data(self):
        self.current_page = 1
        self.refresh_data()

    def refresh_data(self):
        print('refresh_data')
        session = SessionLocal()
        stmt = select(self.model)

        filters = self.get_filter_conditions()
        print('filters',filters)
        if filters:
            stmt = stmt.where(*filters)

        total_items = session.scalar(select(func.count()).select_from(stmt.subquery()))
        print(total_items,'total_items')
        stmt = stmt.offset((self.current_page - 1) * self.rows_per_page).limit(self.rows_per_page)
        results = session.execute(stmt).scalars().all()
        print('result',results)
        session.close()
        print(self.model_columns)
        # [{self.model_columns}]
        columns = list(self.model_columns)
        rows = [{col.name:getattr(row,col.name) for col in columns} for row in results]


        # self.table.rows = [row.__dict__ for row in results]
        self.table.pagination = {
            'page': self.current_page,
            'rowsPerPage': self.rows_per_page,
            # 'rows_number': total_items,
        }
        self.table.rows = rows

    def on_page_change(self, e):
        print(e)
        # self.current_page = e.args
        self.refresh_data()

    def create_data(self):
        ui.notify("新增功能待实现")

    def modify_data(self):
        ui.notify("修改功能待实现")

    def delete_data(self):
        ui.notify("删除功能待实现")
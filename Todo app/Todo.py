# Flet Todo App Mobile IOS/ANDRIOD
import flet as ft 


# Seperate the style sheet for the component in a dict

_dark: str = ft.Colors.with_opacity(0.5, "white")
_light: str = ft.Colors.with_opacity(1, "black")

toggle_style_sheet: dict = {"icon": ft.Icons.DARK_MODE_ROUNDED, "icon_size": 18}
add_style_sheet: dict = {"icon": ft.Icons.ADD_ROUNDED, "icon_size": 18}

item_style_sheet: dict = {
    "height": 50, 
    "expand": True,
    "border_color": _dark,
    "cursor_height": 24,
    "hint_text": "Add your todo item here...",
    "content_padding": 15,
}

todo_item_style_sheet: dict = {"height": 50, "border_radius": 4}

# create a class for each todo item
class ToDoItem(ft.Container):
    # Before we initialize the container and send it to the UI,
    # we can check the theme to set the border color
    
    def __init__(self, hero: object, description: str, theme: str) -> None:
        if theme == "dark":
            todo_item_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            todo_item_style_sheet["border"] = ft.border.all(1, _light)
            
        super().__init__(**todo_item_style_sheet)
        self.hero: object = hero
        self.description: str = description
        
        self.tick = ft.Checkbox()
        
        self.text: ft.Text = ft.Text(
            spans=[ft.TextSpan(text=self.description)], size=14
        )
        self.delete: ft.IconButton = ft.IconButton(
            icon=ft.Icons.DELETE_ROUNDED,
            icon_color="#F10B0BFF",
            on_click=lambda e: self.delete_text(e),
        )
        #self.editView: ft.IconButton = ft.IconButton(
          #  icon=ft.Icons.EDIT_OUTLINED,
            #on_click=lambda e: self.saveClick(e),
            #                )
        
        self.content: ft.Row = ft.Row(
            alignment="spaceBetween",
            controls=[
                ft.Row(controls=[self.tick, self.text]),
                self.delete, #self.editView,
            ],
        )
        
    # method to strike out text if checkbox is clicked
    def strike(self, e) -> None:
        if e.control.value is True:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
        else:
            self.text.spans[0].style = ft.TextStyle()
            
        self.text.update()
        
    # method to delete an item from the list 
    def delete_text(self, e) -> None: 
        self.hero.todo_area.controls.remove(self)
        self.hero.todo_area.update()
        self.hero.item_size()
        
    def editClick(self, e):
        pass 
    
    def saveClick(self, e):
        pass 
# main content area
class Hero(ft.SafeArea):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(content=11, maintain_bottom_view_padding=True)
        self.page = page 
        self.title: ft.Text = ft.Text("TODO LIST", size=20, weight="w800")
        self.toggle: ft.IconButton = ft.IconButton(
            **toggle_style_sheet, on_click=lambda e: self.switch(e)
        )
        self.item: ft.TextField = ft.TextField(**item_style_sheet)
        self.add: ft.IconButton = ft.IconButton(
            **add_style_sheet, on_click=lambda e: self.add_item(e)
        )
        
        self.todo_area: ft.Column = ft.Column(expand=True, spacing=8)
        self.counter: ft.Text = ft.Text("0 items", italic=True)
        
        self.main: ft.Column = ft.Column(
            controls=[
                ft.Row(
                    alignment="SpaceBetween",
                    controls=[self.title, self.toggle],
                ),
                #ft.Divider(height=20),
                ft.Divider(height=10, color="tranparent"),
                ft.Text("1. Add your todo item below"),
                ft.Row(controls=[self.item, self.add], alignment="SpaceBetween"),
                ft.Divider(height=10, color="tranparent"),
                ft.Row(
                    alignment="SpaceBetween",
                    controls=[
                        ft.Text("2. List of todo items."),
                        self.counter,
                    ],
                ),
                self.todo_area,
            ]
        )
        
        self.content = self.main
        
        # we can keep track of the number of items in the list
    def item_size(self)-> None:
        if len(self.todo_area.controls[:]) == 4:
            self.counter.value = f"{len(self.todo_area.controls[:])} item"
            
        else: 
            self.counter.value = f"{len(self.todo_area.controls[:])} items"

        self.counter.update()
        
    def add_item(self, e) -> None:
        if self.item.value != "":
            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.todo_area.controls.append(ToDoItem(self, self.item.value, "dark"))
            else:
                self.todo_area.controls.append(ToDoItem(self, self.item.value, "light"))
                
            self.todo_area.update()
            self.item_size()
            self.item.value = ""
            self.item.update()
            
        else:
            pass 
    
    def switch(self, e) -> None:
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon = ft.Icons.LIGHT_MODE_ROUNDED
            self.item.border_color = _light
            
            for item in self.todo_area.controls[:]:
                item.border = ft.border.all(1, _light)
            
        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon = ft.Icons.DARK_MODE_ROUNDED
            #self.item.border_color = _dark 
            
            for item in self.todo_area.controls[:]:
                item.border = ft.border.all(1, _dark)
            
        self.page.update()

def main(page: ft.Page) -> None:
    page.title = "TODO APP"
    page.window.width = 320
    page.window.height = 660
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.DARK
    theme = ft.Theme()
    page.theme = theme
    
    hero: object = Hero(page)
    page.add(hero)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)# view=ft.WEB_BROWSER)
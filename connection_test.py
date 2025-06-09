# import flet as ft
# import httpx  # Or you can use httpx

# def main(page: ft.Page):
#     def get_data(e):
#         try:
#             response = httpx.get("http://localhost:8087/user-management/product/detail?id=2")
#             if response.status_code == 200:
#                 data = response.json()  # Assuming the server returns JSON
#                 output.value = str(data)
#             else:
#                 output.value = f"Error {response.status_code}"
#         except Exception as ex:
#             output.value = f"Exception: {ex}"
#         page.update()

#     output = ft.Text()
#     btn = ft.ElevatedButton("Fetch Data", on_click=get_data)
#     page.add(btn, output)

# ft.app(target=main)


import flet as ft
import httpx
import json

def main(page: ft.Page):
    name_field = ft.TextField(label="Item Name", width=300)
    descripcion_field = ft.TextField(label="descripcion", width=300)
    result_text = ft.Text()
    id_field = ft.TextField(label="Product ID", width=300)
    list_field = ft.TextField(label="Search as list", width=300)
    output = ft.Text()

    #create function
    def create_item(e):
        try:
            data = {
                "name": name_field.value,
                "descripcion":descripcion_field.value,
                "idBrand": 1, 
                "idCategory": 1, 
                "idSubCategory":1
            }
            response = httpx.post(
                "http://localhost:8087/user-management/product",
                headers={"Content-Type": "application/json"},
                content=json.dumps(data)
            )
            if response.status_code == 201:
                result_text.value = "✅ Item created successfully!"
                name_field.value = ""
                descripcion_field.value = ""
            else:
                result_text.value = f"❌ Error {response.status_code}: {response.text}"
        except Exception as ex:
            result_text.value = f"⚠️ Exception: {ex}"
        page.update()

    #get function
    def get_data(e):
        try:
            product_id = id_field.value
            if not product_id:
                output.value = "⚠️ Please enter a product ID."
                # need to proof if ID is a name
            else:
                url = f"http://localhost:8087/user-management/product/detail?id={product_id}"
                response = httpx.get(url)
            if response.status_code == 200:
                data = response.json()  # Assuming the server returns JSON
                output.value = str(data)
            else:
                output.value = f"Error {response.status_code}"
        except Exception as ex:
            output.value = f"Exception: {ex}"
        page.update()

    #get list function
    def get_list(e):
        try:
            product_id = list_field.value
            if not product_id:
                output.value = "⚠️ Please enter a product Name."
            else:
                url = f"http://localhost:8087/user-management/product/list?name={product_id}"
                response = httpx.get(url)
            if response.status_code == 200:
                data = response.json()  # Assuming the server returns JSON
                output.value = str(data)
            else:
                output.value = f"Error {response.status_code}"
        except Exception as ex:
            output.value = f"Exception: {ex}"
        page.update()

    id_search_btn = ft.ElevatedButton("Get Data", on_click=get_data)
    create_btn = ft.ElevatedButton("Create Item", on_click=create_item)
    list_search_btn = ft.ElevatedButton("Search Name", on_click=get_list)

    page.add(
        ft.Column([
            name_field,
            descripcion_field,
            create_btn,
            id_field,
            id_search_btn,
            result_text, 
            list_field,
            list_search_btn,
            output
        ])
    )

ft.app(target=main)
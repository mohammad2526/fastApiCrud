from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
class Item (BaseModel):
    name:str
    price:float
    brand: Optional[str]="Regular"  #regular is an optional va;ue,
            # if we dont enter any value then it wil l be defau;lt

class UpdateItem(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    brand:Optional[str]=None

inventory={
    # 1:{
    #     "name": "milk",
    #     "price":    3.99,
    #     "brand":    "regular"
    # }
}
@app.get("/")
async def helloWorld():
    return {"Data": "Hello World"}

@app.get('/about')
async def about():
    return {"data":"about Page"}

@app.get("/get-item/{item_id}")
async def get_item(item_id:int = Path(None, description="enter item id which is a positive integer")):
     if item_id not in inventory:
         return {"Error" :  "item not exist"}
     return inventory[item_id]

@app.get("/get-by-name/{item_id}")
async def get_item(*,item_id:int,name : Optional[str] = None ):  #we do not get any error if we not passed
                                    # query params....
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"Data" : "Data not found"}

@app.post("/create-item /{item_id}")
async def create_user(item_id:int,item:Item):
    if item_id in inventory:
        return {"error": "item already exist"}
    # inventory[item_id]={
    #     "name":item.name,
    #     "price":item.price,
    #     "brand":item.brand
    # }

    inventory[item_id]=item #python will TC of this
    return inventory[item_id];


# @app.put("/update-item /{item_id}")
# async def update_item(item_id: int, item: Item):
#     if item_id not in inventory:
#         return {"error": "item not exist"}
#     inventory[item_id].update(item)      # this way need to fill all the
#                                             # attribute value, if not then all will be affected
#     return inventory[item_id];


@app.put("/update-item /{item_id}")
async def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"error": "item not exist"}

    if item.name != None:
        inventory[item_id].name=item.name
    if item.price != None:
        inventory[item_id].price=item.price
    if item.brand != None:
        inventory[item_id].brand=item.brand

    return inventory[item_id];

@app.delete('/delete-item/{item_id}')
async def delete_item(item_id:int):
    if item_id not in inventory:
        return {"Error" : "item id not exis"}

    del inventory[item_id]
    return {"success" : "Item deleted"}

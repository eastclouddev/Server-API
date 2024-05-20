from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from apis import \
    login, logout, password_reset, news, \
    students, mentors, reviews, companies, users, \
    courses, curriculums, questions, billings, receipts, \
    rewards, progresses


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    return "OK"

# ルーターの読み込み
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(password_reset.router)
app.include_router(news.router)
app.include_router(students.router)
app.include_router(mentors.router)
app.include_router(reviews.router)
app.include_router(companies.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(curriculums.router)
app.include_router(questions.router)
app.include_router(billings.router)
app.include_router(receipts.router)
app.include_router(rewards.router)
app.include_router(progresses.router)


from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8080/samplechat/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


@app.get("/samplechat")
async def get():
    return HTMLResponse(html)

manager = ConnectionManager()

@app.websocket("/samplechat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")



html2 = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8080/hogechat/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

# websocketの使い方
# GETメソッドのdefを用意する(基本こいつにアクセスが向く)
# websocketのデコレータを持つdefを用意する(送信の処理でこいつを呼び出す)
# var ws = new WebSocket(`ws://localhost:8080/XXXX/${YYYY}`); html側のこの処理で向き先を変更
# インスタンス名は各双方向通信毎に分ける(Aさん-Bさん、Aさん-Cさんみたいに)

manager_hoge = ConnectionManager()

@app.get("/hogechat")
async def get():
    return HTMLResponse(html2)

@app.websocket("/hogechat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager_hoge.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager_hoge.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager_hoge.disconnect(websocket)
        await manager_hoge.broadcast(f"Client #{client_id} left the chat")
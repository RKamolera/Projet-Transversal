import json
import websocket


class Graph:
    def __init__(self) -> None:
        self.left_data =tuple()
        
    
    def on_message(self, ws, message):
        data = json.loads(message)

        print("************************ je suis un graphe ********************")
        for d in data["data"]:
            self.left_side_table = (d['s'], d['p'], d['v'])
            print(self.left_side_table)


    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"AAPL"}')
        # ws.send('{"type":"subscribe","symbol":"AMZN"}')
        # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
        # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
        pass

    def start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c9324kiad3ic89vi6cmg",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()



if __name__ =="__main__" :
    g= Graph()
    g.start()



# -*- coding: utf-8 -*-
#１つのファイルを任意のバイト数に分割して送受信できるプログラム
# 実行方法は robust/sample 内にこのプログラムファイルを置いて
# 受信側(例) python3 sampleYoshimi.py s 1**.***.***.*** 8000　（ipは受信側のipにすること）
# 送信側(例) python3 sampleYoshimi.py c 1**.***.***.*** 8000　（ipは受信側のipにすること）

# 設計思想
# 1回に送信するデータが小さければジャマーあっても送受信なんとかなるので
# ファイルをある程度のバイト数に分割して最後にくっつければいいよね的なやつ
# あと、性能よりも極力コード量を減らすように意識した(既存のサンプルコードより読みやすいのを目標にした)

# Reference
# 1.Python で Socket 通信 (TCP/UDP サーバ)    https://qiita.com/tick-taku/items/813710328d802829fb4b
# 2.テキストファイルを指定バイト数ごとに分割  https://qiita.com/igarashi_54/items/b879331925a6f76fb00c
# 3.pythonですぐ出来る！ ファイルを転送する方法【TCP通信 応用】
#   https://syachiku-python.com/python%E3%81%A7%E3%81%99%E3%81%90%E5%87%BA%E6%9D%A5%E3%82%8B%EF%BC%81-%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E8%BB%A2%E9%80%81%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%E3%80%90tcp%E9%80%9A%E4%BF%A1/

import socket
import sys

split_byte_size = 4000                      # 分割するバイト数

def split_text_by_byte_size(text, split_byte_size): #ファイルを任意のバイト数に分割する関数
    bytes_text = text                               # １つのファイルの全てのデータ取得
    head = bytes_text[:split_byte_size]             #データの先頭から指定した任意のバイト数のデータを取得
    tail = text[len(head):]                         #分割されていない残りのデータ

    if tail == text: #残りのデータが指定したバイト数より小さければ分割しない
        return []

    split_tail = split_text_by_byte_size(tail, split_byte_size) #データの分割が終わるまで繰り返す（再起）

    results = []                # 分割したデータを格納する変数
    results.append(head)        # 分割したデータを格納
    results.extend(split_tail)  # 最後のデータを格納

    return results

def server(ip, port):
    all= b""                    # 分割されて送られてきたデータを格納する変数
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #アドレスファミリをIPv4(AF_INET),ソケットタイプをTCP(SOCK_STREAM)に指定
        s.bind((ip, port))      # ソケットをバインド
        s.listen(1)

        while True:
            conn, addr = s.accept()
            with conn:
                fname =f"../data/data0"           #受信したファイルのパスを指定
                with open(fname, mode="wb") as f: #ファイルをバイナリモード(書き込み可)で開く
                    while True:
                        data = conn.recv(split_byte_size)    #分割して送られたデータを取得
                        all = all + data          #今までに送られてきたデータと結合
                        # データが送られなくなったらループから抜ける
                        if not data:
                            break
                    f.write(all) #１つのファイルにおける全てのデータを取得したらデータをファイルに保存
                    exit() 

def client(ip, port):
    fname = "../data/data0"                                      #送信するファイルのパスを指定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #アドレスファミリをIPv4(AF_INET),ソケットタイプをTCP(SOCK_STREAM)に指定
        s.connect((ip, port))                                    #サーバ(受信側)に接続
        try:
            with open(fname, mode='rb') as f: #ファイルをバイナリモード(読み取り可)で開く
                text = f.read()               #ファイルのデータを取得
                split_texts = split_text_by_byte_size(
                    text, split_byte_size)    # ファイルを指定したバイト数で取得

                #== 分割した数だけ送信する ====
                for i, split_text in enumerate(split_texts):
                    print(i)              #データの分割数を確認できる 
                    s.sendall(split_text) #分割したデータを送信する
        except:
            pass


if __name__ == "__main__":
    if (sys.argv[1] == "s"):                    # server(受信モード)
        server((sys.argv[2]), int(sys.argv[3])) #ip, port取得
    if (sys.argv[1] == "c"):                    # client(送信モード)
        client((sys.argv[2]), int(sys.argv[3]))
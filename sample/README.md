# 1.Sample Program (sampleYoshimi.py)  

## About  
sampleYoshimi.pyの中に記載。  
## Details  
sampleYoshimi.pyの中に記載。  
## How to run  

```sh
# Run as receier-side
python3 sampleYoshimi.py s 1**.***.***.*** 8000　（***には受信側のipにすること）

# Run as sender-side
python3 sampleYoshimi.py c 1**.***.***.*** 8000　（***には受信側のipにすること）
```

## Performance
ファイル(data0)のみ送信できる :)

- Taro -> Hanako : `OK = 1, FAILED = 0, DUP = 0`
- Hanako -> Taro : `OK = 1, FAILED = 0, DUP = 0`

## Hint to improve this protocol

まずはfor文使って複数のファイルを送信できるように変更しましょう。そのあとは分割するサイズを変えてみたり、sleepを入れてみたり、UDPにしたりなどして下さい

# 2.Sample Program (SCU Protocol)

## About

This sample program is example of the way how you can implement protocol that has robustness. It is written in Python (works on 3.x). You (your group) will try to implement protocol that can beat performance of this protocol.

## Details

By running some tests on trial site, you may realize that as packet is large it is more likely to be corrupted by injected electrical shock. SCU Protocol will split file into unit named `MTU` (check `split_file_into_mtu` function inside `utils.py`), and send it with header that has packet type, id, sequence number. Sender-side will send payload (splitted file) with header that has appropriate data on it. Receiver-side will receive packet and send retransmission request to sender-side when it failed to receive specific fragment of the file.

## How to run

```sh
# Run as sender-side
python3 main.py sender

# Run as receiver-side
python3 main.py receiver
```

## Performance

Slow, but no failure and duplicated files :)

- Taro -> Hanako : `OK = 125, FAILED = 0, DUP = 0`
- Hanako -> Taro : `OK = 56, FAILED = 0, DUP = 0`

## Hint to improve this protocol

Read structure of header (explained at top of the `packet.py`), and think if there are field that is not necessary for this challenge.

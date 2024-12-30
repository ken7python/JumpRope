# Jump Rope Game

このゲームは、プレイヤーがジャンプしてロープを避けるシンプルなゲームです。プレイヤーはスペースキーを押すか、カメラを使用してジャンプ動作を検出することでジャンプできます。

## ゲームの特徴

- カメラを使用してプレイヤーのジャンプ動作を検出
- ジャンプのたびにスコアが増加
- ハイスコアの保存と表示
- ゲームオーバー時にリトライオプション

## 操作方法

- スペースキーを押してジャンプ
- カメラの前でジャンプ動作を行うことでジャンプ

## 必要なライブラリ

- pygame
- opencv-python
- mediapipe

## インストール方法

以下のコマンドを使用して必要なライブラリをインストールしてください。

```bash
pip install pygame opencv-python mediapipe
```

## 実行方法

以下のコマンドを使用してゲームを実行してください。

```bash
python game.py
```

## ゲームの流れ

1. ゲーム開始前に3秒間のカウントダウンが表示されます。
2. カウントダウン後、ゲームが開始されます。
3. プレイヤーはスペースキーを押すか、カメラの前でジャンプ動作を行うことでジャンプします。
4. ジャンプしてロープを避けるたびにスコアが増加します。
5. ロープに当たるとゲームオーバーとなり、ハイスコアが更新されている場合は保存されます。
6. ゲームオーバー後、スペースキーを押すことで再度ゲームを開始できます。

楽しんでください！

using System.Collections.Generic;
using System.IO;
using System.Linq;

public static class RLE
{
    public static void RLE__(string inputFile, string outputFile)
    {
        // ファイル内容読込
        var bytes = File.ReadAllBytes(inputFile);

        // ランレングス圧縮
        var enc = EncodingRunLength(bytes);

        // 圧縮内容書き込み
        File.WriteAllBytes(outputFile, enc);

        // 回答内容書き込み
        var dec = DecodingRunLength(enc);
        File.WriteAllBytes($"{inputFile}_dec.txt", dec);
    }

    // 圧縮
    public static void Encode(string inputFile, string outputFile)
    {
        // ファイル内容読込
        var bytes = File.ReadAllBytes(inputFile);
        // ランレングス圧縮
        var enc = EncodingRunLength(bytes);
        // 圧縮内容書き込み
        File.WriteAllBytes(outputFile, enc);
    }

    // 解凍
    public static void Decode(string inputFile, string outputFile)
    {
        // ファイル内容読込
        var bytes = File.ReadAllBytes(inputFile);
        // 解凍
        var dec = DecodingRunLength(bytes);
        // 解凍内容書き込み
        File.WriteAllBytes(outputFile, dec);
    }

    // ランレングス圧縮を行う
    private static byte[] EncodingRunLength(byte[] bytes)
    {
        var result = new List<byte>();

        int length = 0;
        byte b = 0;

        for (int i = 0; i < bytes.Length; i++)
        {
            if (i == 0)
            {
                // 1文字目の場合保持
                length = 1;
                b = bytes[0];
            }
            else if (bytes[i] == b)
            {
                // 直前の文字と一致していればカウントアップ
                length++;
            }

            // 不一致のタイミングで出力
            if (bytes[i] != b)
            {
                result.AddRange(GetRunLength(b, length));

                // 文字データ更新
                length = 1;
                b = bytes[i];
            }
        }

        // 最後の圧縮結果を出力
        result.AddRange(GetRunLength(b, length));

        return result.ToArray();
    }

    // 文字と連続数から圧縮結果文字列を生成
    private static byte[] GetRunLength(byte b, int length)
    {
        // A, 256 のデータから { A, 255, A, 1 } という配列を返す
        var result = new List<byte>();
        const int MaxLength = 255;  // 1バイトで表現できる最大値

        for (int i = 1; i <= length; i++)
        {
            if (i % MaxLength == 0)
            {
                result.Add(b);
                result.Add(MaxLength);
            }
            else if (i == length)
            {
                // 最終文字数時点で出力
                result.Add(b);
                result.Add((byte)(length % MaxLength));
            }
        }

        return result.ToArray();
    }

    // ランレングス圧縮されたデータを解凍
    private static byte[] DecodingRunLength(byte[] bytes)
    {
        var result = new List<byte>();
        byte b = 0;
        for (int i = 0; i < bytes.Length; i++)
        {
            // 偶数番目には文字, 奇数番目にはデータ長
            if (i % 2 == 0)
            {
                b = bytes[i];
            }
            else
            {
                // データの長さ分バイトデータを作成し末尾に追加
                result.AddRange(Enumerable.Repeat(b, bytes[i]));
            }
        }
        return result.ToArray();
    }
}

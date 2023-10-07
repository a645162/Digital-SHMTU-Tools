# Encoding: UTF-8
import subprocess


def output_py(file_path):
    cmd = "python {}".format(file_path)

    # 不可以用下列，因为无法设置解码所用的编码
    # r = os.popen(cmd)
    # text = r.read()
    # r.close()

    test_monkey = (
        subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    )
    text = test_monkey.stdout.read().decode("utf-8")

    with open(file_path + ".txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == '__main__':
    output_py("ReadDatabase.py")

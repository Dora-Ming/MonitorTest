import difflib
import codecs

# 比较两个文件,并生成比较文档
def compare(file1_path, file2_path, out_file):
    try:
        with codecs.open(file1_path, 'r') as file1, codecs.open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        diff = difflib.HtmlDiff()
        result = diff.make_file(file1_lines, file2_lines)

        # 比较两个文件，将比对差异写入磁盘的html文件，注意加入encoding=utf-8，否则出现乱码
        with codecs.open(out_file, 'w', encoding='utf-8') as f:
            f.writelines(result)
        
    except Exception as e:
        print("错误:" + str(e))
    
    
if __name__ == "__main__":
    path_f1 = 'C:/text1.txt'
    path_f2 = 'C:/text2.txt'
    path_out = 'C:/Python Code/MonitorTest/diff.htm'

    compare(path_f1, path_f2, path_out)
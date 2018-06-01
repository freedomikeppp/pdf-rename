# coding: utf-8
import os
import re
import pprint

def get_exclusion_pages():
	'''
	除外ページを記載したテキストを読み込み、配列へ入れる

	Return:
		list: ページ(int)の配列
	'''
	exclusion_pages = []
	filenm = 'exclusion_pages.txt'
	if os.path.exists(filenm):
		f = open(filenm)
		exclusion_pages = f.readlines()[0].split(',')
		f.close()
	return exclusion_pages

def get_target_pdf_filenames():
	'''
	カレントディレクトリの変更対象となるpdfのソート済みリストを取得

	Return:
		list: ページ(int)の配列
	'''
	re_pdf = re.compile('-[0-9]+\.pdf')
	target_files = [path for path in os.listdir(os.curdir) if re_pdf.search(path)]
	target_files.sort()
	return target_files

def rename_and_remove(target_files, exclusion_pages, del_flg=False):
	'''
	対象のファイルをリネームする。また除外ファイルは削除する。

	Return:
		list: ページ(int)の配列
	'''
	re_pdf = re.compile('-[0-9]+\.pdf')
	re_num = re.compile('[0-9]+')
	page_count = 1

	for file in target_files:
		if re_pdf.search(file):
			# exp) IKE001-0000900-01.pdf -> 01.pdf
			split_filenm = file.rsplit('-', 1)[1]

			# マッチした数字を取り出しintへキャスト（左0埋めを取る為 exp) 01->1）
			number = int(re_num.search(split_filenm).group(0))

			# 除外対象のページなら、ファイルを削除し、renameをスキップ
			if str(number) in exclusion_pages:
				print('削除：' + file)
				if del_flg == True:
					os.remove(file)
				continue
			
			print(f'変換：{file} -> {page_count}.pdf')
			os.rename(file, f'{page_count}.pdf')
			page_count += 1

def run():
	pp = pprint.PrettyPrinter(indent=4)
	target_filenames = get_target_pdf_filenames()
	exclusion_pages = get_exclusion_pages()

	print("対象のファイル：" )
	pp.pprint(target_filenames)

	print("除外対象のページ：")
	pp.pprint(exclusion_pages)

	if input('実行しますか？ y or n: ') == 'y':
		if input('除外対象のページPDFを削除しますか？ y or n: ') == 'y':
			rename_and_remove(target_filenames, exclusion_pages, del_flg=True)
		else:
			rename_and_remove(target_filenames, exclusion_pages, del_flg=False)
	else:
		return

	# pause
	input('完了しました。')


if __name__ == '__main__':
	run()
